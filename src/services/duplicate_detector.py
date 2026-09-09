from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .history import load_history


DUPLICATE_THRESHOLD = 0.85


def check_duplicate(post: str) -> tuple[bool, float]:
    history = load_history()

    if not history:
        return False, 0.0

    previous_posts = [
        item["content"]
        for item in history
        if item.get("content")
    ]

    if not previous_posts:
        return False, 0.0

    documents = previous_posts + [post]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
    )

    vectors = vectorizer.fit_transform(documents)

    new_vector = vectors[-1]
    old_vectors = vectors[:-1]

    similarities = cosine_similarity(
        new_vector,
        old_vectors,
    )[0]

    highest_similarity = float(max(similarities))

    is_duplicate = (
        highest_similarity >= DUPLICATE_THRESHOLD
    )

    return is_duplicate, highest_similarity