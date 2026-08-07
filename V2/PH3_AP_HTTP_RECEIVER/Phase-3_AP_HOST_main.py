# main.py — V3 Phase 3 (Bring-up): ESP AP + Web UI -> Motor Control
# Goal:
#   Phone connects to ENZO Wi‑Fi (AP mode), opens http://192.168.4.1
#   Buttons send W/A/S/D/X to the ESP over HTTP.
#
# Controls:
#   W = forward
#   S = reverse
#   A = pivot left  (left track backwards, right track forwards)
#   D = pivot right (right track backwards, left track forwards)
#   X = stop (also sent on button release)
#
# Safety:
#   - Deadman: if no valid command received for FAILSAFE_MS -> STOP
#
# Notes:
#   - This is a *bring-up tool* (like V2 Phase 2). It can temporarily replace your full ENZO runtime.
#   - Later we’ll merge this into the V1 feature set (tasks loop) so ENZO keeps all features + mobile control.

from machine import Pin, I2C
import network
import socket
import time

# ----------------------------
# Motor driver (same as V2 Phase 2 proven setup)
# ----------------------------
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100_000)  # SDA=8, SCL=9
ADDR = 0x14

MOTOR_LEFT  = 0  # Motor A
MOTOR_RIGHT = 1  # Motor B

CMD_STOP     = 0x01
CMD_RUN_CW   = 0x02
CMD_RUN_CCW  = 0x03

SPEED = 200

# If "forward" is physically backwards on your build, swap these two:
FWD_CMD = CMD_RUN_CCW
REV_CMD = CMD_RUN_CW

def send(cmd, motor, speed=0):
    try:
        i2c.writeto(ADDR, bytes([cmd, motor, speed]))
    except Exception:
        # If I2C glitches, fail safe.
        pass

def stop_all():
    send(CMD_STOP, MOTOR_LEFT)
    send(CMD_STOP, MOTOR_RIGHT)

def forward():
    send(FWD_CMD, MOTOR_LEFT, SPEED)
    send(FWD_CMD, MOTOR_RIGHT, SPEED)

def reverse():
    send(REV_CMD, MOTOR_LEFT, SPEED)
    send(REV_CMD, MOTOR_RIGHT, SPEED)

def pivot_left():
    # Left track backwards, right track forwards (rotate on the spot)
    send(REV_CMD, MOTOR_LEFT, SPEED)
    send(FWD_CMD, MOTOR_RIGHT, SPEED)

def pivot_right():
    # Right track backwards, left track forwards (rotate on the spot)
    send(FWD_CMD, MOTOR_LEFT, SPEED)
    send(REV_CMD, MOTOR_RIGHT, SPEED)

def apply_cmd(c):
    c = (c or "").upper()
    if c == "W":
        forward()
        return True
    if c == "S":
        reverse()
        return True
    if c == "A":
        pivot_left()
        return True
    if c == "D":
        pivot_right()
        return True
    if c == "X" or c == " ":
        stop_all()
        return True
    return False

# ----------------------------
# Wi‑Fi AP (Access Point) setup
# ----------------------------
AP_SSID = "ENZO_HOST"
AP_PASS = "enzo1234"   # must be 8+ chars. Set "" for open network if you want.
AP_CH   = 6

ap = network.WLAN(network.AP_IF)
ap.active(True)
if AP_PASS:
    ap.config(essid=AP_SSID, password=AP_PASS, authmode=network.AUTH_WPA_WPA2_PSK, channel=AP_CH)
else:
    ap.config(essid=AP_SSID, authmode=network.AUTH_OPEN, channel=AP_CH)

# Give it a moment to come up
time.sleep_ms(300)

ip = ap.ifconfig()[0]  # usually 192.168.4.1
print("ENZO AP up:", AP_SSID, "IP:", ip)
print("Open: http://%s" % ip)

# ----------------------------
# Tiny HTTP server + page
# ----------------------------
HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Enzo Host — Phase 3</title>
  <style>
    body{font-family:system-ui,Segoe UI,Arial,sans-serif;background:#f2f2f2;margin:0}
    .wrap{max-width:520px;margin:32px auto;padding:0 16px;text-align:center}
    h1{margin:0 0 6px 0}
    .sub{opacity:.7;margin:0 0 18px 0}
    .grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;align-items:center;justify-items:center}
    .btn{user-select:none;touch-action:none;width:140px;height:80px;border:2px solid #999;border-radius:12px;
         background:white;font-size:26px;font-weight:700;display:flex;align-items:center;justify-content:center}
    .btn:active{background:#e6e6e6}
    .status{margin-top:18px;font-family:ui-monospace,Consolas,monospace;opacity:.85}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Enzo Host</h1>
    <p class="sub">Phase 3 — Mobile Web Control (Bring‑up)</p>

    <div class="grid">
      <div></div>
      <div class="btn" id="W">W</div>
      <div></div>

      <div class="btn" id="A">A</div>
      <div class="btn" id="X">STOP</div>
      <div class="btn" id="D">D</div>

      <div></div>
      <div class="btn" id="S">S</div>
      <div></div>
    </div>

    <div class="status" id="st">Ready.</div>
  </div>

<script>
const st = document.getElementById('st');

let holdTimer = null;
let activeCmd = null;

// How often to resend while holding (ms).
// Must be comfortably less than FAILSAFE_MS on the ESP.
const REPEAT_MS = 120;

async function send(c){
  try{
    const r = await fetch('/cmd?c=' + encodeURIComponent(c), {cache:'no-store'});
    const t = await r.text();
    st.textContent = 'TX ' + c + '  |  ' + t.trim();
  }catch(e){
    st.textContent = 'TX failed: ' + e;
  }
}

function startHold(cmd){
  if(activeCmd === cmd) return;

  stopHold(false);   // stop previous hold without sending X yet
  activeCmd = cmd;

  // Send immediately, then repeat
  send(cmd);
  holdTimer = setInterval(() => send(cmd), REPEAT_MS);
}

function stopHold(sendStop=true){
  if(holdTimer){
    clearInterval(holdTimer);
    holdTimer = null;
  }
  if(activeCmd !== null){
    activeCmd = null;
    if(sendStop) send('X');
  }
}

function bindHold(id, cmd){
  const el = document.getElementById(id);

  const down = (ev)=>{ ev.preventDefault(); startHold(cmd); };
  const up   = (ev)=>{ ev.preventDefault(); stopHold(true); };

  // Touch
  el.addEventListener('touchstart', down, {passive:false});
  el.addEventListener('touchend', up, {passive:false});
  el.addEventListener('touchcancel', up, {passive:false});

  // Mouse (PC testing)
  el.addEventListener('mousedown', down);
  el.addEventListener('mouseup', up);
  el.addEventListener('mouseleave', up);
}

bindHold('W','W');
bindHold('A','A');
bindHold('S','S');
bindHold('D','D');

// STOP button: stop immediately
document.getElementById('X').addEventListener('mousedown', (e)=>{e.preventDefault(); stopHold(true);});
document.getElementById('X').addEventListener('touchstart', (e)=>{e.preventDefault(); stopHold(true);}, {passive:false});
document.getElementById('X').addEventListener('click', (e)=>{e.preventDefault(); stopHold(true);});

// If browser/tab loses focus, stop for safety
window.addEventListener('blur', ()=>stopHold(true));

// Optional: keyboard on laptop when connected to AP
document.addEventListener('keydown', (e)=>{
  const k = (e.key||'').toUpperCase();
  if(['W','A','S','D','X'].includes(k)){ startHold(k); }
  if(e.code === 'Space'){ stopHold(true); }
});
document.addEventListener('keyup', (e)=>{
  const k = (e.key||'').toUpperCase();
  if(['W','A','S','D'].includes(k)){ stopHold(true); }
});
</script>
</body>
</html>
"""

def http_reply(conn, status="200 OK", content_type="text/html", body=""):
    if isinstance(body, str):
        body_b = body.encode("utf-8")
    else:
        body_b = body
    hdr = (
        "HTTP/1.1 %s\r\n"
        "Content-Type: %s; charset=utf-8\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n"
        # CORS headers are harmless here, and make it easier if someone loads a local file by accident.
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, OPTIONS\r\n"
        "Access-Control-Allow-Headers: *\r\n"
        "\r\n"
    ) % (status, content_type, len(body_b))
    # Browsers can drop connections; ignore socket timeouts.
    try:
        conn.send(hdr.encode("utf-8") + body_b)
    except OSError:
        pass

def parse_path(req_line):
    # "GET /cmd?c=W HTTP/1.1"
    try:
        parts = req_line.split()
        if len(parts) < 2:
            return "/", ""
        path_q = parts[1]
        if "?" in path_q:
            p, q = path_q.split("?", 1)
            return p, q
        return path_q, ""
    except Exception:
        return "/", ""

def get_qs_value(qs, key):
    # minimal query string parser
    for kv in qs.split("&"):
        if "=" in kv:
            k, v = kv.split("=", 1)
            if k == key:
                # decode %xx and +
                v = v.replace("+", " ")
                out = ""
                i = 0
                while i < len(v):
                    if v[i] == "%" and i + 2 < len(v):
                        try:
                            out += chr(int(v[i+1:i+3], 16))
                            i += 3
                            continue
                        except Exception:
                            pass
                    out += v[i]
                    i += 1
                return out
    return ""

# ----------------------------
# Main loop
# ----------------------------
FAILSAFE_MS = 250
last_rx = time.ticks_ms()

stop_all()

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(2)
s.settimeout(0.05)

print("HTTP server listening on 0.0.0.0:80")

while True:
    # Deadman stop
    if time.ticks_diff(time.ticks_ms(), last_rx) > FAILSAFE_MS:
        stop_all()
        last_rx = time.ticks_ms()

    try:
        conn, _ = s.accept()
    except OSError:
        time.sleep_ms(5)
        continue

    try:
        conn.settimeout(0.2)
        req = conn.recv(1024)
        if not req:
            try:
                conn.close()
            except OSError:
                pass
            continue

        # Handle OPTIONS (preflight)
        if req.startswith(b"OPTIONS "):
            http_reply(conn, body="")
            try:
                conn.close()
            except OSError:
                pass
            continue

        # First line only
        line = req.split(b"\r\n", 1)[0].decode("utf-8", "ignore")
        path, qs = parse_path(line)

        if path == "/" or path == "/index.html":
            http_reply(conn, content_type="text/html", body=HTML)
        elif path == "/cmd":
            c = get_qs_value(qs, "c")
            ok = apply_cmd(c)
            if ok:
                last_rx = time.ticks_ms()
                http_reply(conn, content_type="text/plain", body="OK c=%s" % (c,))
            else:
                http_reply(conn, status="400 Bad Request", content_type="text/plain", body="BAD c=%s" % (c,))
        else:
            http_reply(conn, status="404 Not Found", content_type="text/plain", body="Not Found")
    except Exception as e:
        try:
            http_reply(conn, status="500 Internal Server Error", content_type="text/plain", body="ERR %r" % (e,))
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except OSError:
            pass

