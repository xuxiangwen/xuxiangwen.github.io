#######################################################################
# Copyright (C)                                                       #
# 2016 Shangtong Zhang(zhangshangtong.cpp@gmail.com)                  #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# 2017 Aja Rangaswamy (aja004@gmail.com)                              #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

# This file is contributed by Tahsincan Köse which implements a synchronous policy evaluation, while the car_rental.py
# implements an asynchronous policy evaluation. This file also utilizes multi-processing for acceleration and contains
# an answer to Exercise 4.5

import numpy as np
import matplotlib.pyplot as plt
import math
import tqdm
import multiprocessing as mp
from functools import partial
import time
import itertools
import logging
from joblib import Parallel, delayed
from scipy.stats import poisson
import seaborn as sns

############# PROBLEM SPECIFIC CONSTANTS #######################
MAX_CARS = 20
MAX_MOVE = 5
MOVE_COST = -2
ADDITIONAL_PARK_COST = -4

RENT_REWARD = 10
# expectation for rental requests in first location
RENTAL_REQUEST_FIRST_LOC = 3
# expectation for rental requests in second location
RENTAL_REQUEST_SECOND_LOC = 4
# expectation for # of cars returned in first location
RETURNS_FIRST_LOC = 3
# expectation for # of cars returned in second location
RETURNS_SECOND_LOC = 2
################################################################

poisson_cache = dict()
poisson_cdf_cache = dict()

def poisson_pmf(n, lam):
    global poisson_cache
    key = n * 10 + lam
    if key not in poisson_cache.keys():
#         poisson_cache[key] = math.exp(-lam) * math.pow(lam, n) / math.factorial(n)
        poisson_cache[key] = poisson.pmf(n, lam)
    return poisson_cache[key]

def poisson_cdf(n, lam):
    global poisson_cdf_cache
    key = n * 10 + lam
    if key not in poisson_cdf_cache.keys():
        poisson_cdf_cache[key] = poisson.cdf(n, lam)
    return poisson_cdf_cache[key]


class PolicyIteration:
    def __init__(self, parallel_processes, delta=1e-2, gamma=0.9, solve_4_7=False, use_multiprocessing=True):
        self.NR_PARALLEL_PROCESSES = parallel_processes
        self.actions = np.arange(-MAX_MOVE, MAX_MOVE + 1)
        self.inverse_actions = {el: ind[0] for ind, el in np.ndenumerate(self.actions)}
        self.value = np.zeros((MAX_CARS + 1, MAX_CARS + 1))
        self.policy = np.zeros(self.value.shape, dtype=np.int)
        self.delta = delta
        self.gamma = gamma
        self.solve_extension = solve_4_7
        self.use_multiprocessing = use_multiprocessing
        self.policies = []
        self.values = []

    def solve(self):
        iterations = 0
        total_start_time = time.time()
        while True:
            self.policies.append(self.policy)
            self.values.append(self.value)
            
            start_time = time.time()
            self.value = self.policy_evaluation(self.value, self.policy)
            elapsed_time = time.time() - start_time
            logging.info(f'PE => Elapsed time {elapsed_time} seconds')
            start_time = time.time()

            policy_change, self.policy = self.policy_improvement(self.actions, self.value, self.policy)
            elapsed_time = time.time() - start_time
            logging.info(f'PI => Elapsed time {elapsed_time} seconds')
            if policy_change == 0:
                break
            iterations += 1
        total_elapsed_time = time.time() - total_start_time
        logging.info(f'Optimal policy is reached after {iterations} iterations in {total_elapsed_time} seconds')

    # out-place
    def policy_evaluation(self, values, policy):

        global MAX_CARS
        iteration = 0
        while True:
        
            iteration = iteration+1
            new_values = np.copy(values)
            k = np.arange(MAX_CARS + 1)
            # cartesian product
            all_states = ((i, j) for i, j in itertools.product(k, k))

            results = []
            if self.use_multiprocessing:
                with mp.Pool(processes=self.NR_PARALLEL_PROCESSES) as p:
                    cook = partial(self.expected_return_pe, policy, values)
                    results = p.map(cook, all_states)
            else:
                cook = partial(self.expected_return_pe, policy, values)
                results = Parallel(n_jobs=self.NR_PARALLEL_PROCESSES)(delayed(cook)(state) for state in all_states) 

            for v, i, j in results:
                new_values[i, j] = v

            difference = np.round(np.abs(new_values - values).max(), 10)
            if iteration % 10==0:
                logging.info(f'after {iteration} iteration: max value change: {difference}')
            values = new_values
            if difference < self.delta:
                logging.info(f'after {iteration} iteration: max value change is converged to {difference}!')
                return values

    def policy_improvement(self, actions, values, policy):
        new_policy = np.copy(policy)

        expected_action_returns = np.zeros((MAX_CARS + 1, MAX_CARS + 1, np.size(actions)))
        cooks = dict()
        with mp.Pool(processes=8) as p:
            for action in actions:
                k = np.arange(MAX_CARS + 1)
                all_states = ((i, j) for i, j in itertools.product(k, k))
                cooks[action] = partial(self.expected_return_pi, values, action)
                results = p.map(cooks[action], all_states)
                for v, i, j, a in results:
                    expected_action_returns[i, j, self.inverse_actions[a]] = v
        for i in range(expected_action_returns.shape[0]):
            for j in range(expected_action_returns.shape[1]):
                new_policy[i, j] = actions[np.argmax(expected_action_returns[i, j])]

        policy_change = (new_policy != policy).sum()
        logging.info(f'Policy changed in {policy_change} states')
        return policy_change, new_policy

    # O(n^4) computation for all possible requests and returns
    def bellman(self, values, action, state):
        expected_return = 0
        if self.solve_extension:
            if action > 0:
                # Free shuttle to the second location
                expected_return += MOVE_COST * (action - 1)
            else:
                expected_return += MOVE_COST * abs(action)
        else:
            expected_return += MOVE_COST * abs(action)

        # moving cars
        num_first_max_rent = int(min(state[0] - action, MAX_CARS))
        num_second_max_rent  = int(min(state[1] + action, MAX_CARS))
        
#         print(state, num_first_max_rent, num_second_max_rent)
        for req1 in range(0, num_first_max_rent+1): 
            if req1 < num_first_max_rent:
                prob1 = poisson_pmf(req1, RENTAL_REQUEST_FIRST_LOC)
            else:
                prob1 = 1 - poisson_cdf(req1-1, RENTAL_REQUEST_FIRST_LOC)          
            expected_return += prob1*req1 * RENT_REWARD 
            
        for req2 in range(0, num_second_max_rent+1):
            if req2 < num_second_max_rent:    
                prob2 = poisson_pmf(req2, RENTAL_REQUEST_SECOND_LOC)                    
            else:      
                prob2 = 1 - poisson_cdf(req2-1, RENTAL_REQUEST_SECOND_LOC)             
            expected_return += prob2*req2 * RENT_REWARD 
        
        for req1 in range(0, num_first_max_rent+1):   
            if req1 < num_first_max_rent:
                prob1 = poisson_pmf(req1, RENTAL_REQUEST_FIRST_LOC)
            else:
                prob1 = 1 - poisson_cdf(req1-1, RENTAL_REQUEST_FIRST_LOC)               
            for req2 in range(0, num_second_max_rent+1):
                # probability for current combination of rental requests                    
                if req2 < num_second_max_rent:    
                    prob2 = poisson_pmf(req2, RENTAL_REQUEST_SECOND_LOC)                    
                else:      
                    prob2 = 1 - poisson_cdf(req2-1, RENTAL_REQUEST_SECOND_LOC)  
                    
                prob = prob1 * prob2                                                

                num_of_cars_first_loc = num_first_max_rent - req1
                num_of_cars_second_loc = num_second_max_rent - req2    
                
                num_first_max_return = MAX_CARS - num_of_cars_first_loc
                num_second_max_return = MAX_CARS - num_of_cars_second_loc

                reward = 0
                for ret1 in range(0, num_first_max_return+1):    
                    if ret1 < num_first_max_return:
                        prob11 = poisson_pmf(ret1, RETURNS_FIRST_LOC)
                    else:
                        prob11 = 1 - poisson_cdf(ret1-1, RETURNS_FIRST_LOC)                       
                    for ret2 in range(0, num_second_max_return+1):                         
                        if ret2 < num_second_max_return:    
                            prob22 = poisson_pmf(ret2, RETURNS_SECOND_LOC)                    
                        else:      
                            prob22 = 1 - poisson_cdf(ret2-1, RETURNS_SECOND_LOC)   
                        prob_ = prob11 * prob22 * prob
                        
                        num_of_cars_first_loc_ = num_of_cars_first_loc + ret1
                        num_of_cars_second_loc_ = num_of_cars_second_loc + ret2
                        
                        if self.solve_extension:
                            if num_of_cars_first_loc_ >= 10:
                                reward += ADDITIONAL_PARK_COST
                            if num_of_cars_second_loc_ >= 10:
                                reward += ADDITIONAL_PARK_COST                           
                                                
                        # Classic Bellman equation for state-value
                        # prob_ corresponds to p(s'|s,a) for each possible s' -> (num_of_cars_first_loc_,num_of_cars_second_loc_)
                        expected_return += prob_ * (
                                reward + self.gamma * values[num_of_cars_first_loc_, num_of_cars_second_loc_])
                        
#         print(state, expected_return)
        return expected_return

    # Parallelization enforced different helper functions
    # Expected return calculator for Policy Evaluation
    def expected_return_pe(self, policy, values, state):

        action = policy[state[0], state[1]]
        expected_return = self.bellman(values, action, state)
        return expected_return, state[0], state[1]

    # Expected return calculator for Policy Improvement
    def expected_return_pi(self, values, action, state):

        if ((action >= 0 and state[0] >= action) or (action < 0 and state[1] >= abs(action))) == False:
            return -float('inf'), state[0], state[1], action
        expected_return = self.bellman(values, action, state)
        return expected_return, state[0], state[1], action

    def plot(self):
        values = self.values
        policies = self.policies
        
        value = values[-1]
        row_count = (len(values) + 3)//3

        _, axes = plt.subplots(row_count, 3, figsize=(row_count*20, 20))

        plt.subplots_adjust(wspace=0.1, hspace=0.2)
        axes = axes.flatten()    

        for i, policy in enumerate(policies):
            fig = sns.heatmap(np.flipud(policy), cmap="YlGnBu", ax=axes[i])
            fig.set_ylabel('# cars at first location', fontsize=30)
            fig.set_yticks(list(reversed(range(MAX_CARS + 1))))
            fig.set_xlabel('# cars at second location', fontsize=30)
            fig.set_title('policy {}'.format(i), fontsize=30)

        fig = sns.heatmap(np.flipud(value), cmap="YlGnBu", ax=axes[len(policies)])
        fig.set_ylabel('# cars at first location', fontsize=30)
        fig.set_yticks(list(reversed(range(MAX_CARS + 1))))
        fig.set_xlabel('# cars at second location', fontsize=30)
        fig.set_title('optimal value', fontsize=30)    

        plt.show()        


if __name__ == '__main__':
    solver = PolicyIteration(parallel_processes=4, delta=1e-4, gamma=0.9, solve_4_5=True)
    solver.solve()
    solver.plot()
