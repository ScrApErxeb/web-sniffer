from core.parser import parse_html_title


def test_parse_html_title():
    html = "<html><head><title>Test</title></head></html>"
    title = parse_html_title(html)
    assert title == "Test"
