import os

from ..datamodel.model import *
from ..inteRface.classes import BayesNet

net_file_path = os.path.join(os.path.dirname(__file__), 'net_set1.net')

with open(net_file_path, "r") as net_file:
    net_def = net_file.read()

skill_names = ['S1']

net_reader = BayesNet(net_def, skill_names)
# question_names = net_reader.get_questions()
# questions_number_of_states = net_reader.get_questions_numbers_of_states()
# skills_number_of_states = net_reader.get_skills_numbers_of_states()

entities = []

me = User(name='František Navrkal', fullname="František'); DROP TABLE users;-- Navrkal",
          password='zizalajeborec123', email='frantisek.navrkal@pirati.cz')
entities.append(me)

my_test = Test(name="Testy test", default_criterion=1, net_definition=net_def, submitter=me)
entities.append(my_test)

# my_skill = Skill(name='S1', test=my_test, text='test skill')
# entities.append(my_skill)

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

# my_question = Question(name="Q1", test=my_test,
#                        text="How much wood would a woodchuck chuck if a woodchuck could chuck wood?")
# entities.append(my_question)

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

# my_wrong_state = QuestionState(question=my_question, number=0, description="Wrong")
# my_right_state = QuestionState(question=my_question, number=1, description="Right")
# my_question_states = [my_wrong_state, my_right_state]
# entities.extend(my_question_states)
#
# my_possible_wrong_answer = PossibleAnswer(state=my_wrong_state, text="A woodchuck would chuck as much wood"
#                                                                      " as a woodchuck could chuck"
#                                                                      " if a woodchuck could chuck wood.")
# my_possible_right_answer = PossibleAnswer(state=my_right_state, text="A woodchuck could chuck"
#                                                                      " 361.9237001 cubic centimetres of wood per day.")
# my_possible_answers = [my_possible_wrong_answer, my_possible_right_answer]
# entities.extend(my_possible_answers)
