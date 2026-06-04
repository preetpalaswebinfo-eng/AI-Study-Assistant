from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import os
from pypdf import PdfReader

app = Flask(__name__)

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")   

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if request.method == 'POST':
        username = request.form['username']
    else:
        username = "Preet"

    return render_template(
        'dashboard.html',
        username=username
    )
@app.route('/chat', methods=['GET', 'POST'])
def chat():

    answer = ""

    if request.method == 'POST':

        question = request.form['question']

        try:
            response = model.generate_content(question)
            answer = response.text

        except Exception as e:
            answer = f"Error: {str(e)}"

    return render_template('chat.html', answer=answer)

@app.route('/summarizer', methods=['GET', 'POST'])
def summarizer():

    summary = ""

    if request.method == 'POST':

        notes = request.form['notes']

        prompt = f"Summarize the following notes in simple points:\n\n{notes}"

        try:
            response = model.generate_content(prompt)
            summary = response.text

        except Exception as e:
            summary = f"Error: {str(e)}"

    return render_template('summarizer.html', summary=summary)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():

    quiz_result = ""

    if request.method == 'POST':

        topic = request.form['topic']

        prompt = f"""
        Generate 5 multiple choice questions about {topic}.

        Format:
        Question
        A)
        B)
        C)
        D)

        Correct Answer:
        """

        try:
            response = model.generate_content(prompt)
            quiz_result = response.text

        except Exception as e:
            quiz_result = f"Error: {str(e)}"

    return render_template('quiz.html', quiz_result=quiz_result)

@app.route('/planner', methods=['GET', 'POST'])
def planner():

    plan = ""

    if request.method == 'POST':

        subject = request.form['subject']
        hours = request.form['hours']

        prompt = f"""
        Create a detailed weekly study plan for {subject}.

        Study time available: {hours} hours per day.

        Give a day-wise study schedule from Monday to Sunday.
        """

        try:
            response = model.generate_content(prompt)
            plan = response.text

        except Exception as e:
            plan = f"Error: {str(e)}"

    return render_template('planner.html', plan=plan)

@app.route('/pdf_analyzer', methods=['GET', 'POST'])
def pdf_analyzer():

    summary = ""

    if request.method == 'POST':

        pdf_file = request.files['pdf']

        file_path = os.path.join("uploads", pdf_file.filename)

        pdf_file.save(file_path)

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text()

        prompt = f"""
        Analyze these notes and provide:

        1. Summary
        2. Important Points
        3. Possible Exam Questions

        Notes:
        {text}
        """

        try:
            response = model.generate_content(prompt)
            summary = response.text

        except Exception as e:
            summary = str(e)

    return render_template(
        'pdf_analyzer.html',
        summary=summary
    )

@app.route('/flashcards', methods=['GET', 'POST'])
def flashcards():

    flashcards = ""

    if request.method == 'POST':

        topic = request.form['topic']

        prompt = f"""
        Create 10 study flashcards for the topic: {topic}

        Format:

        Q: Question
        A: Answer

        Keep answers short and easy to remember.
        """

        try:
            response = model.generate_content(prompt)
            flashcards = response.text

        except Exception as e:
            flashcards = str(e)

    return render_template(
        'flashcards.html',
        flashcards=flashcards
    )

@app.route('/career', methods=['GET', 'POST'])
def career():

    career_result = ""

    if request.method == 'POST':

        interest = request.form['interest']

        prompt = f"""
        A student is interested in: {interest}

        Suggest:

        1. Suitable Career Paths
        2. Required Skills
        3. Recommended Courses
        4. Future Opportunities

        Give the answer in simple points.
        """

        try:
            response = model.generate_content(prompt)
            career_result = response.text

        except Exception as e:
            career_result = str(e)

    return render_template(
        'career.html',
        career_result=career_result
    )

if __name__ == '__main__':
    app.run(debug=True)