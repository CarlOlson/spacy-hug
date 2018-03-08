
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

    doc = nlp(text).doc
    root = next(word for word in doc if word.dep_ == 'ROOT')
    return build_term(root, doc)

def build_term(root, doc):
    children = []
    for word in doc:
        if word.head.i == root.i and word.i != root.i:
            children.append(build_term(word, doc))

    lemma = nlp.vocab[root.lemma].text
    pos = root.tag_.lower()
    children = ', '.join(children)
    return 'word({lemma}, {pos}, root, [{children}])'.format(**locals())
