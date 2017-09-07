import time
start_time = time.time()
from CArisTotle.datamodel.model import *
from CArisTotle.datamodel.procedures import session, init_db, drop_all, \
    get_entity_by_type_and_id, create_and_get_test_instance
from CArisTotle.common.classes import BayesNetDataModelWrapper
from CArisTotle.common.procedures import entropy_remaining, time_remaining,\
    questions_remaining, get_stopping_criteria_states


print("--- %s seconds ---" % (time.time() - start_time))
# --- insert test_data
drop_all()
init_db()
from CArisTotle.dev.test_data import test_data
test_data()

q45: Question = session.query(Question).filter_by(name='Q45').first()
q45.text = 'Q45 MODIFIED placeholder text'
assert session.query(Question).filter_by(name='Q45').first().text == 'Q45 MODIFIED placeholder text'
session.commit()
print("--- %s seconds ---" % (time.time() - start_time))
# --- take imaginary test based on test data
test: Test = get_entity_by_type_and_id(Test, 1)
student = get_entity_by_type_and_id(User, 1)
selection_criterion = get_entity_by_type_and_id(SelectionCriterion, 1)
# for role in student.roles:
#     print(role.name, role.description)

test_instance = create_and_get_test_instance(test, student, 'Test instance 1', selection_criterion)

bayes_net = BayesNetDataModelWrapper(test_instance)

picked_questions = bayes_net.pick_questions()

print([question.name for question in picked_questions])
session.commit()
print("--- %s seconds ---" % (time.time() - start_time))
# --- new request
test_instance_id = test_instance.id
selected_answers_ids = [75]

test_instance = get_entity_by_type_and_id(TestInstance, test_instance_id)
bayes_net = BayesNetDataModelWrapper(test_instance)

for selected_answer_id in selected_answers_ids:
    bayes_net.submit_answer(selected_answer_id)

picked_questions = bayes_net.pick_questions()
print([question.name for question in picked_questions])

session.commit()
print("--- %s seconds ---" % (time.time() - start_time))
# --- new request
test_instance_id = test_instance.id
selected_answers_ids = [42]

# test_instance = get_entity_by_type_and_id(TestInstance, test_instance_id)
# bayes_net = BayesNetDataModelWrapper(test_instance)
bayes_net = BayesNetDataModelWrapper.from_test_instance_id(test_instance_id)

for selected_answer_id in selected_answers_ids:
    bayes_net.submit_answer(selected_answer_id)

results = bayes_net.get_results()
print(results)
print(bayes_net.get_total_skills_entropy())
print(entropy_remaining(test_instance, bayes_net))
print(time_remaining(test_instance))
print(questions_remaining(test_instance))
stopping_criteria_states = get_stopping_criteria_states(test_instance, bayes_net)
print(stopping_criteria_states)
print(stopping_criteria_states.get_pretty_time_remaining())
# print(stopping_criteria_met(test_instance, stopping_criteria_states))
# test_instance.close()
session.commit()


# session.close()
#
# possible_answers = session.query(PossibleAnswer).all()
# pa = possible_answers[0]
#
#
# for ans in pa.question.possible_answers:
#     print(ans.state.description, ": ", ans.text)
# pass
# print(Test.query.first())
# input("Press Enter to drop all tables.")
# drop_all()
#
# with open(net_file_path, "r") as myfile:
#     net_def = myfile.read()
#
# skill_vars_names = ['S1']
# net_reader = BayesNet(net_def, skill_vars_names)
# questions = net_reader.get_questions()
# skills = net_reader.get_skills()
# questions_number_of_states = net_reader.get_questions_numbers_of_states()
# skills_number_of_states = net_reader.get_skills_numbers_of_states()
# # net_reader.insert_evidence(questions[0:2], [0, 1])
# pick = net_reader.pick_question(net_reader.get_questions())  # TODO: test results
# print(pick)

# print(net_file_path)

print("--- %s seconds ---" % (time.time() - start_time))
# pass
# app.run()
