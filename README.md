# PFE AI Topic Finder

A small local web application for browsing AI project topics and ranking them
against a student's interests. The recommender uses a lightweight TF-IDF
content-based method; it does not call an external AI service.

## Prerequisites

- Python 3.11 or newer
- Bash to use `setup.sh`

## Setup

From the repository directory:

```bash
chmod +x setup.sh
./setup.sh
Activate the virtual environment:

bash


source .venv/bin/activate
Run
bash


uvicorn pfe\_topic\_finder.app:app --reload
Open http://127.0.0.1:8000 in a browser.

API
GET /api/topics lists all topics.
GET /api/topics?domain=Healthcare filters by domain.
GET /api/recommend?interests=Arabic%20NLP ranks topics by relevance.
Add domain to recommendations to filter the results.
Add limit to set the maximum number of results (1–20).
GET /docs opens the automatically generated API documentation.
Configuration and catalogue
No environment variables or credentials are required. Edit
src/pfe_topic_finder/topics.json to add, update, or remove topic suggestions.
Each topic should include an ID, title, domain, summary, methods, datasets,
level, and keywords.

Dataset names are suggestions for research planning. Check each dataset's
license, access requirements, and suitability before using it in a thesis.

Tests
Install development dependencies using ./setup.sh, then run:

bash


pytest
Current scope
This version provides a topic catalogue and local content-based recommendations.
It does not generate new research proposals, assess academic novelty, or
replace a supervisor's review.