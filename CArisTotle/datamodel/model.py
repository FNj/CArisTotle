# from sqlalchemy import Column, Integer, String, ForeignKey, Text, MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from typing import List

from flask_security import UserMixin, RoleMixin
from sqlalchemy import UniqueConstraint

from ..common.mixins import AutoReprMixin
from ..config import db

ModelBase = db.Model

Column = db.Column
Integer = db.Integer
# Numeric = db.Numeric
Float = db.Float
Boolean = db.Boolean
String = db.String
ForeignKey = db.ForeignKey
Text = db.Text
DateTime = db.DateTime
Interval = db.Interval
MetaData = db.MetaData

relationship = db.relationship
deferred = db.deferred
backref = db.backref

Table = db.Table


def _get_date():
    return datetime.now()


class TimeStampMixin:
    created_at: datetime = Column(DateTime, default=_get_date)
    updated_at: datetime = Column(DateTime, onupdate=_get_date)


class ClosedAtMixin:
    closed_at: datetime = Column(DateTime)

    def close(self):
        if not self.closed_at:
            self.closed_at = _get_date()


class ForwardDeclarationBase:
    def __init__(self, *vargs, **kwargs):
        pass


class Role(ForwardDeclarationBase): pass


class User(ForwardDeclarationBase): pass


class Test(ForwardDeclarationBase): pass


class Skill(ForwardDeclarationBase): pass


class SkillState(ForwardDeclarationBase): pass


class Question(ForwardDeclarationBase): pass


class QuestionState(ForwardDeclarationBase): pass


class PossibleAnswer(ForwardDeclarationBase): pass


class TestInstance(ForwardDeclarationBase): pass


class Answer(ForwardDeclarationBase): pass


class_list = [Role, User, Test, Skill, SkillState, Question, QuestionState, PossibleAnswer, TestInstance, Answer]

roles_users = Table('roles_users',
                    Column('user_id', Integer, ForeignKey('users.id')),
                    Column('role_id', Integer, ForeignKey('roles.id')))


class Role(ModelBase, RoleMixin):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)


class User(ModelBase, AutoReprMixin, TimeStampMixin, UserMixin):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    fullname: str = Column(String)
    password: str = Column(String)
    email: str = Column(String, unique=True)
    active = Column(Boolean)

    roles = relationship('Role', secondary=roles_users,
                         backref=backref('users', lazy='dynamic'))


class SelectionCriterion(ModelBase, AutoReprMixin, TimeStampMixin):
    __tablename__ = 'selection_criteria'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False, unique=True)
    description: str = Column(Text)


class Test(ModelBase, AutoReprMixin, TimeStampMixin):
    __tablename__ = 'tests'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, nullable=False)
    description: str = Column(Text)
    default_selection_criterion_id: int = Column(Integer, ForeignKey('selection_criteria.id'), nullable=False)
    net_definition: str = deferred(Column(Text, nullable=False))
    submitter_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    stop_max_time: timedelta = Column(Interval)
    stop_min_answers: int = Column(Integer)
    stop_max_entropy: float = Column(Float)

    submitter: User = relationship("User")
    skills: List[Skill] = relationship("Skill", back_populates="test")
    questions: List[Question] = relationship("Question", back_populates="test")
    instances: List[TestInstance] = relationship("TestInstance", back_populates='test')
    default_selection_criterion: SelectionCriterion = relationship("SelectionCriterion")


class Skill(ModelBase, AutoReprMixin, TimeStampMixin):
    __tablename__ = 'skills'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    test_id: int = Column(Integer, ForeignKey('tests.id'), nullable=False)
    text: str = Column(Text)

    test: Test = relationship("Test", back_populates="skills")
    states: List[SkillState] = relationship("SkillState", back_populates="skill")

    __table_args__ = (UniqueConstraint('name', 'test_id', name='_test_skill_name_ux'),)


class SkillState(ModelBase, AutoReprMixin, TimeStampMixin):
    __tablename__ = 'skill_states'

    id: int = Column(Integer, primary_key=True, index=True)
    skill_id: int = Column(Integer, ForeignKey('skills.id'), nullable=False)
    number: int = Column(Integer, nullable=False)
    description: str = Column(String)

    skill: Skill = relationship("Skill", back_populates='states')
    test: Test = property(lambda self: self.skill.test)

    __table_args__ = (UniqueConstraint('number', 'skill_id', name='_skill_state_number_ux'),)


class Question(ModelBase, AutoReprMixin, TimeStampMixin):
    __tablename__ = 'questions'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    test_id: int = Column(Integer, ForeignKey('tests.id'), nullable=False)
    text: str = Column(Text, nullable=False)

    test: Test = relationship("Test", back_populates="questions")
    states: List[QuestionState] = relationship("QuestionState", back_populates="question")
    possible_answers: List[PossibleAnswer] = relationship("PossibleAnswer", secondary="question_states")

    __table_args__ = (UniqueConstraint('name', 'test_id', name='_test_question_name_ux'),)


class QuestionState(ModelBase, AutoReprMixin, TimeStampMixin):
    __tablename__ = 'question_states'

    id: int = Column(Integer, primary_key=True, index=True)
    question_id: int = Column(Integer, ForeignKey('questions.id'), nullable=False)
    number: int = Column(Integer, nullable=False)
    description: str = Column(String)

    question: Question = relationship("Question", back_populates='states')
    test: Test = property(lambda self: self.question.test)
    possible_answers: List[PossibleAnswer] = relationship("PossibleAnswer", back_populates='state')

    __table_args__ = (UniqueConstraint('number', 'question_id', name='_question_state_number_ux'),)


class PossibleAnswer(ModelBase, AutoReprMixin, TimeStampMixin):
    __tablename__ = 'possible_answers'

    id: int = Column(Integer, primary_key=True, index=True)
    state_id: int = Column(Integer, ForeignKey('question_states.id'), nullable=False)
    text: str = Column(Text, nullable=False)

    state: QuestionState = relationship("QuestionState", back_populates='possible_answers')
    question: Question = property(lambda self: self.state.question)
    test: Test = property(lambda self: self.state.test)
    answers: List[Answer] = relationship("Answer", back_populates='possible_answer')


# class TestInstanceState(ModelBase, AutoReprMixin, TimeStampMixin):  # TODO: Consider removal
#     __tablename__ = 'test_instance_states'
#
#     id: int = Column(Integer, primary_key=True, index=True)
#     name: str = Column(String, nullable=False, unique=True)
#     description: str = Column(Text)


class TestInstance(ModelBase, AutoReprMixin, TimeStampMixin, ClosedAtMixin):
    __tablename__ = 'test_instances'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    test_id: int = Column(Integer, ForeignKey('tests.id'), nullable=False)
    student_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    selection_criterion_id: int = Column(Integer, ForeignKey('selection_criteria.id'), nullable=False)
    # state_id: int = Column(Integer, ForeignKey('test_instance_states.id'), nullable=False, default=1)

    test: Test = relationship("Test")
    student: User = relationship("User")
    answers: List[Answer] = relationship("Answer", back_populates='test_instance')
    selection_criterion: SelectionCriterion = relationship("SelectionCriterion")
    # state: TestInstanceState = relationship("TestInstanceState")


class Answer(ModelBase, AutoReprMixin, TimeStampMixin, ClosedAtMixin):
    __tablename__ = 'answers'

    id: int = Column(Integer, primary_key=True, index=True)
    possible_answer_id: int = Column(Integer, ForeignKey('possible_answers.id'), nullable=False)
    test_instance_id: int = Column(Integer, ForeignKey('test_instances.id'), nullable=False)
    question_id: int = Column(Integer, ForeignKey('questions.id'), nullable=False)
    # is_locked_in: bool = Column(Boolean, default=False)  # TODO: change to closed_at

    test_instance: TestInstance = relationship("TestInstance", back_populates='answers')
    possible_answer: PossibleAnswer = relationship("PossibleAnswer", back_populates='answers')
    question: Question = relationship("Question")
    state: QuestionState = property(lambda self: self.possible_answer.state)
    test: Test = property(lambda self: self.test_instance.test)

    __table_args__ = (UniqueConstraint('question_id', 'test_instance_id',
                                       name='_question_test_instance_ux'),)

# class Address(ModelBase):
#     __tablename__ = 'addresses'
#     id: int = Column(Integer, primary_key=True, index=True)
#     email_address: str = Column(String, unique=True, nullable=False)
#     user_id: int = Column(Integer, ForeignKey('users.id'))
#
#     user: User = relationship("User", backref="addresses")
#
#     def __repr__(self):
#         return "<Address(email_address='%s')>" % self.email_address
#
