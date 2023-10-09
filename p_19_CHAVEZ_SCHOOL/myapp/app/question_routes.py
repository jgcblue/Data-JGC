from flask import request, jsonify
from app.models.question_models import *

# Initialize a session
session = Session()

def add_question_routes(app):

    @app.route('/add_question', methods=['POST'])
    def add_question():
        try:
            # Get form data
            question_text = request.form.get('question')
            topic = request.form.get('topic')
            answers = request.form.getlist('answers')
            correct_index = int(request.form.get('correct_index'))

            # Create a new question
            new_question = Question(text=question_text, topic=topic)
            
            # Add answers
            for i, answer_text in enumerate(answers):
                is_correct = (i == correct_index)
                new_answer = Answer(text=answer_text, is_correct=is_correct, topic=topic, question=new_question)
                session.add(new_answer)

            # Add question to session and commit
            session.add(new_question)
            session.commit()

            return jsonify({"status": "success", "message": "Question and answers added successfully"}), 200

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

