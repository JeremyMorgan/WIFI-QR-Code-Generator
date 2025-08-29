# Wi‑Fi QR Generator (Flask)

A tiny Flask app that makes a QR code for your Wi‑Fi network. Point a phone camera at the QR to join without typing a password.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

## Notes
- No database; everything is in-memory.
- Supports WPA/WPA2/WPA3, WEP, or open networks.
- Escapes special characters in SSID/password per Wi‑Fi QR spec.
