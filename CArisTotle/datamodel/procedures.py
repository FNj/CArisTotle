from datetime import datetime
from typing import List, TypeVar, Generic

from .model import User, Test, Question, PossibleAnswer, TestInstance, Answer, SelectionCriterion, \
    Skill, SkillState, Role
from ..config import db

session = db.session
func = db.func


def init_db():
    db.create_all()
    entities = []
    admin_role = Role(name='admin', description="Administrátor aplikace")
    submitter_role = Role(name='submitter', description="Zadavatel testů")
    student_role = Role(name='student', description="Testovaný student")
    roles = [admin_role, submitter_role, student_role]
    entities.extend(roles)
    selection_criterion_1 = SelectionCriterion(id=1, name="Maximalizace středního zisku informace",
                                               description="Maximalizuje se střední hodnota poklesu součtu"
                                                           " Shannonovy entropie napříč dovednostními"
                                                           " proměnnými.")
    selection_criterion_2 = SelectionCriterion(id=2, name="Maximalizace rozptylu na dovednostech",
                                               description="Maximalizace středního rozptylu rozdílu"
                                                           " pravěpdobností stavů dovednostních proměnných"
                                                           " před a po zodpovězení dané otázky.")
    selection_criteria = [selection_criterion_1, selection_criterion_2]
    entities.extend(selection_criteria)
    session.add_all(entities)
    session.commit()


def drop_all():
    db.drop_all()
    db.session.commit()


def list_tests() -> List[Test]:
    return session.query(Test).all()

T = TypeVar('T')


def get_entity_by_type_and_id(entity_type: Generic[T], entity_id: int) -> T:
    entity = session.query(entity_type).filter_by(id=entity_id).first()
    return entity


def get_skill_state_by_skill_and_number(skill: Skill, number: int) -> SkillState:
    return session.query(SkillState).filter(SkillState.skill == skill, SkillState.number == number).first()


def create_and_get_test_instance(test: Test, student: User, name: str,
                                 selection_criterion: SelectionCriterion) -> TestInstance:
    test_instance = TestInstance(test=test, student=student, name=name,
                                 selection_criterion=selection_criterion)
    session.add(test_instance)
    return test_instance


def submit_or_update_answer(test_instance: TestInstance, selected_answer: PossibleAnswer,
                            lock_in: bool = True,
                            force_close: bool = False, force_lock: bool = False) -> bool:
    if force_close or test_instance.closed_at is None:
        existing_answer: Answer = session.query(Answer).filter(
            Answer.test_instance == test_instance, Answer.question == selected_answer.question).first()
        if existing_answer is None:
            answer = Answer(test_instance=test_instance, possible_answer=selected_answer,
                            question=selected_answer.question)
            if lock_in:
                answer.close()
            session.add(answer)
            return True
        elif force_lock or not existing_answer.closed_at:
            existing_answer.possible_answer = selected_answer
            return True
        else:
            raise Exception('Cannot update a locked in answer (unless forced).')
    else:
        raise Exception('Cannot add answer to a closed test (unless forced).')


def list_unanswered_questions(test_instance: TestInstance) -> List[Question]:
    answers = test_instance.answers
    if answers is not None and len(answers) > 0:
        unanswered_questions = session.query(Question).filter(Question.test == test_instance.test,
                                                              ~Question.id.in_(
                                                                  [answer.question.id for answer
                                                                   in answers])).all()
    else:
        unanswered_questions = test_instance.test.questions
    return unanswered_questions


def list_answers_by_test_instance(test_instance: TestInstance) -> List[Answer]:
    return session.query(Answer).filter(Answer.test_instance == test_instance).all()


def list_test_instances_by_test_and_student(test: Test, student: User) -> List[TestInstance]:
    return session.query(TestInstance).filter(TestInstance.test == test,
                                              TestInstance.student == student).all()


def list_selection_criteria() -> List[SelectionCriterion]:
    return session.query(SelectionCriterion).all()


def get_answer_by_question_and_test_instance(question: Question, test_instance: TestInstance) -> Answer:
    return session.query(Answer).filter(Answer.question == question,
                                        Answer.test_instance == test_instance).first()


def get_latest_answers_update_timestamp_by_test_instance(test_instance: TestInstance) -> datetime:
    max_candidates = [dt for dt in
                      session.query(func.max(Answer.created_at), func.max(Answer.updated_at)
                                    ).filter(Answer.test_instance == test_instance).first()
                      if dt is not None]
    if max_candidates:
        return max(max_candidates)
    else:
        return test_instance.created_at


def close_test_instance(test_instance: TestInstance):
    test_instance.close()
    for answer in test_instance.answers:
        answer.close()
