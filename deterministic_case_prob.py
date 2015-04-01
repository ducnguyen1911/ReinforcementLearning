__author__ = 'duc07'
import numpy
import random
import matplotlib.pyplot as plt

GAMMA = 0.9
GOAL_STATE = 6
e = 0.2  # greedy parameter
g_numb_same_q = 0
g_prev_q_arr = numpy.zeros((12, 4))
g_cur_q_arr = numpy.zeros((12, 4))
g_dict_action = {0: -4, 1: 4, 2: -1, 3: 1}  # 0: up, 1: down, 2: left, 3: right
g_q_diff = []


# Randomly select a state
def select_state():
    states = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    return random.choice(states)


# Return only legal actions from state s
def select_act(s):
    acts = []
    for a, v in g_dict_action.iteritems():
        ns = s + v
        if ns in range(0, 12):
            if (a in [2, 3] and ns / 4 == s / 4) or (a in [0, 1]):  # check this condition
                acts.append(a)
    randind = random.randint(0, len(acts) - 1)
    return acts[randind]


def select_act_with_e_greedy(s):
    if random.random() > e:
        return select_act(s)  # random policy
    else:
        return get_max_q_index(s)  # max Q


def get_reward(s, a):
    return 100 if s + g_dict_action[a] == GOAL_STATE else 0


def get_next_state(s, a):
    return s + g_dict_action[a]


# Return max Q from a given state s. Consider all legal actions from that state
def get_max_q(s):
    return max(g_cur_q_arr[s])


def get_max_q_index(s):
    temp_q = []
    temp_q[:] = g_cur_q_arr[s]
    for i in range(0, len(temp_q)):
        ns = s + g_dict_action[i]
        if (ns not in range(0, 12)) or (i in [2, 3] and ns / 4 == s / 4):
            temp_q[i] = -99
    return numpy.argmax(temp_q)


def check_end_condition():
    # print g_cur_q_arr
    # print g_prev_q_arr
    global g_numb_same_q
    if (g_prev_q_arr is not None) and (g_prev_q_arr == g_cur_q_arr).all():
        g_numb_same_q += 1
    else:
        g_numb_same_q = 0
    return True if g_numb_same_q >= 50 else False


def do_episodes():
    global g_cur_q_arr
    s = select_state()  # randomly select a state

    while s != GOAL_STATE:
        a = select_act_with_e_greedy(s)  # with probability, greedy vs. random
        r = get_reward(s, a)
        s_next = get_next_state(s, a)
        g_cur_q_arr[s][a] = r + GAMMA * get_max_q(s_next)  # update table entry for Q(s,a)
        s = s_next


def reset_q_arrs():
    global g_prev_q_arr
    global g_cur_q_arr
    global g_numb_same_q
    global g_q_diff
    g_prev_q_arr = numpy.zeros((12, 4))
    g_cur_q_arr = numpy.zeros((12, 4))
    g_cur_q_arr += random.random() * 0.0001  # init Q table with a very small random number
    g_q_diff = []
    g_numb_same_q = 0


def Q_learning():
    reset_q_arrs()
    global g_prev_q_arr
    i = 0
    while not check_end_condition():
        i += 1
        print 'iter: ', i
        q_diff = numpy.sum(numpy.abs(g_cur_q_arr[:][:] - g_prev_q_arr[:][:]))
        g_q_diff.append(q_diff)
        g_prev_q_arr[:][:] = g_cur_q_arr
        do_episodes()


def plot_q_diff():
    plt.plot(g_q_diff)
    plt.ylabel('Q diff')
    plt.show()


def run(et):
    global e
    e = et
    Q_learning()
    g_cur_q_arr[g_cur_q_arr < 0.5] = -99
    print 'e = ', et
    print 'g_cur_q_arr: ', numpy.around(g_cur_q_arr, 3)
    print 'g_q_diff: ', g_q_diff
    plot_q_diff()


def main():
    run(0.0)
    run(0.2)
    run(0.5)
    run(1.0)


if __name__ == "__main__":
    main()