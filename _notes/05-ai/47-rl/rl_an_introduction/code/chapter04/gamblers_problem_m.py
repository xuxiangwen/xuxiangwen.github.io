import logging 
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson


class Gambler:
    def __init__(self, max_num, head_prob=0.4, theta=1e-4, verbose=False):
        self.max_num = max_num 
        self.head_prob = head_prob
        self.theta = theta
        self.verbose = verbose        
        self.policies = []
        self.values = []    

    def expected_return(self, state, value):
        if state == 0:
            return 0, 0
        elif state == self.max_num:
            return 0, 1
        
        actions = list(range(1, state+1))
        action_returns = []
        for action in actions:
            if np.random.rand() < self.head_prob:
                next_state = state + action
            else:
                next_state = state - action
            action_return = self.head_prob * value[state + action] + (1 - self.head_prob) * value[state - action]
            action_returns.append(action_return)

        i = np.argmax(action_returns)
        policy_action = actions[i]
        action_return = action_returns[i]
        
        return policy_action, action_return



    def value_iteration(self):
        value = np.zeros(self.max_num+1)
        policy = np.zeros(self.max_num+1)
        iteration = 0
        while True:
            delta = 0
            self.policies.append(policy)
            self.values.append(value)
            old_value = value.copy()  
            for i in range(self.max_num+1):
                policy_action, action_return = self.expected_return(state, value)
                policy[i] = policy_action
                value[i] = action_return

            max_value_change = abs(old_value - value).max()
            if iteration % 1 == 0: 
                logging.info(f'after {iteration} iteration: max value change {np.round(max_value_change, 10)}')
            if max_value_change < 1e-4:
                break                      
            iteration += 1



