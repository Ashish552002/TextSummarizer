import math
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Auto-download required resources
for resource in ["punkt", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        nltk.download(resource)


def analyze_article(text: str, max_sentences: int = 3):
    """
    Returns a dictionary with:
      - summary
      - topic
      - crux
    """
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < 50:
        return {"summary": text, "topic": text, "crux": text}

    sentences = sent_tokenize(text)
    words = [w.lower() for w in word_tokenize(text) if re.match(r"[A-Za-z0-9']+", w)]

    stopwords = set(
        "a an and are as at be by for from has have in is it its of on or that the to was were will with this these those their them they he she you your i we our not but if then into over under also more most such can may might should could would than while do does did done".split()
    )

    freq = {}
    for w in words:
        if w not in stopwords:
            freq[w] = freq.get(w, 0) + 1

    # Score sentences
    scores = []
    for idx, sent in enumerate(sentences):
        tokenized = [t.lower() for t in word_tokenize(sent) if re.match(r"[A-Za-z0-9']+", t)]
        if not tokenized:
            continue
        score = sum(freq.get(t, 0) for t in tokenized) / math.sqrt(len(tokenized))
        scores.append((idx, score))

    if not scores:
        return {"summary": text, "topic": "Unknown", "crux": text}

    # Sort by score
    scores.sort(key=lambda x: x[1], reverse=True)

    # --- Topic ---
    top_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:3]
    topic = " ".join([w.capitalize() for w, _ in top_keywords])

    # --- Crux ---
    crux = sentences[scores[0][0]]

    # --- Summary ---
    selected_idx = sorted([i for i, _ in scores[:max_sentences]])
    summary = " ".join(sentences[i] for i in selected_idx)

    return {"summary": summary, "topic": topic, "crux": crux}
