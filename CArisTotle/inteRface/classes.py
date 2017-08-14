from typing import List

from .procedural import init_net, get_questions, get_skills, get_numbers_of_states, insert_evidence, pick_question, \
    get_marginals


class BayesNet:
    def __init__(self, net_string: str, skill_vars_names: List[str]):
        self.net_string = net_string
        self.skill_vars_names = skill_vars_names
        self.model = init_net(self.net_string, self.skill_vars_names)
        self.questions = self.get_questions()
        self.questions_numbers_of_states = self.get_questions_numbers_of_states()
        self.skills = self.get_skills()
        self.skills_numbers_of_states = self.get_skills_numbers_of_states()

    def get_questions(self):
        return get_questions(self.model)

    def get_skills(self):
        return get_skills(self.model)

    def get_questions_numbers_of_states(self):
        return get_numbers_of_states(self.model, self.questions)

    def get_skills_numbers_of_states(self):
        return get_numbers_of_states(self.model, self.skills)

    def insert_evidence(self, questions_names: List[str], questions_states: List[int]):
        self.model = insert_evidence(self.model, questions_names, questions_states)

    def pick_questions(self, candidate_questions=None, selection_criterion=1):
        if candidate_questions is None:
            candidate_questions = self.questions
        return pick_question(self.model, self.questions, candidate_questions, selection_criterion)

    def get_marginals(self, node_names: List[str]):
        return get_marginals(self.model, node_names)

    def get_results(self):
        marginals = self.get_marginals(self.skills)
        return list(zip(self.skills, marginals))
