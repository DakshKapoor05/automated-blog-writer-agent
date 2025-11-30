import os
import logging

logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


class WriterAgent:
    """Writes the final blog from an outline."""

    def __init__(self):
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        if OPENAI_AVAILABLE and self.openai_key:
            openai.api_key = self.openai_key
            self.use_openai = True
        else:
            self.use_openai = False

    def run(self, topic: str, outline: str, style='neutral') -> str:
        if self.use_openai:
            prompt = (
                f"Write a 400–600 word blog post on '{topic}'. Use this outline:\n{outline}\n\n"
                f"Tone: {style}. Keep paragraphs short and include a final actionable takeaway."
            )
            logger.info('Calling OpenAI to write blog...')
            try:
                resp = openai.ChatCompletion.create(
                    model='gpt-4o-mini',
                    messages=[{'role': 'user', 'content': prompt}],
                    max_tokens=700,
                    temperature=0.35,
                )
                blog = resp['choices'][0]['message']['content'].strip()
                return blog
            except Exception as e:
                logger.warning('OpenAI call failed in WriterAgent: %s', e)
                return self._mock(topic)
        else:
            logger.info('Using mock blog writer')
            return self._mock(topic)

    def _mock(self, topic: str):
        intro = f"{topic} is becoming an important topic today. Here's why it matters."
        body = (
            "The use-cases are varied and growing. Organisations see clear ROI when they automate. "
            "However, challenges exist, including cost and skills. To mitigate, start small and iterate."
        )
        outro = "Takeaway: start with a pilot and measure impact."
        return '\n\n'.join([intro, body, outro])
