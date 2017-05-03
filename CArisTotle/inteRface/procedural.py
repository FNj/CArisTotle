from typing import List

import rpy2.robjects as ro
from rpy2.robjects.packages import importr

base = importr('base')
utils = importr('utils')
catest = importr('catest')

r_initialize_network = ro.r['initialize.network']

r_get_questions = ro.r['get.questions']

r_get_skills = ro.r['get.skills']

ro.r('''get.numbers.of.states <- function(model, node_vector) {
                nl <- model@nodes[node_vector]
                vv <- 1:length(nl@nodes)
                for(node in 1:length(nl@nodes)){
                    # nl@nodes[[node]]@name //TO CONSIDER: Maybe make dict instead.
                    vv[node] <- nl@nodes[[node]]@number.of.states
                }
                vv
            }''')
r_get_numbers_of_states = ro.r['get.numbers.of.states']

r_insert_evidence = ro.r['insert.evidence']

r_pick_question = ro.r['pick.question']

ro.r('''get.marginals <- function(model, node_vector) {
                model <- one.dimensional.marginals(model, node.index(model, node_vector))
                x <- list()
                for(i in 1:length(node_vector)){
                    x[[i]] <- model@marginals[[i]]@a
                }
                x
            }''')
r_get_marginals = ro.r['get.marginals']


def init_net(net_string: str, skill_vars_names: List[str]):
    net_string_line_list = ro.StrVector(net_string.split('\n'))
    r_skill_vars_names = ro.StrVector(skill_vars_names)
    return r_initialize_network(net_string_line_list, r_skill_vars_names, is_file=False)


def get_questions(model):
    questions = r_get_questions(model)
    return list(questions)


def get_skills(model):
    skills = r_get_skills(model)
    return list(skills)


def get_numbers_of_states(model, node_names_list: List[str]):
    r_node_vector = ro.StrVector(node_names_list)
    numbers_of_states = r_get_numbers_of_states(model, r_node_vector)
    return list(numbers_of_states)


def insert_evidence(model, question_names_list: List[str], question_states_numbers_list: List[int]):
    question_states_numbers_list = [number + 1 for number in question_states_numbers_list]
    r_questions_vector = ro.StrVector(question_names_list)
    r_questions_states_vector = ro.IntVector(question_states_numbers_list)
    new_model = r_insert_evidence(model=model, evidence=r_questions_vector, state=r_questions_states_vector)
    return new_model


def pick_question(model, all_questions: List[str], candidate_questions: List[str], selection_criterion: int = 1):
    r_all_questions = ro.StrVector(all_questions)
    r_candidate_questions = ro.StrVector(candidate_questions)
    pick_obj = r_pick_question(model, r_all_questions, selection_criterion, r_candidate_questions)
    question_indices = list(pick_obj[2])
    picked_questions = [candidate_questions[index - 1] for index in question_indices]
    return picked_questions


def get_marginals(model, node_names_list: List[str]):
    r_node_vector = ro.StrVector(node_names_list)
    marginals = r_get_marginals(model, r_node_vector)
    return [list(marginal) for marginal in marginals]
