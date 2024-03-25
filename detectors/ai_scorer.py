from abc import ABC, abstractmethod
import openai
import anthropic

class AIScorer(ABC):
    @abstractmethod
    def score_paper(self, abstract):
        pass

class OpenAIScorer(AIScorer):
    def __init__(self, api_key, prompt):
        self.api_key = api_key
        self.prompt = prompt

    def score_paper(self, abstract):
        response = openai.Completion.create(
            engine="davinci",
            prompt=self.prompt + "\n\nAbstract:\n" + abstract,
            max_tokens=150,
            api_key=self.api_key
        )
        score = response.choices[0].text.strip()
        return score

class AnthropicScorer(AIScorer):
    def __init__(self, api_key, prompt):
        self.api_key = api_key
        self.prompt = prompt

    def score_paper(self, abstract):
        # Placeholder for Anthropic API call, as the actual API details are not provided
        # This should be replaced with the actual API call when the details are available
        score = "Anthropic API score for the abstract"
        return score
