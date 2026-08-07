# app/control_ap_http.py
# V2 PH4 mobile control adapter (AP + HTTP receiver)
#
# Non-blocking: tick() processes at most one connection per call.
# Motor authority is NOT here — it calls app.drive_i2c.set_cmd()

import network
import socket
import time
from app import drive_i2c as drive

AP_SSID = "ENZO_HOST"
AP_PASS = "enzo1234"  # 8+ chars; set "" for open if desired
AP_CH = 6

_ap = None
_sock = None
_ready = False
_ip = None

HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>ENZO — PH4</title>
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
    <h1>ENZO</h1>
    <p class="sub">PH4 — Mobile control integrated (V1 features keep running)</p>

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

// Must be comfortably less than FAILSAFE_MS on ESP (drive_i2c)
const REPEAT_MS = 120;

async function send(c){
  try{
    const r = await fetch('/cmd?c=' + encodeURIComponent(c), {cache:'no-store'});
    const t = await r.text();
    st.textContent = 'TX ' + c + ' | ' + t.trim();
  }catch(e){
    st.textContent = 'TX failed: ' + e;
  }
}

function startHold(cmd){
  if(activeCmd === cmd) return;
  stopHold(false);
  activeCmd = cmd;
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

  el.addEventListener('touchstart', down, {passive:false});
  el.addEventListener('touchend', up, {passive:false});
  el.addEventListener('touchcancel', up, {passive:false});

  el.addEventListener('mousedown', down);
  el.addEventListener('mouseup', up);
  el.addEventListener('mouseleave', up);
}

bindHold('W','W');
bindHold('A','A');
bindHold('S','S');
bindHold('D','D');

document.getElementById('X').addEventListener('mousedown', (e)=>{e.preventDefault(); stopHold(true);});
document.getElementById('X').addEventListener('touchstart', (e)=>{e.preventDefault(); stopHold(true);}, {passive:false});
document.getElementById('X').addEventListener('click', (e)=>{e.preventDefault(); stopHold(true);});

window.addEventListener('blur', ()=>stopHold(true));
</script>
</body>
</html>
"""


def _http_reply(conn, status="200 OK", content_type="text/html", body=""):
    if isinstance(body, str):
        body_b = body.encode("utf-8")
    else:
        body_b = body
    hdr = (
        "HTTP/1.1 %s\r\n"
        "Content-Type: %s; charset=utf-8\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, OPTIONS\r\n"
        "Access-Control-Allow-Headers: *\r\n"
        "\r\n"
    ) % (status, content_type, len(body_b))
    try:
        conn.send(hdr.encode("utf-8") + body_b)
    except OSError:
        pass


def _parse_path(req_line):
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


def _get_qs_value(qs, key):
    for kv in qs.split("&"):
        if "=" in kv:
            k, v = kv.split("=", 1)
            if k == key:
                v = v.replace("+", " ")
                out = ""
                i = 0
                while i < len(v):
                    if v[i] == "%" and i + 2 < len(v):
                        try:
                            out += chr(int(v[i + 1 : i + 3], 16))
                            i += 3
                            continue
                        except Exception:
                            pass
                    out += v[i]
                    i += 1
                return out
    return ""


def init():
    global _ap, _sock, _ready, _ip

    if _ready:
        return True

    # Ensure motor service is ready
    try:
        drive.init()
    except Exception as e:
        print("[PH4] drive.init fail:", e)

    _ap = network.WLAN(network.AP_IF)
    _ap.active(True)

    if AP_PASS:
        _ap.config(
            essid=AP_SSID,
            password=AP_PASS,
            authmode=network.AUTH_WPA_WPA2_PSK,
            channel=AP_CH,
        )
    else:
        _ap.config(essid=AP_SSID, authmode=network.AUTH_OPEN, channel=AP_CH)

    time.sleep_ms(300)
    _ip = _ap.ifconfig()[0]
    print("[PH4] AP up:", AP_SSID, "IP:", _ip)
    print("[PH4] Open: http://%s" % _ip)

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    _sock = socket.socket()
    _sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _sock.bind(addr)
    _sock.listen(2)
    _sock.settimeout(0.0)  # NON-BLOCKING accept
    _ready = True
    print("[PH4] HTTP ready :80")
    return True


def tick():
    """
    Call frequently from tasks loop.
    Non-blocking: handles max one request per tick.
    """
    if not _ready:
        return

    try:
        conn, _ = _sock.accept()
    except OSError:
        return

    try:
        conn.settimeout(0.05)
        req = conn.recv(1024)
        if not req:
            return

        if req.startswith(b"OPTIONS "):
            _http_reply(conn, body="")
            return

        line = req.split(b"\r\n", 1)[0].decode("utf-8", "ignore")
        path, qs = _parse_path(line)

        if path == "/" or path == "/index.html":
            _http_reply(conn, content_type="text/html", body=HTML)
            return

        if path == "/cmd":
            c = _get_qs_value(qs, "c")
            ok = drive.set_cmd(c)
            if ok:
                _http_reply(conn, content_type="text/plain", body="OK c=%s" % (c,))
            else:
                _http_reply(
                    conn,
                    status="400 Bad Request",
                    content_type="text/plain",
                    body="BAD c=%s" % (c,),
                )
            return

        _http_reply(conn, status="404 Not Found", content_type="text/plain", body="Not Found")

    except Exception as e:
        try:
            _http_reply(conn, status="500 Internal Server Error", content_type="text/plain", body="ERR %r" % (e,))
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except OSError:
            pass
