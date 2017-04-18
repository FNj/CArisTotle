# from sqlalchemy import Column, Integer, String, ForeignKey, Text, MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
from typing import List

from .config import db
from ..common.mixins import AutoReprMixin

ModelBase = db.Model

Column = db.Column
Integer = db.Integer
String = db.String
ForeignKey = db.ForeignKey
Text = db.Text
MetaData = db.MetaData

relationship = db.relationship


class ForwardDeclarationBase:
    def __init__(self, *vargs, **kwargs):
        pass


class User(ForwardDeclarationBase): pass


class Test(ForwardDeclarationBase): pass


class Skill(ForwardDeclarationBase): pass


class SkillState(ForwardDeclarationBase): pass


class Question(ForwardDeclarationBase): pass


class QuestionState(ForwardDeclarationBase): pass


class PossibleAnswer(ForwardDeclarationBase): pass


class TestInstance(ForwardDeclarationBase): pass


class Answer(ForwardDeclarationBase): pass


class User(ModelBase, AutoReprMixin):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    fullname: str = Column(String)
    password: str = Column(String)
    email: str = Column(String)


class Test(ModelBase, AutoReprMixin):
    __tablename__ = 'tests'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=False)
    default_criterion: int = Column(Integer, nullable=False)
    net_definition: str = Column(Text, nullable=False)
    submitter_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)

    submitter: User = relationship("User")
    skills: List[Skill] = relationship("Skill", back_populates="test")
    questions: List[Question] = relationship("Question", back_populates="test")
    instances: List[TestInstance] = relationship("TestInstance", back_populates='test')


class Skill(ModelBase, AutoReprMixin):
    __tablename__ = 'skills'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    test_id: int = Column(Integer, ForeignKey('tests.id'), nullable=False)
    text: str = Column(Text)

    test: Test = relationship("Test", back_populates="skills")
    states: List[SkillState] = relationship("SkillState", back_populates="skill")


class SkillState(ModelBase, AutoReprMixin):
    __tablename__ = 'skill_states'

    id: int = Column(Integer, primary_key=True)
    skill_id: int = Column(Integer, ForeignKey('skills.id'), nullable=False)
    number: int = Column(Integer, nullable=False)
    description: str = Column(String)

    skill: Skill = relationship("Skill", back_populates='states')
    test: Test = property(lambda self: self.skill.test)


class Question(ModelBase, AutoReprMixin):
    __tablename__ = 'questions'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    test_id: int = Column(Integer, ForeignKey('tests.id'), nullable=False)
    text: str = Column(Text, nullable=False)

    test: Test = relationship("Test", back_populates="questions")
    states: List[QuestionState] = relationship("QuestionState", back_populates="question")
    possible_answers: List[PossibleAnswer] = relationship("PossibleAnswer", secondary="question_states")


class QuestionState(ModelBase, AutoReprMixin):
    __tablename__ = 'question_states'

    id: int = Column(Integer, primary_key=True)
    question_id: int = Column(Integer, ForeignKey('questions.id'), nullable=False)
    number: int = Column(Integer, nullable=False)
    description: str = Column(String)

    question: Question = relationship("Question", back_populates='states')
    test: Test = property(lambda self: self.question.test)
    possible_answers: List[PossibleAnswer] = relationship("PossibleAnswer", back_populates='state')


class PossibleAnswer(ModelBase, AutoReprMixin):
    __tablename__ = 'possible_answers'

    id: int = Column(Integer, primary_key=True)
    state_id: int = Column(Integer, ForeignKey('question_states.id'), nullable=False)
    text: str = Column(Text, nullable=False)

    state: QuestionState = relationship("QuestionState", back_populates='possible_answers')
    question: Question = property(lambda self: self.state.question)
    test: Test = property(lambda self: self.state.test)
    answers: List[Answer] = relationship("Answer", back_populates='possible_answer')


class TestInstance(ModelBase, AutoReprMixin):
    __tablename__ = 'test_instances'

    id: int = Column(Integer, primary_key=True)
    test_id: int = Column(Integer, ForeignKey('tests.id'), nullable=False)
    student_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)

    test: Test = relationship("Test")
    student: User = relationship("User")
    answers: List[Answer] = relationship("Answer", back_populates='test_instance')


class Answer(ModelBase, AutoReprMixin):
    __tablename__ = 'answers'

    id: int = Column(Integer, primary_key=True)
    possible_answer_id: int = Column(Integer, ForeignKey('possible_answers.id'), nullable=False)
    test_instance_id: int = Column(Integer, ForeignKey('test_instances.id'), nullable=False)

    test_instance: TestInstance = relationship("TestInstance", back_populates='answers')
    possible_answer: PossibleAnswer = relationship("PossibleAnswer", back_populates='answers')
    question: Question = property(lambda self: self.possible_answer.question)
    state: QuestionState = property(lambda self: self.possible_answer.state)
    test: Test = property(lambda self: self.test_instance.test)

# class Address(ModelBase):
#     __tablename__ = 'addresses'
#     id: int = Column(Integer, primary_key=True)
#     email_address: str = Column(String, unique=True, nullable=False)
#     user_id: int = Column(Integer, ForeignKey('users.id'))
#
#     user: User = relationship("User", backref="addresses")
#
#     def __repr__(self):
#         return "<Address(email_address='%s')>" % self.email_address
#
