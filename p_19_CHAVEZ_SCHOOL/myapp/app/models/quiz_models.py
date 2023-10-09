from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    topic = Column(String, nullable=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=True)  # Made nullable

    # Relationship with Quiz (if applicable)
    quiz = relationship('Quiz', back_populates='questions', uselist=False)

    # Relationship with Answer
    answers = relationship('Answer', back_populates='question')


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    topic = Column(String, nullable=True)  # Added topic field
    is_correct = Column(Boolean, nullable=False, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)

    # Relationship with Question
    question = relationship('Question', back_populates='answers')

# Assuming you also have a Quiz model
class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)

    # Relationship with Question
    questions = relationship('Question', back_populates='quiz')
