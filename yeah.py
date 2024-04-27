from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        scraped_text = ' '.join([tag.get_text() for tag in soup.find_all(text_tags)])
        return render_template('index.html', scraped_text=scraped_text)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)