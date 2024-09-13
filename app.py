from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the translation and grammar correction models
translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")  # English to French translation model
grammar_corrector = pipeline("text2text-generation", model="t5-base", task="grammar-correction")  # Grammar correction

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    user_input = request.form['user_input']
    
    # Perform translation
    translated = translator(user_input, max_length=100)[0]['translation_text']
    
    # Correct the grammar of the translation
    corrected = grammar_corrector(translated, max_length=100, num_return_sequences=1)[0]['generated_text']
    
    return jsonify({"translated": translated, "corrected": corrected})

if __name__ == '__main__':
    app.run(debug=True)
