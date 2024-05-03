from flask import Flask, request, render_template, Response, session, redirect, url_for
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        target_text = request.form.get('target_text')

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        scraped_text = ' '.join([tag.get_text() for tag in soup.find_all(text_tags)])
        lower_case_text = scraped_text.lower()  # Convert scraped text to lowercase

        # Create a DataFrame
        df = pd.DataFrame({
            'ScrapedText': [lower_case_text],
            'TargetText': [target_text]
        })

        # Save the DataFrame to session
        session['df'] = df.to_dict()

        # Redirect to the preview route
        return redirect(url_for('preview'))

    return render_template('index.html')

@app.route('/preview', methods=['GET', 'POST'])
def preview():
    df = pd.DataFrame(session.get('df', {}))
    scraped_text = df['ScrapedText'][0] if 'ScrapedText' in df else ''

    if request.method == 'POST':
        # Update the scraped text with the edited text
        edited_text = request.form.get('edited_text')
        df['ScrapedText'][0] = edited_text
        session['df'] = df.to_dict()
        return render_template('preview.html', scraped_text=scraped_text)

    return scraped_text  # Return just the scraped text for GET requests

@app.route('/download', methods=['GET'])
def download():
    df = pd.DataFrame(session.get('df', {}))
    csv = df.to_csv(index=False)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
             "attachment; filename=dataset.csv"})

if __name__ == "__main__":
    app.run(debug=True)