import pytest
from retrievers.tasks import score_abstract
from detectors.ai_scorer import OpenAIScorer, AnthropicScorer

@pytest.fixture
def abstract():
    return "This is a test abstract for a research paper."

@pytest.fixture
def openai_scorer(mocker):
    mocker.patch('detectors.ai_scorer.OpenAIScorer.score_paper', return_value=(42, "Test explanation"))
    return OpenAIScorer(api_key="test_api_key")

@pytest.fixture
def anthropic_scorer(mocker):
    mocker.patch('detectors.ai_scorer.AnthropicScorer.score_paper', return_value=(50, "Placeholder explanation"))
    return AnthropicScorer(api_key="test_api_key")

def test_score_abstract_openai(abstract, openai_scorer, mocker):
    mocker.patch('retrievers.tasks.config', return_value='OpenAI')
    score, explanation, scorer_type = score_abstract(abstract)
    assert score == 42
    assert explanation == "Test explanation"
    assert scorer_type == 'OpenAI'

def test_score_abstract_anthropic(abstract, anthropic_scorer, mocker):
    mocker.patch('retrievers.tasks.config', return_value='Anthropic')
    score, explanation, scorer_type = score_abstract(abstract)
    assert score == 50
    assert explanation == "Placeholder explanation"
    assert scorer_type == 'Anthropic'
