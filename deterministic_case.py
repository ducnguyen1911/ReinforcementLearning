__author__ = 'duc07'
import numpy
from random import randint

GAMMA = 0.9
GOAL_STATE = 7
g_numb_same_q = 0
g_prev_q_arr = None
g_cur_q_arr = numpy.zeros((12, 4))
g_dict_action = {'left': -1, 'right': 1, 'up': -4, 'down': 4}


# Randomly select a state
def select_state():
    return randint(1, 12)


# Return only legal actions from state s
def select_act(s):
    acts = []
    for a, v in g_dict_action.iteritems():
        if (s + v) in range(1, 12):
            acts.append(a)
    return acts


def get_reward(s, a):
    return 100 if s + g_dict_action[a] == GOAL_STATE else 0


def get_next_state(s, a):
    return s + g_dict_action[a]


# Return max Q from a given state s. Consider all legal actions from that state
def get_max_q(s):
    return max(g_cur_q_arr[s])


def check_end_condition():
    global g_numb_same_q
    if g_prev_q_arr == g_cur_q_arr:
        g_numb_same_q += 1
    else:
        g_numb_same_q = 0
    return True if g_numb_same_q >= 50 else False


def do_episodes():
    global g_cur_q_arr
    g_cur_q_arr = numpy.zeros((12, 4))  # 1. Init the table entry Q(s,a) to zero
    s = select_state()  # randomly select a state

    while s != GOAL_STATE:
        a = select_act(s)  # with probability, greedy vs. random
        r = get_reward(s, a)
        s_next = get_next_state(s, a)
        g_cur_q_arr[s][a] = r + GAMMA * get_max_q(s_next)  # update table entry for Q(s,a)
        s = s_next


def Q_learning():
    global g_prev_q_arr
    while check_end_condition():
        g_prev_q_arr = g_cur_q_arr
        do_episodes()


def run():
    Q_learning()
    print g_cur_q_arr


def main():
    for i in range(1, 10):
        run()


if __name__ == "__main__":
    main()