import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import poisson


class State:
    def __init__(self, first_car_num, second_car_num):
        self.first_car_num = first_car_num
        self.second_car_num = second_car_num

class JackRental:
    def __init__(self, max_car_num=20, max_move_car_num=5, poisson_upper_bound=11,
                 car_rent_lambda=(3, 4), car_return_lambda=(3, 2), 
                 constant_rent=False, constant_return=True,
                 rent_reward=10, move_reward=-2, in_place=True,
                 discount=0.9, theta=1e-4, verbose=False):
        self.max_car_num = max_car_num
        self.max_move_car_num = max_move_car_num
        self.poisson_upper_bound = poisson_upper_bound
        self.car_rent_lambda = car_rent_lambda
        self.car_return_lambda = car_return_lambda
        self.constant_rent = constant_rent
        self.constant_return = constant_return
        self.rent_reward = rent_reward
        self.move_reward = move_reward
        self.in_place = in_place
        self.discount = discount
        self.theta = theta
        self.verbose = verbose
        self.poisson_cache = {}

    def get_move_actions(self, state):
        actions = []
        first_max_num = min(self.max_move_car_num, state[0])
        second_max_num = min(self.max_move_car_num, state[1])
        actions =  list(range(-second_max_num, 0)) + list(range(0, first_max_num+1))
#         print(f'state={state} actions={actions}')
        return np.array(actions)
    
    def poisson_prob(self, n, lambda_):
        key = n * 10 + lambda_
        if key not in self.poisson_cache:
            self.poisson_cache[key] = poisson.pmf(n, lambda_)
        return self.poisson_cache[key]    
    
    def send_back(self,state):
        send_back_num = 0
        new_state = state.copy()
        for i in range(len(new_state)):
            if new_state[i] > self.max_car_num:
                send_back_num += new_state[i] - self.max_car_num  
                new_state[i] = self.max_car_num
        return new_state, 0
             
    
    def rent(self, state):
        def rent_(car_num, rent_lambda):
            if self.constant_rent:
                rent_num = rent_lambda
            else:
                rent_num =  self.poisson_upper_bound 
                while rent_num >= self.poisson_upper_bound:
                    rent_num = np.random.poisson(lam=rent_lambda)

            rent_num = min(rent_num, car_num)   
            car_num -= rent_num
            return car_num, rent_num*self.rent_reward
        
        reward = 0
        new_state = state.copy()
        for i in range(len(new_state)):
            new_state[i], r = rent_(new_state[i], self.car_rent_lambda[i])
            reward += r 
#         if self.verbose: print(f'rent: {new_state}, {reward}' )
        return new_state, reward
            
    def return_(self, state):
        def return__(car_num, return_lambda):
            if self.constant_rent:
                return_num = return_lambda
            else:
                return_num =  self.poisson_upper_bound 
                while return_num >= self.poisson_upper_bound:            
                    return_num = np.random.poisson(lam=return_lambda)

            car_num += return_num
            return car_num, 0
        
        reward = 0
        new_state = state.copy()
        for i in range(len(new_state)):
            new_state[i], r = return__(new_state[i], self.car_return_lambda[i])
            reward += r    
        
#         if self.verbose: print(f'return_: {new_state}, {reward}' )
        new_state, r = self.send_back(new_state)
        reward += r                 
        return new_state, reward     
        
    
    def move(self, state, move_car_num):     
        new_state = state.copy() 
                 
        new_state[0] -= move_car_num
        new_state[1] += move_car_num    
        reward = abs(move_car_num)*self.move_reward 

        new_state, r = self.send_back(new_state) 
        reward += r             
        return new_state, reward
    
    def expected_return_wrong(self, state, action, v):
        returns = 0
        next_state, r = self.move(state, action)
        returns += r         
        next_state, r = self.rent(next_state)
        returns += r                 
        next_state, r = self.return_(next_state)
        returns += r
        
        returns += self.discount * v[next_state[0], next_state[1]]
        return returns        
        
    
    def expected_return(self, state, action, v):
        returns = 0
        next_state, r = self.move(state, action)
        returns += r                                   

        reward_rent = 0
        for first_rent_num in range(self.poisson_upper_bound):
            for second_rent_num in range(self.poisson_upper_bound):
                prob_rent = self.poisson_prob(first_rent_num, self.car_rent_lambda[0]) *  \
                    self.poisson_prob(second_rent_num, self.car_rent_lambda[1])
                
                current_state = next_state.copy()
                
                valid_first_rent_num = min(first_rent_num, current_state[0])
                valid_second_rent_num = min(second_rent_num, current_state[1])
                
                current_state[0] -= valid_first_rent_num
                current_state[1] -= valid_second_rent_num
                
                reward = (valid_first_rent_num + valid_second_rent_num) * self.rent_reward
                
                if not self.constant_return:                
                    for first_return_num in range(self.poisson_upper_bound):
                        for second_return_num in range(self.poisson_upper_bound):     
                            prob_return = self.poisson_prob(first_return_num, self.car_return_lambda[0]) *  \
                                self.poisson_prob(first_return_num, self.car_return_lambda[1])
                            prob = prob_return * prob_rent

                            first_car_num = min(current_state[0] + first_return_num, self.max_car_num)
                            second_car_num = min(current_state[1] + second_return_num, self.max_car_num)

                            reward_rent += prob*reward
                            returns += prob * (reward + self.discount * v[first_car_num, second_car_num])
                else:
                    prob = prob_rent
                    
                    first_return_num = self.car_return_lambda[0]
                    second_return_num = self.car_return_lambda[1]

                    first_car_num = min(current_state[0] + first_return_num, self.max_car_num)
                    second_car_num = min(current_state[1] + second_return_num, self.max_car_num)

                    reward_rent += prob*reward
                    returns += prob * (reward + self.discount * v[first_car_num, second_car_num])
#         print(f'state={state}, returns={returns}, reward_rent={reward_rent}')
                                        
        return returns
    
    def run(self, fun=None):
        plt.close()
        # Initialization
        
        v = np.zeros((self.max_car_num+1, self.max_car_num+1))
        pi = np.zeros((self.max_car_num+1, self.max_car_num+1), dtype=np.int) 
        
        if fun is None:
            fun = self.expected_return
        
        iterations = 0
        fontsize = 30
        if self.verbose:
            _, axes = plt.subplots(2, 3, figsize=(40, 20))
            plt.subplots_adjust(wspace=0.1, hspace=0.2)
            axes = axes.flatten()        
        while True:
            # Policy Evaluation
            if self.verbose and iterations<len(axes):
                fig = sns.heatmap(np.flipud(pi), cmap="YlGnBu", ax=axes[iterations])
                fig.set_ylabel('# cars at first location', fontsize=fontsize)
                fig.set_yticks(list(reversed(range(self.max_car_num + 1))))
                fig.set_xlabel('# cars at second location', fontsize=fontsize)
                fig.set_title('policy {}'.format(iterations), fontsize=fontsize)            
            
            k = 0
            while True:
                k = k + 1
                delta = 0
                old_v = v.copy()
                for i in range(self.max_car_num+1):
                    for j in range(self.max_car_num+1):  
                        state = [i, j]     
                        action = pi[i, j]
                        if self.in_place:
                            v[i, j] = fun(state, action, v)
                        else:
                            v[i, j] = fun(state, action, old_v)
                        new_delta = abs(v[i, j]-old_v[i,j])
                        
                        if new_delta > delta:
                            delta = new_delta
                if k % 10 == 0:
                    print(f'after {k} iteration: delta={delta}')
                if delta < self.theta:
                    break
            
            # Policy Improvement
            is_stable = True
            for i in range(self.max_car_num+1):
                for j in range(self.max_car_num+1):  
                    state = [i, j]          
                    old_action = pi[i, j]
                    
                    actions = self.get_move_actions(state)    
                    actions_values = []
                    for action in actions:  
                        actions_values.append(fun(state, action, v))
                    
                    new_action = actions[np.argmax(actions_values)]
                    pi[i, j] = new_action
                                      
                    if is_stable and old_action != new_action:
                        is_stable = False
            print('policy stable = {}'.format(is_stable))
            if is_stable:    
                if self.verbose and iterations<len(axes):
                    fig = sns.heatmap(np.flipud(v), cmap="YlGnBu", ax=axes[-1])
                    fig.set_ylabel('# cars at first location', fontsize=fontsize)
                    fig.set_yticks(list(reversed(range(self.max_car_num + 1))))
                    fig.set_xlabel('# cars at second location', fontsize=fontsize)
                    fig.set_title('optimal value', fontsize=fontsize)            
                break
            iterations += 1
        if self.verbose:
            plt.show()  
        return v, pi
        

if __name__ == '__main__':
    rental = JackRental()
    print(f'rental.get_actions(5, 4) = {rental.get_actions(5, 4)}')
    print(f'rental.get_actions(17, 16) = {rental.get_actions(17, 16)}')

