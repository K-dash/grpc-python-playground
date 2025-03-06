from urllib.request import urlopen

def test_render_homepage():
    homepage_html = urlopen("http://localhost:8001").read().decode("utf-8")
    assert "<title>Online Books For You</title>" in homepage_html
    assert homepage_html.count("<li>") == 2
