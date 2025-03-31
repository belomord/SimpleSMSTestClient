import src.http_url


def test_empty_url():
    assert src.http_url.HttpUrl().address == 'http://localhost:80/'
    assert src.http_url.HttpUrl(protocol='https').address == 'https://localhost:443/'


def test_url_by_address():
    adr = 'http://localhost:4010/send_sms/srv'
    url = src.http_url.HttpUrl.from_address(adr)
    assert url.address.lower() == adr.lower().strip()
