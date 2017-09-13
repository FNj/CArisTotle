import os

from ..config import user_datastore
from ..datamodel.model import *
from ..datamodel.procedures import get_entity_by_type_and_id, session
from ..inteRface.classes import BayesNet


def test_data():
    net_file_path = os.path.join(os.path.dirname(__file__), 'net_set1.net')

    with open(net_file_path, "r") as net_file:
        net_def = net_file.read()

    skill_names = ['S1']

    net_reader = BayesNet(net_def, skill_names)

    selection_criterion_1 = get_entity_by_type_and_id(SelectionCriterion, 1)

    entities = []

    me = user_datastore.create_user(name='František Navrkal', fullname="František'); DROP TABLE users;-- Navrkal",
                                    password='zizalajeborec123', email='frantisek.navrkal@pirati.cz')
    # me.roles = roles
    entities.append(me)

    my_test = Test(name="Testy test", default_selection_criterion=selection_criterion_1,
                   net_definition=net_def, submitter=me)
    my_test.description = """Testovní test k testování."""
    my_test.stop_max_entropy = .5  # v bitech
    my_test.stop_min_answers = 10
    my_test.stop_max_time = timedelta(minutes=90)
    entities.append(my_test)

    skills = []
    for skill_name in net_reader.skills:
        skill = Skill(name=skill_name, test=my_test, text=skill_name + ' placeholder text')
        skills.append(skill)
    entities.extend(skills)

    skill_states = []
    for i, skill_number_of_states in enumerate(net_reader.skills_numbers_of_states):
        for state_number in range(skill_number_of_states):
            skill_state = SkillState(skill=skills[i], number=state_number,
                                     description=skills[i].name + ' state number ' +
                                                 str(state_number) + ' placeholder description')
            skill_states.append(skill_state)
    entities.extend(skill_states)

    questions = []
    for question_name in net_reader.questions:
        question = Question(name=question_name, test=my_test, text=question_name + ' placeholder text')
        questions.append(question)
    entities.extend(questions)

    questions_states = []
    possible_answers = []
    for i, question_number_of_states in enumerate(net_reader.questions_numbers_of_states):
        for state_number in range(question_number_of_states):
            question_state = QuestionState(question=questions[i], number=state_number,
                                           description=questions[i].name + ' state number ' +
                                                       str(state_number) + ' placeholder description')
            questions_states.append(question_state)
            possible_answer = PossibleAnswer(state=question_state, text=questions[i].name + ' state number ' +
                                                                        str(state_number) + ' possible answer')
            possible_answers.append(possible_answer)
    entities.extend(questions_states)
    entities.extend(possible_answers)

    session.add_all(entities)
    session.commit()
