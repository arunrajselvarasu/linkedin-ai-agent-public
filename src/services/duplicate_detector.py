import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .history import load_history


DUPLICATE_THRESHOLD = 0.85


def normalize_text(text: str) -> str:
    """
    Normalize text before comparison.
    """

    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text,
    )

    # Remove LinkedIn-style hashtags
    text = re.sub(
        r"#\w+",
        " ",
        text,
    )

    # Remove punctuation
    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return text


def calculate_similarity(
    new_post: str,
    previous_posts: list[str],
) -> float:

    if not previous_posts:
        return 0.0

    documents = [
        normalize_text(post)
        for post in previous_posts
    ]

    new_document = normalize_text(new_post)

    documents.append(new_document)

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
    )

    vectors = vectorizer.fit_transform(
        documents
    )

    new_vector = vectors[-1]

    old_vectors = vectors[:-1]

    similarities = cosine_similarity(
        new_vector,
        old_vectors,
    )[0]

    return float(max(similarities))


def check_duplicate(
    post: str,
) -> tuple[bool, float]:

    history = load_history()

    if not history:
        return False, 0.0

    previous_posts = [
        item["content"]
        for item in history
        if item.get("content")
        and item.get("status")
        in {"dry_run", "published"}
    ]

    if not previous_posts:
        return False, 0.0

    highest_similarity = calculate_similarity(
        post,
        previous_posts,
    )

    is_duplicate = (
        highest_similarity
        >= DUPLICATE_THRESHOLD
    )

    print(
        "\n=============================="
    )
    print("🔍 DUPLICATE CHECK")
    print("==============================")

    print(
        f"Highest similarity: "
        f"{highest_similarity:.3f}"
    )

    print(
        f"Duplicate threshold: "
        f"{DUPLICATE_THRESHOLD:.2f}"
    )

    if is_duplicate:
        print("❌ Duplicate detected")
    else:
        print("✅ No duplicate detected")

    return (
        is_duplicate,
        highest_similarity,
    )