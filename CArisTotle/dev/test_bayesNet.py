from unittest import TestCase

import os

from ..inteRface import classes as rifc


class TestBayesNet(TestCase):
    def setUp(self):
        net_file_path = os.path.join(os.path.dirname(__file__), 'net_set1.net')
        with open(net_file_path, "r") as net_file:
            self.net_def = net_file.read()
        self.skill_vars_names = ['S1']
        self.net_reader = rifc.BayesNet(self.net_def, self.skill_vars_names)

    def test_init(self):
        self.assertIsNotNone(self.net_reader)

    def test_get_questions(self):
        questions = self.net_reader.get_questions()
        self.assertEqual(len(questions), 53)
        for i, question in enumerate(questions):
            self.assertEqual(question[0], 'Q')

    def test_get_skills(self):
        skills = self.net_reader.get_skills()
        self.assertEqual(skills, ['S1'], 'Unexpected skill name.')

    def test_get_questions_numbers_of_states(self):
        states = self.net_reader.get_questions_numbers_of_states()
        for state in states:
            self.assertEqual(state, 2, 'Unexpected number of question states.')

    def test_get_skills_numbers_of_states(self):
        states = self.net_reader.get_skills_numbers_of_states()
        for state in states:
            self.assertEqual(state, 3, 'Unexpected number of skill states.')

    def test_insert_evidence(self):
        self.net_reader.insert_evidence(['Q42', 'Q24'], [0, 1])

    def test_pick_question(self):
        pick = self.net_reader.pick_questions(self.net_reader.get_questions())
        self.assertEqual(pick, ['Q19'], 'Unexpected question picked.')
