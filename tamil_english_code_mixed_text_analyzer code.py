
import re
import html
import unicodedata
from typing import List, Dict, Tuple, Any

# ==============================================================================
# MODULE 1: DATA ENGINEERING & PREPROCESSING PIPELINE
# ==============================================================================

# Extended Tanglish Colloquial Lexicon & Phonetic Harmonization Lookup
TANGLISH_LEXICON: Dict[str, Dict[str, Any]] = {
    # Positive / Appreciative
    "semma": {"lang": "ta", "pos": "ADJ", "polarity": 1.0, "canonical": "semma"},
    "semaya": {"lang": "ta", "pos": "ADJ", "polarity": 1.0, "canonical": "semma"},
    "mass": {"lang": "en", "pos": "ADJ", "polarity": 0.9, "canonical": "mass"},
    "vera": {"lang": "ta", "pos": "ADJ", "polarity": 0.5, "canonical": "vera"},
    "level": {"lang": "en", "pos": "NOUN", "polarity": 0.5, "canonical": "level"},
    "super": {"lang": "en", "pos": "ADJ", "polarity": 0.8, "canonical": "super"},
    "thalaiva": {"lang": "ta", "pos": "NOUN", "polarity": 0.7, "canonical": "thalaivar"},
    "thalaivar": {"lang": "ta", "pos": "NOUN", "polarity": 0.7, "canonical": "thalaivar"},
    "nalla": {"lang": "ta", "pos": "ADJ", "polarity": 0.8, "canonical": "nalla"},
    "nallaa": {"lang": "ta", "pos": "ADJ", "polarity": 0.8, "canonical": "nalla"},
    "alagu": {"lang": "ta", "pos": "ADJ", "polarity": 0.8, "canonical": "azhagu"},
    "azhagu": {"lang": "ta", "pos": "ADJ", "polarity": 0.8, "canonical": "azhagu"},
    "veri": {"lang": "ta", "pos": "NOUN", "polarity": 0.8, "canonical": "veri"},
    "marana": {"lang": "ta", "pos": "ADJ", "polarity": 0.8, "canonical": "marana"},
    "theri": {"lang": "ta", "pos": "ADJ", "polarity": 0.8, "canonical": "theri"},
    "vetri": {"lang": "ta", "pos": "NOUN", "polarity": 0.8, "canonical": "vetri"},
    "pudichirukku": {"lang": "ta", "pos": "VERB", "polarity": 0.9, "canonical": "pidithirukirathu"},
    "pidichirukku": {"lang": "ta", "pos": "VERB", "polarity": 0.9, "canonical": "pidithirukirathu"},
    
    # Negative / Critical
    "waste": {"lang": "en", "pos": "ADJ", "polarity": -0.9, "canonical": "waste"},
    "mokkai": {"lang": "ta", "pos": "ADJ", "polarity": -0.9, "canonical": "mokkai"},
    "mokka": {"lang": "ta", "pos": "ADJ", "polarity": -0.9, "canonical": "mokkai"},
    "worst": {"lang": "en", "pos": "ADJ", "polarity": -1.0, "canonical": "worst"},
    "bore": {"lang": "en", "pos": "ADJ", "polarity": -0.7, "canonical": "bore"},
    "kevalam": {"lang": "ta", "pos": "ADJ", "polarity": -0.9, "canonical": "kevalam"},
    "lag": {"lang": "en", "pos": "NOUN", "polarity": -0.6, "canonical": "lag"},
    "thalaivali": {"lang": "ta", "pos": "NOUN", "polarity": -0.8, "canonical": "thalaivali"},
    "karumam": {"lang": "ta", "pos": "NOUN", "polarity": -0.9, "canonical": "karumam"},
    "disappointing": {"lang": "en", "pos": "ADJ", "polarity": -0.8, "canonical": "disappointing"},
    "pudikala": {"lang": "ta", "pos": "VERB", "polarity": -0.9, "canonical": "pidikavillai"},
    "pidikala": {"lang": "ta", "pos": "VERB", "polarity": -0.9, "canonical": "pidikavillai"},
    
    # Connectives & Structural / Neutral
    "padam": {"lang": "ta", "pos": "NOUN", "polarity": 0.0, "canonical": "padam"},
    "movie": {"lang": "en", "pos": "NOUN", "polarity": 0.0, "canonical": "movie"},
    "cinemava": {"lang": "ta", "pos": "NOUN", "polarity": 0.0, "canonical": "cinema"},
    "acting": {"lang": "en", "pos": "NOUN", "polarity": 0.0, "canonical": "acting"},
    "nadippu": {"lang": "ta", "pos": "NOUN", "polarity": 0.0, "canonical": "nadippu"},
    "bgm": {"lang": "en", "pos": "NOUN", "polarity": 0.2, "canonical": "bgm"},
    "music": {"lang": "en", "pos": "NOUN", "polarity": 0.1, "canonical": "music"},
    "isai": {"lang": "ta", "pos": "NOUN", "polarity": 0.1, "canonical": "isai"},
    "director": {"lang": "en", "pos": "NOUN", "polarity": 0.0, "canonical": "director"},
    "direction": {"lang": "en", "pos": "NOUN", "polarity": 0.0, "canonical": "direction"},
    "iyakkunar": {"lang": "ta", "pos": "NOUN", "polarity": 0.0, "canonical": "iyakkunar"},
    "climax": {"lang": "en", "pos": "NOUN", "polarity": 0.0, "canonical": "climax"},
    "song": {"lang": "en", "pos": "NOUN", "polarity": 0.0, "canonical": "song"},
    "paattu": {"lang": "ta", "pos": "NOUN", "polarity": 0.0, "canonical": "paattu"},
    "pattu": {"lang": "ta", "pos": "NOUN", "polarity": 0.0, "canonical": "paattu"},
    "hero": {"lang": "en", "pos": "NOUN", "polarity": 0.1, "canonical": "hero"},
    "heroine": {"lang": "en", "pos": "NOUN", "polarity": 0.1, "canonical": "heroine"},
    "trailer": {"lang": "en", "pos": "NOUN", "polarity": 0.0, "canonical": "trailer"},
    "story": {"lang": "en", "pos": "NOUN", "polarity": 0.0, "canonical": "story"},
    "kadhai": {"lang": "ta", "pos": "NOUN", "polarity": 0.0, "canonical": "kadhai"},
    "screenplay": {"lang": "en", "pos": "NOUN", "polarity": 0.0, "canonical": "screenplay"},
    "theatre": {"lang": "en", "pos": "NOUN", "polarity": 0.0, "canonical": "theatre"},
    "bro": {"lang": "en", "pos": "NOUN", "polarity": 0.1, "canonical": "bro"},
    "nanba": {"lang": "ta", "pos": "NOUN", "polarity": 0.3, "canonical": "nanba"},
    "thambi": {"lang": "ta", "pos": "NOUN", "polarity": 0.2, "canonical": "thambi"},
    "aana": {"lang": "ta", "pos": "CONJ", "polarity": 0.0, "canonical": "aanal"},
    "aanal": {"lang": "ta", "pos": "CONJ", "polarity": 0.0, "canonical": "aanal"},
    "but": {"lang": "en", "pos": "CONJ", "polarity": 0.0, "canonical": "but"},
    "and": {"lang": "en", "pos": "CONJ", "polarity": 0.0, "canonical": "and"},
    "romba": {"lang": "ta", "pos": "ADV", "polarity": 0.0, "canonical": "romba"},
    "migavum": {"lang": "ta", "pos": "ADV", "polarity": 0.0, "canonical": "migavum"},
    "konjam": {"lang": "ta", "pos": "ADV", "polarity": 0.0, "canonical": "konjam"},
    "irukku": {"lang": "ta", "pos": "VERB", "polarity": 0.0, "canonical": "irukirathu"},
    "aachu": {"lang": "ta", "pos": "VERB", "polarity": 0.0, "canonical": "aanathu"},
    "varum": {"lang": "ta", "pos": "VERB", "polarity": 0.0, "canonical": "varum"},
    "kuda": {"lang": "ta", "pos": "ADV", "polarity": 0.0, "canonical": "kooda"},
    "than": {"lang": "ta", "pos": "PART", "polarity": 0.0, "canonical": "thaan"},
    "dhan": {"lang": "ta", "pos": "PART", "polarity": 0.0, "canonical": "thaan"},
    "paathen": {"lang": "ta", "pos": "VERB", "polarity": 0.0, "canonical": "paarthen"},
    "paarthein": {"lang": "ta", "pos": "VERB", "polarity": 0.0, "canonical": "paarthen"},
}

# Emoji to Polarity & Semantic Word Mapping
EMOJI_SENTIMENT_MAP: Dict[str, Tuple[float, str]] = {
    "🔥": (0.9, "fire_mass"),
    "❤️": (0.9, "love_heart"),
    "😍": (0.9, "adore"),
    "👏": (0.7, "applause"),
    "👍": (0.6, "thumbs_up"),
    "💯": (0.9, "hundred_perfect"),
    "😂": (0.4, "laughing"),
    "🤣": (0.4, "rolling_laughing"),
    "😭": (-0.5, "crying"),
    "😡": (-0.9, "angry"),
    "🤬": (-1.0, "furious"),
    "🤮": (-1.0, "disgusted"),
    "👎": (-0.8, "thumbs_down"),
    "💔": (-0.9, "heartbreak"),
    "🥱": (-0.7, "boring_yawn"),
    "😴": (-0.6, "sleeping_bore"),
}

COMMON_ENGLISH_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "this", "that", "it", "they",
    "good", "bad", "great", "nice", "awesome", "terrible", "worst", "best",
    "in", "on", "at", "to", "for", "with", "from", "by", "about", "like",
    "watch", "watched", "see", "seen", "time", "one", "first", "second",
    "acting", "direction", "music", "bgm", "scenes", "story", "screenplay",
    "climax", "interval", "entry", "fight", "dance", "comedy", "dialogue"
}


def clean_text(raw_text: str) -> str:
    """Removes URLs, mentions, decodes HTML entities, and strips stray noise."""
    if not isinstance(raw_text, str):
        return ""
    text = html.unescape(raw_text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)      # Strip URLs
    text = re.sub(r"@[\w_]+", "", text)                     # Strip @mentions
    text = re.sub(r"#([\w_]+)", r"\1", text)                # Extract hashtag text
    text = re.sub(r"[\r\n\t]+", " ", text)                  # Collapse newlines
    return text.strip()


def normalize_elongations(text: str) -> str:
    """
    Collapses repeated characters (3 or more down to 2).
    Example: 'semmaaaaa' -> 'semmaa', 'massssss' -> 'mass'
    """
    return re.sub(r"(.)\1{2,}", r"\1\1", text)


def is_native_tamil(text: str) -> bool:
    """Checks whether token contains Unicode characters from the Tamil block (U+0B80 - U+0BFF)."""
    return any("\u0B80" <= ch <= "\u0BFF" for ch in text)


# ==============================================================================
# MODULE 2: TOKEN-LEVEL LANGUAGE IDENTIFICATION & CMI CALCULATION
# ==============================================================================

def identify_token_language(token: str) -> str:
    """
    Identifies the language of an individual token:
      - 'ta-Taml': Native Tamil Unicode script
      - 'ta-Latn': Romanized Tamil (Tanglish)
      - 'en': English
      - 'univ': Universal (Punctuation, Numbers, Emojis)
    """
    clean_tok = re.sub(r"[^\w\s]", "", token).strip().lower()
    if not clean_tok or clean_tok.isnumeric():
        return "univ"

    # Native script check
    if is_native_tamil(token):
        return "ta-Taml"

    # Lexicon lookup
    if clean_tok in TANGLISH_LEXICON:
        lex_lang = TANGLISH_LEXICON[clean_tok]["lang"]
        return "ta-Latn" if lex_lang == "ta" else "en"

    # Common English words
    if clean_tok in COMMON_ENGLISH_WORDS:
        return "en"

    # Heuristic Morphological Tanglish Indicators
    tanglish_suffixes = ("nga", "gal", "um", "oda", "ku", "la", "aachu", "iruku", "dhan", "than", "pa")
    tanglish_prefixes = ("marana", "thala", "kola", "keda")
    if any(clean_tok.endswith(suf) for suf in tanglish_suffixes) or any(clean_tok.startswith(pre) for pre in tanglish_prefixes):
        return "ta-Latn"

    # Fallback default: English if alphabetic
    return "en" if clean_tok.isalpha() else "univ"


def calculate_cmi(tokens: List[str]) -> Tuple[float, Dict[str, int]]:
    """
    Computes Gambäck & Das (FIRE Benchmark) Code-Mixing Index (CMI):
      CMI = 100 * [1 - (max(w_en, w_ta) / (n - u))]   if (n - u) > 0 else 0
    where:
      n = total tokens
      u = universal/punctuation tokens
      w_en = English word count
      w_ta = Tamil (Tanglish + Native) word count
    """
    counts = {"en": 0, "ta": 0, "univ": 0}
    for tok in tokens:
        lang = identify_token_language(tok)
        if lang in ("ta-Latn", "ta-Taml"):
            counts["ta"] += 1
        elif lang == "en":
            counts["en"] += 1
        else:
            counts["univ"] += 1

    n = len(tokens)
    u = counts["univ"]
    lang_tokens = n - u

    if lang_tokens <= 0:
        cmi = 0.0
    else:
        max_dominant = max(counts["en"], counts["ta"])
        cmi = 100.0 * (1.0 - (max_dominant / lang_tokens))

    return round(cmi, 2), counts


# ==============================================================================
# MODULE 3: SENTIMENT & POLARITY PREDICTION ENGINE
# ==============================================================================

class CodeMixedSentimentAnalyzer:
    """
    Multi-Class Sentiment Classification Engine tailored for Tamil-English text.
    Handles contrastive conjunctions ('but', 'aana') and emoji polarity amplification.
    """

    def __init__(self):
        self.classes = ["Positive", "Negative", "Neutral", "Mixed_Feelings"]

    def analyze(self, text: str) -> Dict[str, Any]:
        cleaned = clean_text(text)
        normalized = normalize_elongations(cleaned)
        
        # Tokenize (words and emojis preserved)
        raw_tokens = re.findall(r"[\w']+|[^\w\s]", normalized)
        word_tokens = [tok for tok in raw_tokens if any(c.isalnum() for c in tok)]

        token_analyses = []
        sentiment_scores = []
        positive_evidence = 0
        negative_evidence = 0

        # Scan for contrastive discourse markers ('but', 'aana', 'aanal')
        has_contrastive = False
        contrastive_indices = []

        for idx, tok in enumerate(raw_tokens):
            lower_tok = tok.lower()
            lang = identify_token_language(tok)
            polarity = 0.0

            # Emoji check
            if tok in EMOJI_SENTIMENT_MAP:
                polarity, sem_tag = EMOJI_SENTIMENT_MAP[tok]
                lang = "emoji"
            elif lower_tok in TANGLISH_LEXICON:
                polarity = TANGLISH_LEXICON[lower_tok]["polarity"]
            elif lower_tok in ("good", "great", "nice", "awesome", "best", "fire"):
                polarity = 0.8
            elif lower_tok in ("bad", "terrible", "worst", "hate", "boring", "waste"):
                polarity = -0.8

            if lower_tok in ("but", "aana", "aanal"):
                has_contrastive = True
                contrastive_indices.append(idx)

            if polarity > 0.1:
                positive_evidence += 1
            elif polarity < -0.1:
                negative_evidence += 1

            sentiment_scores.append(polarity)
            token_analyses.append({
                "token": tok,
                "language": lang,
                "polarity": polarity
            })

        # Calculate Code Mixing Index
        cmi_score, lang_counts = calculate_cmi(word_tokens)

        # Compute aggregate sentiment orientation
        total_polarity = sum(sentiment_scores)
        n_tokens = max(len(word_tokens), 1)
        normalized_polarity = total_polarity / n_tokens

        # Determine Classification
        if positive_evidence > 0 and negative_evidence > 0 and (has_contrastive or abs(positive_evidence - negative_evidence) <= 1):
            prediction = "Mixed_Feelings"
            conf = 0.85
        elif normalized_polarity >= 0.15:
            prediction = "Positive"
            conf = min(0.60 + abs(normalized_polarity) * 0.4, 0.98)
        elif normalized_polarity <= -0.15:
            prediction = "Negative"
            conf = min(0.60 + abs(normalized_polarity) * 0.4, 0.98)
        else:
            prediction = "Neutral"
            conf = 0.70

        # Build class probability distribution
        probs = {c: 0.05 for c in self.classes}
        probs[prediction] = conf
        remaining = 1.0 - conf
        other_classes = [c for c in self.classes if c != prediction]
        for c in other_classes:
            probs[c] = round(remaining / len(other_classes), 3)
        probs[prediction] = round(1.0 - sum(probs[c] for c in other_classes), 3)

        return {
            "input_text": text,
            "cleaned_text": normalized,
            "prediction": prediction,
            "confidence": conf,
            "probabilities": probs,
            "cmi_score": cmi_score,
            "language_breakdown": lang_counts,
            "token_details": token_analyses,
            "has_mixed_signals": has_contrastive or (positive_evidence > 0 and negative_evidence > 0)
        }


# ==============================================================================
# MODULE 4: THEMATIC KEYWORD & TOPIC EXTRACTION
# ==============================================================================

THEMATIC_CATEGORIES = {
    "Acting / Performance": ["acting", "nadippu", "hero", "heroine", "thalaivar", "mass", "screen"],
    "Music / BGM": ["bgm", "music", "isai", "song", "paattu", "songs", "soundtrack"],
    "Direction & Screenplay": ["director", "direction", "screenplay", "story", "kadhai", "climax", "lag"],
    "Visuals / Cinematography": ["visuals", "cinematography", "vfx", "camera", "frame", "fire", "shot"],
    "General Appreciation / Critique": ["padam", "movie", "theatre", "trailer", "super", "waste", "mokka"]
}

def extract_topics(text: str) -> List[str]:
    """Identifies key topical aspects present in the code-mixed comment."""
    lower_text = text.lower()
    matched_topics = []
    for category, keywords in THEMATIC_CATEGORIES.items():
        if any(kw in lower_text for kw in keywords):
            matched_topics.append(category)
    return matched_topics if matched_topics else ["General Discussion"]


# ==============================================================================
# DEMONSTRATION & TEST HARNESS
# ==============================================================================

def run_demonstration():
    """Runs the analyzer on diverse real-world Tamil-English social media sentences."""
    analyzer = CodeMixedSentimentAnalyzer()

    test_samples = [
        "Padam semma mass bro, fire visuals and BGM vera level! 🔥❤️",
        "Second half romba lag aachu, story is total waste and worst climax...",
        "First half semma super entertainment, but second half konjam bore mokka.",
        "Trailer release date eppo varum nanba? Waiting for update!",
        "Thalaivar acting marana mass, anirudh bgm theri mass hits 💯",
        "Padam average than bro, one time watchable for comedy scenes."
    ]

    print("=" * 85)
    print(" TAMIL-ENGLISH CODE-MIXED TEXT ANALYZER (Tanglish NLP)")
    print(" Candidate: REYASH V (23UAI090) | Sri Manakula Vinayagar Engineering College")
    print("=" * 85)

    for i, sample in enumerate(test_samples, 1):
        result = analyzer.analyze(sample)
        topics = extract_topics(sample)

        print(f"\n[SAMPLE {i}]: \"{sample}\"")
        print(f"  -> Prediction   : {result['prediction']} (Confidence: {result['confidence']*100:.1f}%)")
        print(f"  -> CMI Score    : {result['cmi_score']}% (Code-Mixing Index)")
        print(f"  -> Language Mix : English={result['language_breakdown']['en']}, "
              f"Tamil={result['language_breakdown']['ta']}, Univ={result['language_breakdown']['univ']}")
        print(f"  -> Topics       : {', '.join(topics)}")
        print(f"  -> Probabilities: {result['probabilities']}")
        
        # Token inspection table
        token_str = " ".join([f"{t['token']}[{t['language']}]" for t in result['token_details'] if t['language'] != 'univ'])
        print(f"  -> Tokens Tagged: {token_str}")
        print("-" * 85)


if __name__ == "__main__":
    run_demonstration()
