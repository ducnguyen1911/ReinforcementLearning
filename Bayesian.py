import math
import random

__author__ = 'duc07'

prob_c = [0.6, 0.4]
prob_a_c0 = [0.67, 0.33]
prob_a_c1 = [0.25, 0.75]
prob_b_c0 = [0.9, 0.1]
prob_b_c1 = [0.4, 0.6]


def gen_rand_val(probs):
    r = 0
    p = -1
    while r >= p:
        x = math.ceil(random.random() * len(probs)) - 1
        x = int(x)
        p = probs[x]
        r = random.random()
    return x


def print_stats(gen_values_ab):
    ab_counts = [0, 0, 0, 0]
    for i in gen_values_ab:
        a = i[0]
        b = i[1]
        ab_counts[a * 2 + b] += 1

    print 'P(a=0|b=0) = ', ab_counts[0] / float(ab_counts[0] + ab_counts[1])
    print 'P(a=1|b=0) = ', ab_counts[1] / float(ab_counts[0] + ab_counts[1])
    print 'P(a=0|b=1) = ', ab_counts[2] / float(ab_counts[2] + ab_counts[3])
    print 'P(a=1|b=1) = ', ab_counts[3] / float(ab_counts[2] + ab_counts[3])


def Monte_Carlo(n=10):
    gen_values_ab = []
    for i in range(0,n+1):
        c = gen_rand_val(prob_c)
        if c == 0:
            a = gen_rand_val(prob_a_c0)
            b = gen_rand_val(prob_b_c0)
        elif c == 1:
            a = gen_rand_val(prob_a_c1)
            b = gen_rand_val(prob_b_c1)
        gen_values_ab.append([a, b])
    print_stats(gen_values_ab)


def main():
    # print gen_rand_val([0.3, 0.7])
    Monte_Carlo(n=10)
    Monte_Carlo(n=100)
    Monte_Carlo(n=1000)


if __name__ == "__main__":
    main()

