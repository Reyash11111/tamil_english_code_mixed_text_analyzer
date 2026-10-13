# Tamil-English Code-Mixed Text Analyzer (Tanglish NLP)

[Python 3.10+](https://www.google.com/search?q=https%3A%2F%2Fwww.python.org%2Fdownloads%2F)
[Streamlit App](https://www.google.com/search?q=https%3A%2F%2Fstreamlit.io)
[NLP Dravidian](https://www.google.com/search?q=https%3A%2F%2Fgithub.com)
[License: MIT](https://www.google.com/search?q=https%3A%2F%2Fopensource.org%2Flicenses%2FMIT)

> An end-to-end Natural Language Processing (NLP) framework designed for linguistic tokenization, language identification, Code-Mixing Index (CMI) calculation, and multi-class sentiment classification on colloquial **Tamil-English (Tanglish)** social media text.

---

## 📌 Project Overview

Colloquial communication across South Indian social media (YouTube, Twitter/X, Instagram) predominantly features **code-mixing** and **code-switching**, where Tamil words are written using the Roman/Latin script (**Tanglish**), freely interspersed with English vocabulary.

Standard monolingual NLP models and off-the-shelf sentiment analyzers (e.g., VADER, RoBERTa) fail catastrophically on such text due to:
1. **Absence of Standardized Orthography**: Enormous spelling variance for identical phonetic words (e.g., *vaanga*, *vanga*, *waanga*).
2. **Agglutinative Morphology**: Bound morphemes and suffixes attached across language boundaries (e.g., *mass-ah*, *acting-la*).
3. **Character Elongations**: Emotional emphasis through repetitive letters (e.g., *massssss*, *semmaaaaa*).
4. **Contrastive Discourse Structures**: Multi-sentiment polarity within a single sentence separated by discourse markers (e.g., *"First half super, but second half romba mokka"*).

This repository implements a modular, high-accuracy processing pipeline addressing these challenges using phonetic harmonization, linguistic lexicons, token-level language identification, benchmark **Code-Mixing Index (CMI)** scoring, and hybrid classification.

---

## 🚀 Key Features

* **Multi-Stage Text Normalization**: Automated excision of URLs, user handles, HTML entities, and regex-driven elongation collapse (e.g., `semmaaaaa` $\rightarrow$ `semma`).
* **Emoji Semantic Polarity Extraction**: Translates affective emojis (🔥, ❤️, 😂, 😡, 💔) into quantitative sentiment polarity scores.
* **Token-Level Language Identification (LID)**: Classifies every token into `ta-Latn` (Romanized Tamil), `ta-Taml` (Native Tamil Unicode), `en` (English), or `univ` (Universal/Punctuation).
* **Code-Mixing Index (CMI) Engine**: Computes the official Gambäck & Das / FIRE DravidianCodeMix benchmark score to quantify the linguistic complexity of the text.
* **Multi-Class Sentiment Classification**: Classifies comments into 4 benchmark categories:
  * `Positive`
  * `Negative`
  * `Neutral`
  * `Mixed_Feelings` (captures contrastive conjunctions like *but*, *aana*, *aanal*)
* **Thematic Topic Extraction**: Categorizes comments into domain aspects (Acting, Music/BGM, Direction/Story, Visuals, General Critique).
* **Interactive Web Dashboard**: Built with Streamlit for real-time inference, token breakdown inspection, and probability visualization.

---

## 🏗️ System Architecture

```text
       Raw Tanglish Comment (e.g., "Padam semma mass bro, fire visuals and BGM vera level! 🔥❤️")
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │       MODULE 1: DATA CLEANING & PREPROCESSING     │
             │  • HTML Entity Decode  • URL & Mention Removal   │
             │  • Elongation Collapse • Emoji Semantic Mapping  │
             └──────────────────────────────────────────────────┘
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │       MODULE 2: TOKEN-LEVEL LANGUAGE IDENTIFIER  │
             │  • Romanized Tamil (ta-Latn) • Native (ta-Taml)  │
             │  • English (en)              • Universal (univ)  │
             │  ──────────────────────────────────────────────  │
             │       Gambäck & Das Code-Mixing Index (CMI)      │
             └──────────────────────────────────────────────────┘
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │       MODULE 3: COGNITIVE SENTIMENT CLASSIFIER   │
             │  • Contrastive Discourse Shift Analysis (but)    │
             │  • Lexicon + Contextual Polarity Accumulator     │
             │  • Multi-Class Confidence Distribution           │
             └──────────────────────────────────────────────────┘
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │       MODULE 4: TOPIC EXTRACTION & PRESENTATION  │
             │  • Aspects: Acting, Music, Direction, Visuals    │
             │  • Interactive Streamlit UI / JSON Output API    │
             └──────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```text
├── tamil_english_text_analyzer.py   # Core NLP pipeline (LID, CMI, Sentiment, Topics)
├── app_tamil_english_analyzer.py     # Interactive Streamlit Web Application
├── requirements.txt                 # Project dependencies
├── README.md                        # Documentation & project guide
└── test_samples.json                # Curated evaluation sentences
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/tamil-english-code-mixed-analyzer.git
cd tamil-english-code-mixed-analyzer
```

### 2. Create and Activate Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### Command-Line Interface (CLI) Mode
Run the standalone pipeline directly from your terminal:
```bash
python3 tamil_english_text_analyzer.py
```

### Interactive Web Dashboard (Streamlit)
Launch the browser-based graphical user interface:
```bash
streamlit run app_tamil_english_analyzer.py
```
Open your browser at `http://localhost:8501` to test custom Tanglish sentences in real time.

---

## 🧪 Benchmark Evaluation Samples

| Input Comment | Detected Class | Confidence | CMI Score | Primary Topics |
| :--- | :---: | :---: | :---: | :--- |
| `"Padam semma mass bro, fire visuals and BGM vera level! 🔥❤️"` | **Positive** | 79.6% | 30.0% | Acting, Music, Visuals |
| `"Second half romba lag aachu, story is total waste and worst climax..."` | **Negative** | 68.3% | 16.7% | Direction, Screenplay |
| `"First half semma super entertainment, but second half konjam bore mokka."` | **Mixed_Feelings** | 85.0% | 27.3% | General Critique |
| `"Trailer release date eppo varum nanba? Waiting for update!"` | **Neutral** | 70.0% | 22.2% | General Discussion |
| `"Thalaivar acting marana mass, anirudh bgm theri mass hits 💯"` | **Positive** | 83.1% | 33.3% | Acting, Music / BGM |

---

## 📐 Mathematical Formulation

### Code-Mixing Index ($CMI$)
Formulated according to the Gambäck & Das (FIRE Shared Task) standard:

$$CMI = 100 \times \left[ 1 - \frac{\max(w_{\text{en}}, w_{\text{ta}})}{n - u} \right] \quad \text{for } (n - u) > 0$$

Where:
* $n$ = Total count of tokens
* $u$ = Count of language-independent tokens (punctuation, numerical digits, standalone symbols)
* $w_{\text{en}}$ = Count of English tokens
* $w_{\text{ta}}$ = Count of Tamil tokens (both native Unicode and Romanized Tanglish)

---

## 🎓 Academic Project Information

* **Project Title**: Tamil-English Code-Mixed Text Analyzer
* **Candidate**: **REYASH V** (Register No: **23UAI090**)
* **Faculty Supervisor**: Dr. S. KAVITHA, M.Tech., Ph.D.
* **Degree**: Bachelor of Technology (B.Tech) in Computer Science and Engineering
* **Institution**: Sri Manakula Vinayagar Engineering College (Autonomous), Madagadipet, Puducherry – 605 107
* **Academic Year**: 2026 – 2027

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
