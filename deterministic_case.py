import copy

__author__ = 'duc07'
import numpy
import random

GAMMA = 0.9
GOAL_STATE = 6
g_numb_same_q = 0
g_prev_q_arr = numpy.zeros((12, 4))
g_cur_q_arr = numpy.zeros((12, 4))
g_dict_action = {0: -4, 1: 4, 2: -1, 3: 1}  # 0: up, 1: down, 2: left, 3: right


# Randomly select a state
def select_state():
    states = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    return random.choice(states)


# Return only legal actions from state s
def select_act(s):
    acts = []
    for a, v in g_dict_action.iteritems():
        if (s + v) in range(0, 12):
            acts.append(a)
    randind = random.randint(0, len(acts) - 1)
    return acts[randind]


def get_reward(s, a):
    return 100 if s + g_dict_action[a] == GOAL_STATE else 0


def get_next_state(s, a):
    return s + g_dict_action[a]


# Return max Q from a given state s. Consider all legal actions from that state
def get_max_q(s):
    return max(g_cur_q_arr[s])


def check_end_condition():
    print g_cur_q_arr
    print g_prev_q_arr
    global g_numb_same_q
    if (g_prev_q_arr is not None) and (g_prev_q_arr == g_cur_q_arr).all():
        g_numb_same_q += 1
    else:
        g_numb_same_q = 0
    return True if g_numb_same_q >= 50 else False


def do_episodes():
    global g_cur_q_arr
    # g_cur_q_arr = numpy.zeros((12, 4))  # 1. Init the table entry Q(s,a) to zero
    s = select_state()  # randomly select a state

    while s != GOAL_STATE:
        a = select_act(s)  # with probability, greedy vs. random
        r = get_reward(s, a)
        s_next = get_next_state(s, a)
        g_cur_q_arr[s][a] = r + GAMMA * get_max_q(s_next)  # update table entry for Q(s,a)
        s = s_next


def Q_learning():
    global g_prev_q_arr
    i = 0
    while not check_end_condition():
        i += 1
        print 'iter: ', i
        g_prev_q_arr[:][:] = g_cur_q_arr
        do_episodes()


def run():
    Q_learning()
    print g_cur_q_arr


def main():
    for i in range(1, 2):
        run()


if __name__ == "__main__":
    main()