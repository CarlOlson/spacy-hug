
import hug
import server
from falcon import HTTP_200, HTTP_400, HTTP_404

def test_not_found():
    response = hug.test.get(server, '', {})
    assert response.status == HTTP_404
    assert response.data == 'not_found.'

def test_empty_parse():
    response = hug.test.get(server, '/parse', {})
    assert response.status == HTTP_400
    assert response.data == 'empty.'

    response = hug.test.get(server, '/parse', {'text': ''})
    assert response.status == HTTP_400
    assert response.data == 'empty.'
