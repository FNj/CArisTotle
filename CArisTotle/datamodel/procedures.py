from .config import db
from .model import User, Test, Question, PossibleAnswer, TestInstance, Answer

session = db.session


def init_db():
    # ModelBase.metadata.create_all(engine)
    db.create_all()


def drop_all():
    # ModelBase.metadata.drop_all(engine)
    db.drop_all()


def list_tests():
    return session.query(Test).all()


def get_entity_by_type_and_id(entity_type: type, entity_id: int):
    entity = session.query(entity_type).filter_by(id=entity_id).first()
    return entity


def create_and_get_test_instance(test: Test, student: User) -> TestInstance:
    test_instance = TestInstance(test=test, student=student)
    session.add(test_instance)
    return test_instance


def post_answer(test_instance: TestInstance, selected_answer: PossibleAnswer):
    answer = Answer(test_instance=test_instance, possible_answer=selected_answer)
    session.add(answer)


def get_unanswered_questions(test_instance: TestInstance):
    answers = test_instance.answers
    if answers is not None and len(answers) > 0:
        unanswered_questions = session.query(Question).filter(Question.test == test_instance.test, ~Question.id.in_(
            [answer.question.id for answer in answers])).all()
    else:
        unanswered_questions = test_instance.test.questions
    return unanswered_questions
