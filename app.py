from flask import Flask, render_template, request
import io, base64
import qrcode

app = Flask(__name__)

def escape_wifi_text(s: str) -> str:
    """
    Escape special chars per Wi‑Fi QR standard: \\,;,: and quotes.
    """
    if s is None:
        return ""
    s = s.replace("\\", "\\\\")
    s = s.replace(";", r"\;").replace(",", r"\,").replace(":", r"\:")
    s = s.replace('"', r'\"').replace("'", r"\'")
    return s

def build_wifi_payload(ssid: str, password: str, auth: str, hidden: bool) -> str:
    # Map auth choices to standard values
    auth_map = {"WPA/WPA2/WPA3": "WPA", "WEP": "WEP", "None (open)": "nopass"}
    t = auth_map.get(auth, "WPA")
    ssid_e = escape_wifi_text(ssid or "")
    pwd_e = escape_wifi_text(password or "")
    hidden_str = "true" if hidden else "false"
    # When open network, omit P:
    if t == "nopass":
        payload = f"WIFI:T:{t};S:{ssid_e};H:{hidden_str};;"
    else:
        payload = f"WIFI:T:{t};S:{ssid_e};P:{pwd_e};H:{hidden_str};;"
    return payload

def make_qr_png_bytes(data: str) -> bytes:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

@app.route("/", methods=["GET", "POST"])
def index():
    qr_b64 = None
    payload = None
    ssid = password = ""
    auth = "WPA/WPA2/WPA3"
    hidden = False
    if request.method == "POST":
        ssid = request.form.get("ssid", "").strip()
        password = request.form.get("password", "").strip()
        auth = request.form.get("auth", "WPA/WPA2/WPA3")
        hidden = request.form.get("hidden") == "on"
        payload = build_wifi_payload(ssid, password, auth, hidden)
        png_bytes = make_qr_png_bytes(payload)
        qr_b64 = base64.b64encode(png_bytes).decode("ascii")
    return render_template("index.html", qr_b64=qr_b64, payload=payload, ssid=ssid, password=password, auth=auth, hidden=hidden)

if __name__ == "__main__":
    # For local dev only
    app.run(debug=True, host="0.0.0.0", port=5001)
    