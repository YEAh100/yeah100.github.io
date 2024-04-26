from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route('/scrape_and_extract', methods=['POST'])
def scrape_and_extract():
    url = request.json['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join(soup.stripped_strings)
    doc = nlp(text)
    entities = {ent.text: ent.label_ for ent in doc.ents}
    return jsonify(entities)

if __name__ == '__main__':
    app.run(port=42251)