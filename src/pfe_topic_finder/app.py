"""FastAPI application for browsing and recommending PFE topics."""

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pfe_topic_finder.recommender import filter_topics, load_topics, recommend_topics

_PACKAGE_DIR = Path(__file__).resolve().parent
_STATIC_DIR = _PACKAGE_DIR / "static"

app = FastAPI(
    title="PFE AI Topic Finder",
    description="Browse and discover AI project topics using content-based ranking.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    """Serve the web interface."""
    return FileResponse(_STATIC_DIR / "index.html")


@app.get("/api/topics")
def get_topics(domain: str | None = None) -> dict[str, object]:
    """List topics, optionally filtered by domain."""
    topics = filter_topics(domain)

    if domain and not topics:
        available_domains = sorted({topic["domain"] for topic in load_topics()})
        raise HTTPException(
            status_code=404,
            detail={
                "message": "No topics found for this domain.",
                "available_domains": available_domains,
            },
        )

    return {"count": len(topics), "topics": topics}


@app.get("/api/recommend")
def get_recommendations(
    interests: str = Query(min_length=2, description="Interests or desired keywords"),
    domain: str | None = None,
    limit: int = Query(default=5, ge=1, le=20),
) -> dict[str, object]:
    """Recommend topics matching a student's interests."""
    topics = recommend_topics(interests=interests, limit=limit, domain=domain)
    return {"count": len(topics), "topics": topics}
