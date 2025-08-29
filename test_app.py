import pytest
from app import escape_wifi_text, build_wifi_payload, make_qr_png_bytes, app

# Test escape_wifi_text
def test_escape_wifi_text_basic():
    assert escape_wifi_text('abc') == 'abc'

def test_escape_wifi_text_special_chars():
    # The actual output for 'a;b,c:d"e\f' is 'a\;b\,c\:d\"e\\f'
    result = escape_wifi_text('a;b,c:d"e\\f')
    assert result == 'a\\;b\\,c\\:d\\"e\\\\f'

def test_escape_wifi_text_none():
    assert escape_wifi_text(None) == ''

# Test build_wifi_payload
def test_build_wifi_payload_wpa():
    result = build_wifi_payload('MySSID', 'MyPass', 'WPA/WPA2/WPA3', False)
    assert result == 'WIFI:T:WPA;S:MySSID;P:MyPass;H:false;;'

def test_build_wifi_payload_wep():
    result = build_wifi_payload('SSID', '12345', 'WEP', True)
    assert result == 'WIFI:T:WEP;S:SSID;P:12345;H:true;;'

def test_build_wifi_payload_open():
    result = build_wifi_payload('OpenSSID', '', 'None (open)', False)
    assert result == 'WIFI:T:nopass;S:OpenSSID;H:false;;'

# Test make_qr_png_bytes
def test_make_qr_png_bytes_type():
    data = 'WIFI:T:WPA;S:Test;P:1234;H:false;;'
    png = make_qr_png_bytes(data)
    assert isinstance(png, bytes)
    assert png[:8] == b'\x89PNG\r\n\x1a\n'  # PNG header

# Flask app route test
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    # Check for a string present in the HTML title
    assert b'Wi' in response.data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
