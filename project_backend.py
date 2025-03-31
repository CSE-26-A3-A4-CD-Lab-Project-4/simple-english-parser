from flask import Flask, request, jsonify
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class LL1Parser:
    def __init__(self):
        # Define strict LL(1) grammar rules
        self.grammar = {
            "S": [["NP", "VP"]],
            "NP": [["Pronoun"], ["Article", "Noun"]],
            "VP": [["Verb"], ["Verb", "NP"]],
            "Article": [["a"], ["the"]],
            "Noun": [["dog"], ["cat"], ["book"], ["boy"], ["girl"]],
            "Verb": [["runs"], ["eats"], ["reads"], ["sleeps"], ["walks"]],
            "Pronoun": [["he"], ["she"], ["it"], ["i"]]
        }

        # Define POS mappings for classification only
        self.pos_map = {
            "PRP": "Pronoun",   # he, she, it
            "DT": "Article",    # a, the
            "NN": "Noun",       # dog, apple, book
            "NNS": "Noun",      # Added for plural nouns
            "VB": "Verb",       # eat, run, play
            "VBZ": "Verb",      # eats, runs, plays
            "VBP": "Verb",      # eat, run (present tense)
            "VBG": "Verb",      # Added for -ing forms
            "VBD": "Verb"       # Added for past tense
        }

        # Create first sets for predictive parsing
        self.first_sets = self._compute_first_sets()
        
    def _compute_first_sets(self):
        # Simplified first set computation for this basic grammar
        first_sets = {}
        # For terminals, first set is just the terminal itself
        for non_terminal, rules in self.grammar.items():
            first_sets[non_terminal] = set()
            for rule in rules:
                first_symbol = rule[0]
                if first_symbol not in self.grammar:  # It's a terminal
                    first_sets[non_terminal].add(first_symbol)
        
        # Process until no changes
        changed = True
        while changed:
            changed = False
            for non_terminal, rules in self.grammar.items():
                for rule in rules:
                    first_symbol = rule[0]
                    if first_symbol in self.grammar:  # It's a non-terminal
                        before_size = len(first_sets[non_terminal])
                        first_sets[non_terminal].update(first_sets[first_symbol])
                        if len(first_sets[non_terminal]) > before_size:
                            changed = True
        
        return first_sets

    def tag_tokens(self, tokens):
        pos_tags = pos_tag(tokens)
        result = []
        for token, tag in pos_tags:
            # Map POS tag to our grammar categories
            grammar_category = self.pos_map.get(tag, None)
            
            # If we can't map the POS tag, check if the word itself is in our terminals
            if grammar_category is None:
                for category, rules in self.grammar.items():
                    if any(rule == [token.lower()] for rule in rules):
                        grammar_category = category
                        break
            
            # If we still don't have a mapping, this token isn't in our grammar
            if grammar_category is None:
                return None
                
            result.append((token.lower(), grammar_category))
            
        return result

    def parse(self, token_info):
        if len(token_info) > 3:
            return False  # Restrict to max 3-word sentences

        tokens = [token for token, _ in token_info]
        categories = [category for _, category in token_info]
        
        # Initialize parsing
        stack = ["$", "S"]  # Start with end marker and start symbol
        input_buffer = tokens + ["$"]  # Add end marker to input
        input_categories = categories + ["$"]
        input_index = 0
        
        while stack[-1] != "$":  # Continue until we've processed everything
            top = stack[-1]
            current_token = input_buffer[input_index]
            current_category = input_categories[input_index]
            
            # If top of stack is a terminal
            if top not in self.grammar:
                if top == current_token:
                    stack.pop()
                    input_index += 1
                else:
                    return False  # Mismatch - parsing fails
            else:  # Top of stack is a non-terminal
                # Find matching production rule
                matching_rule = None
                for rule in self.grammar[top]:
                    first_symbol = rule[0]
                    
                    # Direct match with token
                    if first_symbol == current_token:
                        matching_rule = rule
                        break
                    
                    # Match with category
                    if first_symbol == current_category:
                        matching_rule = rule
                        break
                    
                    # Check first sets for non-terminals
                    if first_symbol in self.grammar and current_token in self.first_sets[first_symbol]:
                        matching_rule = rule
                        break
                
                if matching_rule:
                    stack.pop()  # Remove the non-terminal
                    # Push production in reverse order
                    for symbol in reversed(matching_rule):
                        if symbol != "ε":  # Skip empty productions
                            stack.append(symbol)
                else:
                    return False  # No matching rule
                    
        # Parse successful if we've consumed all input
        return input_index == len(input_buffer) - 1

@app.route('/check', methods=['POST'])
def check_grammar():
    data = request.get_json()
    sentence = data.get("sentence", "").lower()
    tokens = word_tokenize(sentence)

    parser = LL1Parser()
    token_info = parser.tag_tokens(tokens)
    
    if not token_info:
        return jsonify({
            "sentence": sentence, 
            "valid": False, 
            "error": "Unknown word structure or words not in grammar"
        })

    result = parser.parse(token_info)
    return jsonify({"sentence": sentence, "valid": result})

if __name__ == '__main__':
    app.run(debug=True, port=5002)