import os
import logging
from typing import List

logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


class ResearchAgent:
    """
    Simple research agent: uses OpenAI to generate quick research notes for a topic.
    Falls back to a canned mock if OpenAI is not available or key missing.
    """

    def __init__(self):
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        if OPENAI_AVAILABLE and self.openai_key:
            openai.api_key = self.openai_key
            self.use_openai = True
        else:
            self.use_openai = False

    def run(self, topic: str) -> List[str]:
        if self.use_openai:
            prompt = (
                f"List 5 concise research notes (1 sentence each) about the topic: {topic}."
                " Include recent trends, common pain points, and notable use-cases."
            )
            logger.info('Calling OpenAI for research notes...')
            try:
                resp = openai.ChatCompletion.create(
                    model='gpt-4o-mini',
                    messages=[{'role': 'user', 'content': prompt}],
                    max_tokens=300,
                    temperature=0.2,
                )
                text = resp['choices'][0]['message']['content']
                notes = [n.strip('- \n') for n in text.split('\n') if n.strip()][:5]
                logger.info('Received %d research notes from OpenAI', len(notes))
                return notes
            except Exception as e:
                logger.warning('OpenAI call failed in ResearchAgent: %s', e)
                return self._mock(topic)
        else:
            logger.info('OpenAI key not found — using mock research notes')
            return self._mock(topic)

    def _mock(self, topic: str):
        mock = [
            f"{topic}: growing interest due to automation potential.",
            f"Cost and ethics are common concerns in {topic} applications.",
            "SMEs often lack data/skills to deploy end-to-end solutions.",
            "Recent tools reduce time-to-prototype significantly.",
            "High ROI reported in areas with repeatable processes."
        ]
        return mock
