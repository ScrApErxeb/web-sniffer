from unittest.mock import patch, Mock
from core.http_client import fetch

def test_fetch_success():
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.text = "<html>ok</html>"
    with patch("requests.get", return_value=mock_resp):
        html = fetch("https://example.com")
        assert html == "<html>ok</html>"

def test_fetch_failure():
    with patch("requests.get", side_effect=Exception("fail")):
        html = fetch("https://example.com")
        assert html is None
