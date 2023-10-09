from models import Question, Answer, Quiz, Session  # Adjust the import based on your actual file and class names

# Initialize a session
session = Session()


# Sample questions and answers for Calculus 3
calculus_questions = [
    "What is the integral of x^2?",
    "What is the derivative of sin(x)?",
    "What is the limit of (1/x) as x approaches infinity?"
]

calculus_answers = [
    ["x^3/3 + C", "x^3 + C"],
    ["cos(x)", "sin(x)"],
    ["0", "1"]
]

# Sample questions and answers for Probability
probability_questions = [G
    "What is P(A and B) if A and B are independent?",
    "What is the expected value of a fair six-sided die?",
    "What is the variance of a uniform distribution from a to b?"
]

probability_answers = [
    ["P(A) * P(B)", "P(A) + P(B)"],
    ["3.5", "6"],
    ["(b-a)^2 / 12", "(b-a)^2"]
]

def add_questions_and_answers():
    # Create quizzes
    quiz1 = Quiz(title="Calculus 3 Quiz")
    quiz2 = Quiz(title="Probability Quiz")

    # Add questions and answers for Calculus 3
    for i, question_text in enumerate(calculus_questions):
        question = Question(text=question_text, topic="Calculus 3", quiz=quiz1)
        for j, answer_text in enumerate(calculus_answers[i]):
            is_correct = (j == 0)  # Assuming the first answer is always correct
            answer = Answer(text=answer_text, is_correct=is_correct, topic="Calculus 3", question=question)
            session.add(answer)
        session.add(question)

    # Add questions and answers for Probability
    for i, question_text in enumerate(probability_questions):
        question = Question(text=question_text, topic="Probability", quiz=quiz2)
        for j, answer_text in enumerate(probability_answers[i]):
            is_correct = (j == 0)  # Assuming the first answer is always correct
            answer = Answer(text=answer_text, is_correct=is_correct, topic="Probability", question=question)
            session.add(answer)
        session.add(question)

    # Add quizzes to session and commit
    session.add_all([quiz1, quiz2])
    session.commit()

# Add the questions and answers to the database
add_questions_and_answers()





