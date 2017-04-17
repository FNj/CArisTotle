import time

from CArisTotle.datamodel.model import *
from CArisTotle.datamodel.procedures import session, init_db, drop_all
from CArisTotle.dev.test_data import entities, net_file_path
from CArisTotle.inteRface import classes as rifc

start_time = time.time()
drop_all()
init_db()

session.add_all(entities)
session.commit()

q45: Question = session.query(Question).filter_by(name='Q45').first()
q45.text = 'Q45 MODIFIED placeholder text'
session.commit()

# session.close()
#
# possible_answers = session.query(PossibleAnswer).all()
# pa = possible_answers[0]
#
#
# for ans in pa.question.possible_answers:
#     print(ans.state.description, ": ", ans.text)

# input("Press Enter to drop all tables.")
drop_all()
#
with open(net_file_path, "r") as myfile:
    net_def = myfile.readlines()

skill_vars_names = ['S1']
net_reader = rifc.BayesNet(net_def, skill_vars_names)
questions = net_reader.get_questions()
skills = net_reader.get_skills()
questions_number_of_states = net_reader.get_questions_numbers_of_states()
skills_number_of_states = net_reader.get_skills_numbers_of_states()
net_reader.insert_evidence(questions[0:2], [0, 1])
pick = net_reader.pick_question(['Q2', 'Q3', 'Q4', 'Q5', 'Q36'])  # TODO: test results
print(pick)

print(net_file_path)

print("--- %s seconds ---" % (time.time() - start_time))
pass
# app.run()
