ENZO V2 END BASELINE SNAPSHOT

This folder represents the completed V2 state produced from the V1 end baseline after the Phase 4 integration steps.

Runtime placement on the ESP:
- main.py -> /main.py
- application modules in this folder -> /app/
- actuators/__init__.py -> /app/actuators/__init__.py

pins.py and selftest.py are retained from the V1 baseline as optional diagnostic/reference files. They are not imported by the normal V2 runtime and are not required for normal boot.

The empty actuators package is intentionally retained from the V1 baseline structure.
