import logging 
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import poisson
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter
from IPython.display import display

class Gambler:
    def __init__(self, max_num=100, discount=1.00, head_prob=0.4, theta=1e-9, show_iteration_count=1):
        self.max_num = max_num 
        self.discount = discount
        self.head_prob = head_prob
        self.theta = theta       
        self.policies = []
        self.values = []    
        self.show_iteration_count = show_iteration_count

    def expected_return(self, state, value, verbose=False):
#         actions = list(range(1, state + 1 ))
#         action_returns = []
#         for action in actions:
#             action_return = self.head_prob * value[min(state + action, self.max_num)] + (1 - self.head_prob) * value[state - action]
#             action_returns.append(action_return)  

        actions = np.array((range(1, min(state, self.max_num - state) +1)))
        action_returns = []
        for action in actions:
            action_return = self.head_prob * self.discount * value[state + action] + (1 - self.head_prob) * self.discount * value[state - action]
            action_returns.append(action_return)          
        
        # 为了数值稳定性
#         i = np.argmax(np.round(action_returns, 9))
        i = np.argmax(np.round(action_returns, 9))
    
        policy_action = actions[i]
        action_return = np.max(action_returns)
        
        if verbose:
            print('-'*25, f'state={state}, best_action={actions[i]}', '-'*25)
            df = pd.DataFrame(data={'state':state, 'action':actions, 'action_return':np.round(action_returns, 9)})
#             display(df)
            df_max = df.loc[(df['action_return']==np.round(action_return, 9))].head(2)
   
            display(df_max)
            
        
        return policy_action, action_return


    def value_iteration(self):
        value = np.zeros(self.max_num+1)
        policy = np.zeros(self.max_num+1)
        value[self.max_num] = 1
        iteration = 0
        while True:
            iteration += 1

            old_value = value.copy()  
            self.values.append(old_value)  
            self.policies.append(policy)            
            for i in range(1, self.max_num):
                policy_action, action_return = self.expected_return(i, value)
                policy[i] = policy_action
                value[i] = action_return

            max_value_change = abs(old_value - value).max()
            if iteration % self.show_iteration_count == 0: 
                logging.info(f'after {iteration} iteration: max value change {np.round(max_value_change, 10)}')
            if max_value_change < self.theta:
                break                      
            

    def plot(self):
        _, axes = plt.subplots(2, 1, figsize=(9, 11))

        plt.subplots_adjust(wspace=0.1, hspace=0.2)
        axes = axes.flatten()   
        
        if len(self.policies)>10:
            iterations = set([int(i) for i in np.linspace(0, len(self.policies)-1, 10)])  
        else:
            iterations = range(len(self.policies))
        
        x = range(0, self.max_num+1)
        for i in iterations:
            axes[0].plot(x, self.values[i], label=f'sweep {(i+1)}')
        axes[0].set_xlabel('Capital')
        axes[0].set_xticks(range(0, self.max_num+1, 5))
        axes[0].set_ylabel('Value Estimates')   
        axes[0].legend(fontsize=9)

        policy = self.policies[-1]            
        axes[1].step(x, policy)
        axes[1].set_xlabel('Capital')
        axes[1].set_xticks(range(0, self.max_num+1, 5))
        axes[1].set_yticks(range(0, 51, 5))        
        
        axes[1].set_ylabel('Final policy(stake)')
        axes[1].xaxis.set_minor_locator(AutoMinorLocator())
        axes[1].yaxis.set_minor_locator(AutoMinorLocator())        
        
        plt.show()


