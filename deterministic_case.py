__author__ = 'duc07'
import numpy

GAMMA = 0.9
GOAL_STATE = 7
g_numb_same_q = 0
g_prev_q_arr = None
g_cur_q_arr = numpy.zeros((12, 4))


def select_state():
    return ''


def select_act(s):
    return ''


def get_reward(s, a):
    return 0


def get_next_state(s, a):
    return ''


def get_max_q(s2):
    return 0


def check_end_condition():
    global g_numb_same_q
    if g_prev_q_arr != g_cur_q_arr:
        g_numb_same_q += 1
    else:
        g_numb_same_q = 0
    if g_numb_same_q >= 50:
        return True
    else:
        return False


def Q_learning():
    global g_prev_q_arr
    # 1. Init the table entry Q(s,a) to zero
    q_arr = numpy.zeros((12, 4))
    # 2. Observe the current state s
    while check_end_condition():
        g_prev_q_arr = g_cur_q_arr
        do_episodes()


def do_episodes():
    global g_cur_q_arr
    g_cur_q_arr = numpy.zeros((12, 4))
    s = select_state()  # randomly select a state

    while s != GOAL_STATE:
        a = select_act(s)  # with probability, greedy vs. random
        r = get_reward(s, a)
        s_next = get_next_state(s, a)
        # update table entry for Q(s,a)
        g_cur_q_arr[s][a] = r + GAMMA * get_max_q(s_next)
        s = s_next