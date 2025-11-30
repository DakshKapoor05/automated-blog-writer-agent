from fastapi import FastAPI, Query
from pydantic import BaseModel
import uvicorn
import logging
from agents.research_agent import ResearchAgent
from agents.outline_agent import OutlineAgent
from agents.writer_agent import WriterAgent
from session.memory import SessionMemory
import os

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Automated Blog Writer")

# Initialize agents and memory
memory = SessionMemory(save_path='session_memory.json')
researcher = ResearchAgent()
outliner = OutlineAgent()
writer = WriterAgent()


class GenerateResponse(BaseModel):
    topic: str
    style: str
    outline: str
    blog: str
    metadata: dict


@app.get("/generate_blog", response_model=GenerateResponse)
async def generate_blog(topic: str = Query(...), style: str = Query("neutral")):
    logger.info('New request: topic="%s", style="%s"', topic, style)

    session_id = f"session_{topic[:20].replace(' ', '_')}"
    memory.set(session_id, {"topic": topic, "style": style})

    # 1) Research step
    logger.info("Running ResearchAgent")
    research_notes = researcher.run(topic)
    logger.info("Research notes length: %d", len(research_notes))

    # 2) Outline step
    logger.info("Running OutlineAgent")
    outline = outliner.run(topic, research_notes, style)

    # 3) Writer step
    logger.info("Running WriterAgent")
    blog = writer.run(topic, outline, style)

    metadata = {
        "research_snippet_count": len(research_notes),
        "word_count": len(blog.split()),
    }

    # Persist memory snapshot
    memory.append(session_id, {"outline": outline, "blog": blog})

    return GenerateResponse(
        topic=topic,
        style=style,
        outline=outline,
        blog=blog,
        metadata=metadata,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
