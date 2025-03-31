# LL(1) Simple English Parser with Frontend
This is an implementation of an LL(1) parser in Python to validate simple English sentences against a predefined grammar. The parser is wrapped in a Flask API that can be used to check if sentences conform to the grammar rules. The Frontend for the project is a webpage which uses HTML and CSS for the design, and JavaScript for the API Calls. It features a minimal design.

## Features

- LL(1) parsing algorithm for context-free grammar validation
- Support for simple English sentences (up to 3 words)
- REST API endpoint for grammar checking
- POS (Part of Speech) tagging using NLTK
- CORS support for cross-origin requests
- Webpage with a minimal design written in HTML, CSS and JavaScript for the frontend.

## Grammar Rules

The parser implements the following grammar:

```
S → NP VP
NP → Pronoun | Article Noun
VP → Verb | Verb NP
```

With terminals:
- Pronouns: he, she, it, I
- Articles: a, the
- Nouns: dog, cat, book
- Verbs: runs, eats, reads

## Requirements

- Python 3.6+
- Flask
- NLTK
- Flask-CORS

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/CSE-26-A3-A4-CD-Lab-Project-4/simple-english-parser.git
   cd ll1-parser
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install flask nltk flask-cors
   ```

4. Download NLTK data:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('averaged_perceptron_tagger')
   ```

## Usage

1. Start the Flask server:
   ```
   python project_backend.py
   ```

   The server will start on `http://localhost:5002`

2. Open the `index.html` in a web browser.
3. Enter sentence in the given field and click on "Check Grammar" button.
4. The result of the parsing would be displayed below the button.


## Examples of Valid Sentences

- "He runs"
- "She reads"
- "The dog runs"
- "A cat eats"
- "He reads a book"
- "The dog eats a cat"

## Limitations

- Only supports sentences up to 3 words long
- Limited vocabulary defined in the grammar
- Does not handle complex grammatical structures
- No support for verb tenses or conjugations beyond the defined terminals

## Extending the Parser

To add support for more words or grammar rules, modify the `grammar` and `pos_map` dictionaries in the `LL1Parser` class in the Python file.
