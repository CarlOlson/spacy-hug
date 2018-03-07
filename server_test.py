
import hug
import server
from falcon import HTTP_200, HTTP_400, HTTP_404

def test_not_found():
    response = hug.test.get(server, '', {})
    assert response.status == HTTP_404
    assert response.data == 'not_found.'

def test_parse_without_params():
    response = hug.test.get(server, '/parse', {})
    assert response.status == HTTP_400
    assert response.data == 'empty.'

def test_parse_with_empty_param():
    response = hug.test.get(server, '/parse', {'text': ''})
    assert response.status == HTTP_400
    assert response.data == 'empty.'

def test_parse_with_valid_string():
    response = hug.test.get(server, '/parse', {'text': 'Hello World.'})
    assert response.status == HTTP_200
    assert response.data == 'word(world, nn, root, [])'
