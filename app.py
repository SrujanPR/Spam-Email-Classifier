from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

# Train model
df = pd.read_csv("spam.csv", encoding='ISO-8859-1')[['v1', 'v2']]
df.columns = ['label', 'text']
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

X = df['text']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('model', MultinomialNB())
])

pipeline.fit(X_train, y_train)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        subject = request.form["subject"]
        prediction = pipeline.predict([subject])
        session['result'] = "Spam" if prediction[0] == 1 else "Not Spam"
        return redirect(url_for('index'))  # Redirect after POST

    result = session.pop('result', None)  # Only show once
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
