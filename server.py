
import hug
import falcon
import spacy

nlp = spacy.load('en')

hug.API(__name__).http.output_format = hug.output_format.text

@hug.not_found()
def not_found():
    return 'not_found.'

@hug.get('/parse')
def parse(text:hug.types.text='', response=None):
    """Parse a string into a prolog-readable dependency graph."""
    if text == '':
        response.status = falcon.HTTP_400
        return 'empty.'

    nodes = []
    for word in nlp(text).doc:
        lemma = word.text.lower()
        pos = word.tag_.lower()
        nodes.append('word({lemma}, {pos}, root, [])'.format(**locals()))
    return nodes[1]
