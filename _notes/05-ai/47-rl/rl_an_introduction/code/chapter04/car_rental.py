#######################################################################
# Copyright (C)                                                       #
# 2016 Shangtong Zhang(zhangshangtong.cpp@gmail.com)                  #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# 2017 Aja Rangaswamy (aja004@gmail.com)                              #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import logging
from scipy.stats import poisson
from tqdm import trange
from joblib import Parallel, delayed

# matplotlib.use('Agg')

# maximum # of cars in each location
MAX_CARS = 20

# maximum # of cars to move during night
MAX_MOVE_OF_CARS = 5

# expectation for rental requests in first location
RENTAL_REQUEST_FIRST_LOC = 3

# expectation for rental requests in second location
RENTAL_REQUEST_SECOND_LOC = 4

# expectation for # of cars returned in first location
RETURNS_FIRST_LOC = 3

# expectation for # of cars returned in second location
RETURNS_SECOND_LOC = 2

DISCOUNT = 0.9

# credit earned by a car
RENTAL_CREDIT = 10

# cost of moving a car
MOVE_CAR_COST = 2

# all possible actions
actions = np.arange(-MAX_MOVE_OF_CARS, MAX_MOVE_OF_CARS + 1)


poisson_pmf_cache = dict()
poisson_cdf_cache = dict()

def get_poisson_pmf(n, lam):
#     global poisson_pmf_cache
    key = n * 10 + lam
    if key not in poisson_pmf_cache:
        poisson_pmf_cache[key] = poisson.pmf(n, lam)
    return poisson_pmf_cache[key]

def get_poisson_cdf(n, lam):
#     global poisson_cdf_cache
    key = n * 10 + lam
    if key not in poisson_cdf_cache:
        poisson_cdf_cache[key] = poisson.cdf(n, lam)
    return poisson_cdf_cache[key]

def poisson_probability(num, lambda_):
    probs = np.array([get_poisson_pmf(i, lambda_) for i in range(num)] + [1- get_poisson_cdf(num-1, lambda_)])
    nums = np.arange(0, num+1)
    return nums, probs


def compute_rental_return_probs(car_num, rent_lambda, return_lambda, constant_rented_cars, constant_returned_cars):
    if constant_rented_cars:
        rent_nums = np.array([min(rent_lambda, car_num)])
        rent_probs = np.array([1.00])
    else:
        rent_nums, rent_probs = poisson_probability(car_num, rent_lambda)
    car_nums = car_num - rent_nums
    return_max_nums = MAX_CARS - car_nums
    if constant_returned_cars:
        return_items = [(np.array([min(return_lambda, return_max_num)]), np.array([1.00])) for return_max_num in return_max_nums]
    else:
        return_items = [poisson_probability(return_max_num, return_lambda) for return_max_num in return_max_nums]

    last_items = [(car_num + return_nums, rent_prob*return_probs) for (return_nums, return_probs), rent_prob, car_num in zip(return_items, rent_probs, car_nums)]
    last_nums = []
    last_probs = []
    for nums, probs in last_items:
        last_nums += list(nums)
        last_probs += list(probs)
    last_nums = np.array(last_nums)
    last_probs = np.array(last_probs)
    return rent_nums, rent_probs, last_nums, last_probs
        
    
def expected_return(state, action, state_value, constant_rented_cars, constant_returned_cars, exercise_4_7):
    """
    @state: [# of cars in first location, # of cars in second location]
    @action: positive if moving cars from first location to second location,
            negative if moving cars from second location to first location
    @stateValue: state value matrix
    @constant_returned_cars:  if set True, model is simplified such that
    the # of cars returned in daytime becomes constant
    rather than a random value from poisson distribution, which will reduce calculation time
    and leave the optimal policy/value state matrix almost the same
    """
    # initailize total return
    returns = 0.0
    
    if exercise_4_7 and action > 1:
        returns -= MOVE_CAR_COST * (abs(action)-1)
    else:
        returns -= MOVE_CAR_COST * abs(action)

    # moving cars
    NUM_OF_CARS_FIRST_LOC = min(state[0] - action, MAX_CARS)
    NUM_OF_CARS_SECOND_LOC = min(state[1] + action, MAX_CARS)
    
    first_rent_nums, first_rent_probs, first_last_nums, first_last_probs = \
        compute_rental_return_probs(NUM_OF_CARS_FIRST_LOC, RENTAL_REQUEST_FIRST_LOC, RETURNS_FIRST_LOC, constant_rented_cars, constant_returned_cars)
    second_rent_nums, second_rent_probs, second_last_nums, second_last_probs = \
        compute_rental_return_probs(NUM_OF_CARS_SECOND_LOC, RENTAL_REQUEST_SECOND_LOC, RETURNS_SECOND_LOC, constant_rented_cars, constant_returned_cars)
    returns += np.sum(first_rent_probs * first_rent_nums) * RENTAL_CREDIT
    returns += np.sum(second_rent_probs * second_rent_nums) * RENTAL_CREDIT
        
    reward = 0
    for first_num, first_prob in zip(first_last_nums, first_last_probs):
        for second_num, second_prob in zip(second_last_nums, second_last_probs):
            prob = first_prob*second_prob
            if exercise_4_7:
                if  first_num>10:
                    reward -= prob*4
                if  second_num>10:
                    reward -= prob*4                            
            reward += DISCOUNT*prob* state_value[first_num, second_num]
            
    returns += reward
    
    return returns


def action_select(state, value, constant_rented_cars, constant_returned_cars, exercise_4_7):
    action_returns = []
    available_actions = list(range(-min(MAX_MOVE_OF_CARS, state[1]), min(MAX_MOVE_OF_CARS, state[0])+1 ))

    for action in available_actions:
        action_returns.append(expected_return(state, action, value, 
                                              constant_rented_cars, constant_returned_cars,
                                              exercise_4_7))
    new_action = available_actions[np.argmax(action_returns)]
    return new_action


def run(in_place=True, show=False, n_jobs=1, constant_rented_cars=False, constant_returned_cars=True, exercise_4_7=False):
    value = np.zeros((MAX_CARS + 1, MAX_CARS + 1))
    policy = np.zeros(value.shape, dtype=np.int)

    iterations = 0   
    policies = []
    values = []
    
        
    while True:
        policies.append(policy)
        values.append(value)
        # policy evaluation (in-place)
        k = 0
        while True:
            k = k + 1
            old_value = value.copy()            
            if n_jobs <=1:
                for i in range(MAX_CARS + 1):
                    for j in range(MAX_CARS + 1):
                        if in_place:
                            new_state_value = expected_return([i, j], policy[i, j], value, 
                                                              constant_rented_cars, constant_returned_cars, 
                                                              exercise_4_7)
                        else:
                            new_state_value = expected_return([i, j], policy[i, j], old_value, 
                                                              constant_rented_cars, constant_returned_cars, 
                                                              exercise_4_7)
                        value[i, j] = new_state_value
            else:
                value = Parallel(n_jobs=n_jobs)(delayed(expected_return)([i, j], policy[i, j], old_value, 
                                                                             constant_rented_cars, constant_returned_cars, 
                                                                             exercise_4_7) 
                                                for i in range(MAX_CARS + 1) 
                                                for j in range(MAX_CARS + 1)) 
                value = np.array(value)
                value = value.reshape(MAX_CARS + 1, MAX_CARS + 1)

            max_value_change = abs(old_value - value).max()
            if k % 10 == 0: 
                logging.info(f'after {k} iteration: max value change {np.round(max_value_change, 10)}')
            if max_value_change < 1e-4:
                break       
                
         
        # policy improvement
        policy_stable = True
        if n_jobs <=1:
            for i in range(MAX_CARS + 1):
                for j in range(MAX_CARS + 1):
                    old_action = policy[i, j]
                    new_action = action_select([i, j], value, 
                                               constant_rented_cars, constant_returned_cars, 
                                               exercise_4_7)
                    policy[i, j] = new_action

                    if policy_stable and old_action != new_action:
                        policy_stable = False
        else:
            new_policy = Parallel(n_jobs=n_jobs)(delayed(action_select)([i, j], value, 
                                                                        constant_rented_cars, constant_returned_cars, 
                                                                        exercise_4_7)    
                                                 for i in range(MAX_CARS + 1) 
                                                 for j in range(MAX_CARS + 1)) 

            new_policy = np.array(new_policy, dtype=np.int)
            new_policy = new_policy.reshape(MAX_CARS + 1, MAX_CARS + 1)
            max_policychange = abs(new_policy - policy).max()
            policy = new_policy
            if max_policychange > 0:
                policy_stable = False
                    
        logging.info('policy stable {}'.format(policy_stable))

        if policy_stable:
            break

        iterations += 1

    return values, policies


def plot_policies(values, policies, save_name=None):
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
    if save_name is not None:
        plt.savefig(f'../images/{save_name}.png')
    plt.show()

def figure_4_2(in_place=True, constant_rented_cars=False, constant_returned_cars=True, show=False, n_jobs=1):
    value, policy = run(in_place=in_place, show=show, 
                        constant_rented_cars=constant_rented_cars, constant_returned_cars=constant_returned_cars,
                        n_jobs=n_jobs, exercise_4_7=False)
        
    plt.close()

    return value, policy    
    

def exercise_4_7(in_place=True, constant_rented_cars=False, constant_returned_cars=True, show=False, n_jobs=1):
    value, policy = run(in_place=in_place, show=show, 
                        constant_rented_cars=constant_rented_cars, constant_returned_cars=constant_returned_cars,
                        n_jobs=n_jobs, exercise_4_7=True)

    plt.savefig('../images/exercise_4_7.png')
    if show:
        plt.show()        
    plt.close()

    return value, policy


if __name__ == '__main__':
    figure_4_2()
