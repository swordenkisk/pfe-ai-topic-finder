from pfe_topic_finder.recommender import (
    filter_topics,
    load_topics,
    recommend_topics,
    tokenize,
)


def test_tokenize_returns_lowercase_words() -> None:
    assert tokenize("Arabic NLP, 2026!") == ["arabic", "nlp", "2026"]


def test_catalogue_contains_topics() -> None:
    assert len(load_topics()) >= 5


def test_filter_topics_is_case_insensitive() -> None:
    topics = filter_topics("healthcare")

    assert topics
    assert all(topic["domain"] == "Healthcare" for topic in topics)


def test_recommendations_rank_matching_topics() -> None:
    topics = recommend_topics("Arabic NLP text classification")

    assert topics
    assert topics[0]["id"] == "arabic-sentiment-analysis"
    assert all("score" in topic for topic in topics)


def test_recommendations_can_be_filtered_by_domain() -> None:
    topics = recommend_topics("computer vision", domain="Agriculture")

    assert topics
    assert all(topic["domain"] == "Agriculture" for topic in topics)


def test_unrelated_query_returns_no_recommendations() -> None:
    assert recommend_topics("quantum underwater volcanoes") == []
