#!/usr/bin/env python3

from random import Random
import sys
from copy import copy

RNG = None

class Colors(object):
    to_name = ('blue', 'green', 'orange', 'purple')
    to_letters = tuple([i[0].upper() for i in to_name])
    BLUE, GREEN, ORANGE, PURPLE = 0, 1, 2, 3
    B, G, O, P = 0, 1, 2, 3
    indices = (0, 1, 2, 3)

PAIRS_OF_PAIRS = (((0, 1), (2, 3)),
                  ((0, 2), (1, 3)),
                  ((0, 3), (1, 2)))
S_DOMAIN_STR = ('0.25', '0.5', '0.75')
C_DOMAIN = (1, 2)
NUM_BEADS_PER_URN = 5
NUM_URNS = 4

def choose_s():
    return RNG.choice([0.25, 0.5, 0.75])

def choose_c():
    return RNG.choice([1, 2])

def choose_pair_of_pairs():
    return RNG.choice(PAIRS_OF_PAIRS)



def generate_urns(max_contamination_number):
    start_num = 3
    urn_list = []
    for color_index in Colors.indices:
        urn_color = [Colors.to_letters[color_index]] * start_num
        urn_list.append(urn_color)
    pair_of_pairs = choose_pair_of_pairs()
    for pair in pair_of_pairs:
        f_ind, s_ind = pair
        fu, su = urn_list[f_ind], urn_list[s_ind]
        for cup in [fu, su]:
            for i in range(max_contamination_number):
                color_index = f_ind if RNG.random() < 0.5 else s_ind
                color = Colors.to_letters[color_index]
                cup.append(color)
    for color_index, urn in enumerate(urn_list):
        if len(urn) < NUM_BEADS_PER_URN:
            color = Colors.to_letters[color_index]
            urn.extend([color] * (NUM_BEADS_PER_URN - len(urn)))
        urn.sort()
    return [''.join(i) for i in urn_list]

def debug(msg):
    sys.stderr.write('DEBUG: {}\n'.format(msg))

SAMPLE_SIZE = 20

def simulate():
    switch_rate_param = choose_s()
    max_contamination_number = choose_c()
    switch_prob = switch_rate_param + 0.25*(1-switch_rate_param)
    urns = generate_urns(max_contamination_number)
    debug('urns = {}'.format(urns))
    model = {'S': switch_rate_param,
             'C': max_contamination_number,
             'switch_prob': switch_prob,
             'urns': urns}
    bead_colors, urn_colors = simulate_data(switch_rate_param, urns, SAMPLE_SIZE)
    return model, bead_colors, urn_colors

class Model(object):
    def __init__(self, switch_prob_str, max_num_contam, model_prior):
        self.switch_prob_str = switch_prob_str
        self.s = float(switch_prob_str)
        self.c = max_num_contam
        self.prior = model_prior
        self.full_params = []

class FullParam(object):
    def __init__(self, model, urns, urn_prior):
        self.model = model
        self.urns = urns
        self.prob_urn_given_model = urn_prior
        self.joint_prior = 0.0
        self.log_like_data_given_urn = [0]*NUM_URNS
        self.model.full_params.append(self)
        self.add_prob_given_model(urn_prior)

    def add_prob_given_model(self, p):
        self.joint_prior += p*self.model.prior
        ujp = self.joint_prior/NUM_URNS
        self.urn_prob = [ujp]*NUM_URNS

def all_perms(f_ind, s_ind, c):
    fc = Colors.to_letters[f_ind]
    sc = Colors.to_letters[s_ind]
    if c == 1:
        p = (0.5, 0.5)
    else:
        assert c == 2
        p = (0.25, 0.5, 0.25)
    r = []
    for ns, prob in enumerate(p):
        c = [fc]*(NUM_BEADS_PER_URN - ns)
        c.extend([sc]*ns)
        c.sort()
        r.append((''.join(c), prob))
    return r

def gen_urn_domains(c):
    npp = len(PAIRS_OF_PAIRS)
    for pp in PAIRS_OF_PAIRS:
        fp, sp = pp
        fir_perm = all_perms(fp[0], fp[1], c)
        sec_perm = all_perms(fp[1], fp[0], c)
        fir_ind, sec_ind = fp
        thi_perm = all_perms(sp[0], sp[1], c)
        fou_perm = all_perms(sp[1], sp[0], c)
        thi_ind, fou_ind = sp
        for fu, fprob in fir_perm:
            for su, sprob in sec_perm:
                for tu, tprob in thi_perm:
                    for lu, lprob in fou_perm:
                        el = [None, None, None, None]
                        el[fir_ind] = fu
                        el[sec_ind] = su
                        el[thi_ind] = tu
                        el[fou_ind] = lu
                        p = fprob*sprob*tprob*lprob
                        yield tuple(el), p/npp



def gen_priors():
    by_params = {}
    num_models = len(C_DOMAIN)*len(S_DOMAIN_STR)
    model_prior = 1.0/num_models
    for c in C_DOMAIN:
        for s in S_DOMAIN_STR:
            pt = (s, c)
            by_params[pt] = Model(switch_prob_str=s, max_num_contam=c, model_prior=model_prior)
    by_s_c_u = {}
    for c in C_DOMAIN:
        for u, uprob in gen_urn_domains(c):
            for s in S_DOMAIN_STR:
                by_c_u = by_s_c_u.setdefault(s, {})
                by_u = by_c_u.setdefault(c, {})
                fp = by_u.get(u)
                if fp is None:
                    mkey = (s, c)
                    model = by_params[mkey]
                    fp = FullParam(model=model, urns=u, urn_prior=uprob)
                    by_u[u] = fp
                else:
                    fp.add_prob_given_model(uprob)
    all_combos = []
    for s in S_DOMAIN_STR:
        by_c_u = by_s_c_u[s]
        for c in C_DOMAIN:
            by_u = by_c_u[c]
            cl = [(i.urns, i) for i in by_u.values()]
            cl.sort()
            all_combos.extend([i[-1] for i in cl])
    return list(by_params.values()), all_combos

def analyze(data):
    models, params = gen_priors()
    tp = 0.0
    #for fp in params:
    #    mod = fp.model
    for mod in models:
        mp = 0.0
        for fp in mod.full_params:
            debug('S={:0.2f},C={},U={} Pr={}'.format(mod.s, mod.c, fp.urns, fp.joint_prior))
            tp += fp.joint_prior
            mp += fp.joint_prior
        debug('M(S={}, c={}) prob = {}'.format(mod.s, mod.c, mp))
    debug('total prior prob = {}'.format(tp))

def simulate_data(switch_rate_param, urns, sample_size):
    bead_colors, urn_colors = [], []
    active_index = RNG.choice(Colors.indices)
    active_urn = urns[active_index]
    for i in range(sample_size):
        bead_color = RNG.choice(active_urn)
        bead_colors.append(bead_color)
        urn_colors.append(Colors.to_letters[active_index])
        if RNG.random() < switch_rate_param:
            active_index = RNG.choice(Colors.indices)
            active_urn = urns[active_index]
    return bead_colors, urn_colors

def read_data():
    raise NotImplementedError("read_data not implemented")

def main():
    global RNG
    from datetime import datetime
    import argparse
    p = argparse.ArgumentParser(description='simulator and ML analyzer for urn HMM')
    ACTION_CHOICES = ('simulate', 'analyze', 'both')
    p.add_argument('--action', choices=ACTION_CHOICES, default='both',
                   help='controls the main action.')
    p.add_argument('--seed', default=None, type=int,
                   help='seed for the pseudorandom number generator')
    parsed = p.parse_args()
    print("action = {}".format(parsed.action))
    if parsed.seed is None:
        seed = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
    else:
        seed = parsed.seed
    print("seed = {}".format(seed))
    RNG = Random()
    RNG.seed(seed)
    if parsed.action == 'analyze':
        data = read_data()
    else:
        model, data, urn_samples = simulate()
    if parsed.action == 'simulate':
        print('\t'.join(data))
    else:
        estimate = analyze(data)

if __name__ == '__main__':
    main()
