
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

def is_child_of(word, root):
    return word.head.i == root.i and word.i != root.i

def build_term(root, doc):
    if root.is_punct:
        return ''

    children = [word for word in doc if is_child_of(word, root)]
    children = map(lambda word: build_term(word, doc), children)
    children = ', '.join(children)

    lemma = nlp.vocab[root.lemma].text
    pos = root.tag_.lower()
    dep = root.dep_.lower()
    return 'word({lemma}, {pos}, {dep}, [{children}])'.format(**locals())
