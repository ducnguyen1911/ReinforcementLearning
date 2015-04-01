__author__ = 'duc07'
import numpy

GOAL_STATE = 6
g_dict_action = {0: -4, 1: 4, 2: -1, 3: 1}  # 0: up, 1: down, 2: left, 3: right
g_e_arr = numpy.zeros((12, 4))


def is_legal(s, a):
    ns = s + g_dict_action[a]
    if ns in range(0, 12):
        if (a in [2, 3] and ns / 4 == s / 4) or (a in [0, 1]):
            return True
    return False


def get_reward(s, a):
    return 100 if s + g_dict_action[a] == GOAL_STATE else 0


def get_move_probs(s, a):
    move_probs = [0, 0, 0, 0]
    legal_numb = 4
    for i in range(0, 4):
        if not is_legal(s, i):
            move_probs[i] = 0
            legal_numb -= 1
    for i in range(0, 4):
        if i == a:
            move_probs[i] = 0.7
        elif is_legal(s, i):
            move_probs[i] = (1 - 0.7) / (legal_numb - 1)
    return move_probs  # [0.7, 0.15, 0.15, 0]


def calc_E_sa(s, a):
    e = 0
    move_probs = get_move_probs(s, a)
    for i in range(0, 4):
        e += move_probs[i] * get_reward(s, i)
    return e


def calc_E(s):
    for a in g_dict_action.keys():
        g_e_arr[s][a] = calc_E_sa(s, a) if is_legal(s, a) else 0
    print g_e_arr[s][:]


def main():
    calc_E(2)  # calculate Expected reward E[r(s,a)] for S3
    calc_E(5)  # calculate Expected reward E[r(s,a)] for S6
    calc_E(7)  # calculate Expected reward E[r(s,a)] for S8
    calc_E(10)  # calculate Expected reward E[r(s,a)] for S11

if __name__ == "__main__":
    main()