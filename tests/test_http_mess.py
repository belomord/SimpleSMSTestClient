import src.file_config
import src.http_url
import src.http_mess


def test_http_request():
    user = src.file_config.User(login='user1', password='password')
    url = src.http_url.HttpUrl(protocol='http', host='localhost', port=80, path='/api')
    body = '{"test":1}'

    http_req = src.http_mess.HttpRequest(url=url, user=user, body=body)
    b = http_req.to_bytes()
    http_req = src.http_mess.HttpRequest.from_bytes(b)

    assert http_req.user.login == user.login
    assert http_req.user.password == user.password

    assert http_req.url.host == url.host
    assert http_req.url.port == url.port
    assert http_req.url.path == url.path

    assert http_req.body == body


def test_http_response():
    code = 200
    text = 'OK'
    body = '{"test":1}'
    http_resp = src.http_mess.HttpResponse(code=code, message=text, body=body)
    b = http_resp.to_bytes()
    http_resp = src.http_mess.HttpResponse.from_bytes(b)

    assert http_resp.code == code
    assert http_resp.message == text
    assert http_resp.body == body
    