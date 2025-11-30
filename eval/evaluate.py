from agents.research_agent import ResearchAgent
from agents.outline_agent import OutlineAgent
from agents.writer_agent import WriterAgent
import os

# Simple evaluation: compare baseline (single-call) vs pipeline

researcher = ResearchAgent()
outliner = OutlineAgent()
writer = WriterAgent()

TOPIC = os.environ.get('EVAL_TOPIC', 'Impact of AI on Finance')

# Baseline: single-call writer that is given only topic
print('\n=== Running baseline single-call writer ===')
baseline = writer.run(TOPIC, outline=f"- {TOPIC}", style='neutral')
print('Baseline word count:', len(baseline.split()))

# Pipeline
print('\n=== Running multi-agent pipeline ===')
notes = researcher.run(TOPIC)
outline = outliner.run(TOPIC, notes, style='neutral')
article = writer.run(TOPIC, outline, style='neutral')
print('Pipeline word count:', len(article.split()))

print('\n--- Outline used: ---')
print(outline)

print('\n--- Pipeline article (first 800 chars): ---')
print(article[:800])

# Basic manual scoring guidance
print('\n\nManual evaluation suggestions:')
print('1) Read both articles and rate preference 1-5 for quality.')
print('2) Check coherence to outline, factuality, and actionable takeaways.')
