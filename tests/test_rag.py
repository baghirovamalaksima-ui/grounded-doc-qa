from pathlib import Path
from unittest.mock import patch
import pytest
from rag import Chunk, ask, grounded, load_documents, retrieve

@pytest.fixture
def docs():
    return load_documents(Path(__file__).parents[1] / 'data')

def test_cited_answer(docs):
    answer = ask('How many paid vacation days?', docs)
    assert answer['status'] == 'answered'
    assert grounded(answer['claims'], docs)
    assert '20' in answer['claims'][0]['quote']

@pytest.mark.parametrize('question', ['Mars population?', '', 'salary bonuses?'])
def test_unknown_abstains(docs, question):
    assert ask(question, docs)['status'] == 'abstained'

def test_empty_corpus():
    assert ask('paid vacation days', [])['status'] == 'abstained'

@pytest.mark.parametrize('claims', [[], [{'quote': 'Invented paid vacation days', 'source': 'x'}],
    [{'quote': 'Employees receive 99 days', 'source': 'a'}], [{'quote': '', 'source': 'a'}]])
def test_reject_fabrication(claims):
    assert not grounded(claims, [Chunk('a', 'Employees receive 20 days')])

def test_deterministic_ties():
    assert retrieve('vacation', [Chunk('b', 'vacation'), Chunk('a', 'vacation')])[0][1].id == 'a'

def test_bad_k():
    with pytest.raises(ValueError):
        retrieve('x', [], 0)

def test_model_connection_failure(docs):
    with patch('urllib.request.urlopen', side_effect=OSError):
        assert ask('paid vacation days', docs, model='demo')['status'] == 'abstained'

def test_forged_llm_output(docs):
    import io
    import json
    body = json.dumps({'response': json.dumps({'claims': [{'source': 'handbook.md#p2',
        'quote': 'Employees receive 999 paid vacation days per year.'}]})}).encode()
    with patch('urllib.request.urlopen', return_value=io.BytesIO(body)):
        assert ask('paid vacation days', docs, model='demo')['status'] == 'abstained'
