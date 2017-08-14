from typing import List

from .model import User, Test, Question, PossibleAnswer, TestInstance, Answer, SelectionCriterion, \
    Skill, SkillState
from ..config import db

session = db.session


def init_db():
    # ModelBase.metadata.create_all(engine)
    db.create_all()


def drop_all():
    # ModelBase.metadata.drop_all(engine)
    db.drop_all()


def list_tests() -> List[Test]:
    return session.query(Test).all()


def get_entity_by_type_and_id(entity_type: type, entity_id: int):
    entity = session.query(entity_type).filter_by(id=entity_id).first()
    return entity


def get_skill_states_by_skill_and_number(skill: Skill, number: int) -> SkillState:
    return session.query(SkillState).filter(SkillState.skill == skill, SkillState.number == number).first()


def create_and_get_test_instance(test: Test, student: User, selection_criterion: SelectionCriterion) \
        -> TestInstance:
    test_instance = TestInstance(test=test, student=student, selection_criterion=selection_criterion)
    session.add(test_instance)
    return test_instance


def submit_answer(test_instance: TestInstance, selected_answer: PossibleAnswer):
    answer = Answer(test_instance=test_instance, possible_answer=selected_answer)
    session.add(answer)


def get_unanswered_questions(test_instance: TestInstance) -> List[Question]:
    answers = test_instance.answers
    if answers is not None and len(answers) > 0:
        unanswered_questions = session.query(Question).filter(Question.test == test_instance.test,
                                                              ~Question.id.in_(
                                                                  [answer.question.id for answer in
                                                                   answers])).all()
    else:
        unanswered_questions = test_instance.test.questions
    return unanswered_questions


def list_test_instances_by_test_and_student(test: Test, student: User) -> List[TestInstance]:
    return session.query(TestInstance).filter(TestInstance.test == test, TestInstance.student == student).all()
