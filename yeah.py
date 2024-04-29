from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import filedialog
from tkinter import Tk

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    scraped_text = ''
    if request.method == 'POST':
        url = request.form.get('url')
        target_text = request.form.get('target_text')
        auto_save = request.form.get('auto_save')  # This should be a checkbox in your form

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        scraped_text = ' '.join([tag.get_text() for tag in soup.find_all(text_tags)])
        lower_case_text = scraped_text.lower()  # Convert scraped text to lowercase

        if target_text:
            # Create a DataFrame
            df = pd.DataFrame({
                'ScrapedText': [lower_case_text],
                'TargetText': [target_text]
            })

            if auto_save:
                # Save the DataFrame to a CSV file
                df.to_csv('dataset.csv', index=False)
            else:
                # Open a file dialog to select the save location
                root = Tk()
                root.withdraw()  # Hide the main window
                file_path = filedialog.asksaveasfilename(defaultextension='.csv')
                df.to_csv(file_path, index=False)

    return render_template('index.html', scraped_text=scraped_text)

if __name__ == "__main__":
    app.run(debug=True)