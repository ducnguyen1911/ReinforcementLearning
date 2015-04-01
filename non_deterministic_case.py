import math

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
g_numb_visit_arr = numpy.zeros((12, 4))
g_reward_arr = numpy.zeros((12, 4))
g_est_e_arr = numpy.zeros((12, 4))


# Randomly select a state
def select_state():
    states = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    return random.choice(states)


# Return only legal actions from state s
def select_act(s):
    acts = []
    for a, v in g_dict_action.iteritems():
        if is_legal(s, a):
                acts.append(a)
    randi = random.randint(0, len(acts) - 1)
    return acts[randi]


def select_act_with_e_greedy(s):
    if random.random() > e:
        return select_act(s)  # random policy
    else:
        return get_max_q_index(s)  # max Q


# Revise this function for non-deterministic case
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
            legal_numb -= 1
    for i in range(0, 4):
        if i == a:
            move_probs[i] = 0.7
        elif is_legal(s, i):
            numb_left = legal_numb - 1 if is_legal(s, a) else legal_numb
            move_probs[i] = (1 - 0.7) / numb_left
    return move_probs  # [0.7, 0.15, 0.15, 0]


def gen_rand_action(move_probs):
    r = 0
    p = -1
    while r >= p:
        x = math.ceil(random.random() * len(move_probs)) - 1
        x = int(x)
        p = move_probs[x]
        r = random.random()
    return x


def get_next_state(s, a):
    move_probs = get_move_probs(s, a)
    actual_a = gen_rand_action(move_probs)
    return s + g_dict_action[actual_a], actual_a


# Return max Q from a given state s. Consider all legal actions from that state
def get_max_q(s):
    return max(g_cur_q_arr[s])


def get_max_q_index(s):
    if s < 0:
        return 0
    temp_q = []
    temp_q[:] = g_cur_q_arr[s]
    for i in range(0, len(temp_q)):
        if not is_legal(s, i):
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


def calc_alpha(s, a):
    return round(float(1) / (1 + g_numb_visit_arr[s][a]), 2)


def calc_expect_value():
    global g_est_e_arr
    arr = g_reward_arr[:][:] / g_numb_visit_arr[:][:]
    g_est_e_arr[:][:] = arr
    for i in (2, 5, 7, 10):
        print 'Expected value for S', i + 1, ': ', arr[i]


def do_episodes():
    global g_cur_q_arr
    global g_reward_arr
    global g_numb_visit_arr
    s = select_state()  # randomly select a state
    while s != GOAL_STATE:
        a = select_act_with_e_greedy(s)  # with probability, greedy vs. random
        g_numb_visit_arr[s][a] += 1  # check this point --------------------------------- **********************
        s_next, actual_a = get_next_state(s, a)  # check this with stochastic case -------- *** -----------------------
        r = get_reward(s, actual_a)
        g_reward_arr[s][a] += r  # update observed reward
        alpha = calc_alpha(s, a)
        # g_cur_q_arr[s][a] = r + GAMMA * get_max_q(s_next)  # update table entry for Q(s,a)
        g_cur_q_arr[s][a] = (1 - alpha) * g_prev_q_arr[s][a]
        g_cur_q_arr[s][a] += alpha * (r + get_max_q(s_next))
        g_cur_q_arr[s][a] = round(g_cur_q_arr[s][a], 2)

        s = s_next


def reset_q_arrs():
    global g_prev_q_arr
    global g_cur_q_arr
    global g_numb_same_q
    global g_q_diff
    global g_numb_visit_arr
    global g_reward_arr
    g_prev_q_arr = numpy.zeros((12, 4))
    g_cur_q_arr = numpy.zeros((12, 4))
    g_cur_q_arr += random.random() * 0.0001
    g_numb_visit_arr = numpy.zeros((12, 4))
    g_reward_arr = numpy.zeros((12, 4))
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
    calc_expect_value()  # ====================================== is it right to call it here???? =====================


def plot_q_diff():
    plt.plot(g_q_diff)
    plt.ylabel('Q diff')
    plt.show()


def run(et):
    print 'e = ', et
    global e
    e = et
    Q_learning()
    g_cur_q_arr[g_cur_q_arr < 0.5] = -99
    print 'g_cur_q_arr: ', numpy.around(g_cur_q_arr, 3)
    print 'g_q_diff: ', g_q_diff
    plot_q_diff()


# Calculate Probability * maxQ
def calc_pm(s, a):
    move_probs = get_move_probs(s, a)  # ==================== ???? not quite sure here =====================
    max_q = [get_max_q(s + g_dict_action[ta]) if is_legal(s, ta) else 0 for ta in (0, 1, 2, 3)]
    return numpy.sum(numpy.array(move_probs) * numpy.array(max_q))


def validate_condition():
    # print Q table for S3, S6, S8, S11
    for s in (2, 5, 7, 10):
        print 'Q(s, a) for S', s + 1, ': ', g_cur_q_arr[s][:]
    # print right side of the formula in problem 6
    p_arr = numpy.zeros((12, 4))
    for s in (2, 5, 7, 10):
        for a in (0, 1, 2, 3):
            p_arr[s][a] = calc_pm(s, a)
    for s in (2, 5, 7, 10):
        print 'Expected value for S', s + 1, ': ', g_est_e_arr[s][:] + GAMMA * p_arr[s][:]


def main():
    run(0.0)
    # validate_condition()
    run(0.2)
    run(0.5)
    run(1.0)
    # arr = get_move_probs(0, 0)
    # print arr

if __name__ == "__main__":
    main()