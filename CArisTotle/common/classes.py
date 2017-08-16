from ..datamodel.model import TestInstance, PossibleAnswer
from ..datamodel.procedures import list_unanswered_questions, submit_or_update_answer, get_entity_by_type_and_id
from ..inteRface.classes import BayesNet


class BayesNetDataModelWrapper:
    def __init__(self, test_instance: TestInstance, locked_in_only: bool=True):  # TODO: Only consider locked_in_questions (opt, but def)
        self.test_instance = test_instance
        self.test = test_instance.test
        self.questions = self.test.questions
        self.skills = sorted(self.test.skills, key=lambda skill: skill.name)
        self.answers = [answer for answer in self.test_instance.answers
                        if answer.is_locked_in or not locked_in_only]
        self.unanswered_questions = list_unanswered_questions(self.test_instance)
        self.selection_criterion = self.test_instance.selection_criterion
        self.bayes_net = BayesNet(self.test.net_definition, [skill.name for skill in self.skills])
        if len(self.answers) > 0:
            self.bayes_net.insert_evidence(questions_names=[answer.question.name for answer in self.answers],
                                           questions_states=[answer.state.number for answer in self.answers])

    def pick_questions(self):
        self.unanswered_questions = list_unanswered_questions(self.test_instance)
        picked_names = self.bayes_net.pick_questions(
            candidate_questions=[question.name for question in self.unanswered_questions],
            selection_criterion=self.selection_criterion.id)
        # return session.query(Question).filter(Question.test == self.test, Question.name.in_(picked_names)).all()
        return [question for question in self.questions if question.name in picked_names]

    def submit_answer(self, selected_answer_id):  # deprecated
        answer = get_entity_by_type_and_id(PossibleAnswer, selected_answer_id)
        self.bayes_net.insert_evidence(questions_names=[answer.question.name],
                                       questions_states=[answer.state.number])
        submit_or_update_answer(self.test_instance, answer, lock_in=True)

    # def get_results(self):
    #     bn_results = sorted(self.bayes_net.get_results(), key=lambda tup: tup[0])
    #     marginal_values_lists = [tup[1] for tup in bn_results]
    #     skill_value_dict = {skill: dict(zip(sorted(skill.states, key=lambda state: state.number),
    #                                         marginal_value))
    #                         for skill, marginal_value in
    #                         zip(self.skills, marginal_values_lists)}
    #     return skill_value_dict

    def get_results(self):
        bn_results = sorted(self.bayes_net.get_results(), key=lambda tup: tup[0])
        marginal_values_lists = [tup[1] for tup in bn_results]
        skill_value_tuple_list = [(skill, list(zip(sorted(skill.states, key=lambda state: state.number),
                                                   marginal_values)))
                                  for skill, marginal_values in zip(self.skills, marginal_values_lists)]
        return skill_value_tuple_list

    @classmethod
    def from_test_instance_id(cls, test_instance_id: int):
        return cls(get_entity_by_type_and_id(TestInstance, test_instance_id))
