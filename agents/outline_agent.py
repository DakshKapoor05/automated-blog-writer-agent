import os
import logging

logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


class OutlineAgent:
    """Creates a 3-4 point outline for the blog given research notes."""

    def __init__(self):
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        if OPENAI_AVAILABLE and self.openai_key:
            openai.api_key = self.openai_key
            self.use_openai = True
        else:
            self.use_openai = False

    def run(self, topic: str, notes, style='neutral') -> str:
        if self.use_openai:
            prompt = (
                f"Given these research notes:\n{chr(10).join(notes)}\n\n"
                f"Create a concise 4-point outline for a short blog post on '{topic}' in a {style} style."
            )
            logger.info('Calling OpenAI for outline...')
            try:
                resp = openai.ChatCompletion.create(
                    model='gpt-4o-mini',
                    messages=[{'role': 'user', 'content': prompt}],
                    max_tokens=250,
                    temperature=0.2,
                )
                outline = resp['choices'][0]['message']['content'].strip()
                return outline
            except Exception as e:
                logger.warning('OpenAI call failed in OutlineAgent: %s', e)
                return self._mock(topic)
        else:
            logger.info('Using mock outline')
            return self._mock(topic)

    def _mock(self, topic: str):
        bullets = [
            f"Intro to {topic}",
            "Key benefits and use-cases",
            "Challenges and mitigation",
            "Practical steps to get started"
        ]
        return '\n'.join([f"- {b}" for b in bullets])
