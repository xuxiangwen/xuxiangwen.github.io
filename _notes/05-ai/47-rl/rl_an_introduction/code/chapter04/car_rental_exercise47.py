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

# An up bound for poisson distribution
# If n is greater than this value, then the probability of getting n is truncated to 0
POISSON_UPPER_BOUND = 11

# Probability for poisson distribution
# @lam: lambda should be less than 10 for this function
poisson_cache = dict()


def poisson_probability(n, lam):
#     global poisson_cache
    key = n * 10 + lam
    if key not in poisson_cache:
        poisson_cache[key] = poisson.pmf(n, lam)
    return poisson_cache[key]


def expected_return(state, action, state_value, constant_rented_cars, constant_returned_cars):
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

    # cost for moving cars
    returns -= MOVE_CAR_COST * abs(action)

    # moving cars
    NUM_OF_CARS_FIRST_LOC = min(state[0] - action, MAX_CARS)
    NUM_OF_CARS_SECOND_LOC = min(state[1] + action, MAX_CARS)
    
#     print(f'state={state}, returns={returns}')

    # go through all possible rental requests
    if constant_rented_cars:
        # probability for current combination of rental requests
        prob = 1.00

        num_of_cars_first_loc = NUM_OF_CARS_FIRST_LOC
        num_of_cars_second_loc = NUM_OF_CARS_SECOND_LOC

        # valid rental requests should be less than actual # of cars
        valid_rental_first_loc = min(num_of_cars_first_loc, RENTAL_REQUEST_FIRST_LOC)
        valid_rental_second_loc = min(num_of_cars_second_loc, RENTAL_REQUEST_SECOND_LOC)

        # get credits for renting
        reward = (valid_rental_first_loc + valid_rental_second_loc) * RENTAL_CREDIT
        num_of_cars_first_loc -= valid_rental_first_loc
        num_of_cars_second_loc -= valid_rental_second_loc

        if constant_returned_cars:
            # get returned cars, those cars can be used for renting tomorrow
            returned_cars_first_loc = RETURNS_FIRST_LOC
            returned_cars_second_loc = RETURNS_SECOND_LOC
            num_of_cars_first_loc = min(num_of_cars_first_loc + returned_cars_first_loc, MAX_CARS)
            num_of_cars_second_loc = min(num_of_cars_second_loc + returned_cars_second_loc, MAX_CARS)
            returns += prob * (reward + DISCOUNT * state_value[num_of_cars_first_loc, num_of_cars_second_loc])
        else:
            for returned_cars_first_loc in range(POISSON_UPPER_BOUND):
                for returned_cars_second_loc in range(POISSON_UPPER_BOUND):
                    prob_return = poisson_probability(
                        returned_cars_first_loc, RETURNS_FIRST_LOC) * poisson_probability(returned_cars_second_loc, RETURNS_SECOND_LOC)
                    num_of_cars_first_loc_ = min(num_of_cars_first_loc + returned_cars_first_loc, MAX_CARS)
                    num_of_cars_second_loc_ = min(num_of_cars_second_loc + returned_cars_second_loc, MAX_CARS)
                    prob_ = prob_return * prob
                    returns += prob_ * (reward + DISCOUNT *
                                        state_value[num_of_cars_first_loc_, num_of_cars_second_loc_])        
        
        
    else:
        for rental_request_first_loc in range(POISSON_UPPER_BOUND):
            for rental_request_second_loc in range(POISSON_UPPER_BOUND):
                # probability for current combination of rental requests
                prob = poisson_probability(rental_request_first_loc, RENTAL_REQUEST_FIRST_LOC) * \
                    poisson_probability(rental_request_second_loc, RENTAL_REQUEST_SECOND_LOC)

                num_of_cars_first_loc = NUM_OF_CARS_FIRST_LOC
                num_of_cars_second_loc = NUM_OF_CARS_SECOND_LOC

                # valid rental requests should be less than actual # of cars
                valid_rental_first_loc = min(num_of_cars_first_loc, rental_request_first_loc)
                valid_rental_second_loc = min(num_of_cars_second_loc, rental_request_second_loc)

                # get credits for renting
                reward = (valid_rental_first_loc + valid_rental_second_loc) * RENTAL_CREDIT
                num_of_cars_first_loc -= valid_rental_first_loc
                num_of_cars_second_loc -= valid_rental_second_loc

                if constant_returned_cars:
                    # get returned cars, those cars can be used for renting tomorrow
                    returned_cars_first_loc = RETURNS_FIRST_LOC
                    returned_cars_second_loc = RETURNS_SECOND_LOC
                    num_of_cars_first_loc = min(num_of_cars_first_loc + returned_cars_first_loc, MAX_CARS)
                    num_of_cars_second_loc = min(num_of_cars_second_loc + returned_cars_second_loc, MAX_CARS)
                    returns += prob * (reward + DISCOUNT * state_value[num_of_cars_first_loc, num_of_cars_second_loc])
                else:
                    for returned_cars_first_loc in range(POISSON_UPPER_BOUND):
                        for returned_cars_second_loc in range(POISSON_UPPER_BOUND):
                            prob_return = poisson_probability(
                                returned_cars_first_loc, RETURNS_FIRST_LOC) * poisson_probability(returned_cars_second_loc, RETURNS_SECOND_LOC)
                            num_of_cars_first_loc_ = min(num_of_cars_first_loc + returned_cars_first_loc, MAX_CARS)
                            num_of_cars_second_loc_ = min(num_of_cars_second_loc + returned_cars_second_loc, MAX_CARS)
                            if  num_of_cars_first_loc_>10:
                                reward -= 4*(num_of_cars_first_loc_-10)
                            if  num_of_cars_second_loc_>10:
                                reward -= 4*(num_of_cars_first_loc_-10)                                
                            prob_ = prob_return * prob
                            returns += prob_ * (reward + DISCOUNT *
                                                state_value[num_of_cars_first_loc_, num_of_cars_second_loc_])
                            
#     print(f'state={state}, returns={returns}')
    return returns

def figure_4_2(in_place=True, constant_rented_cars=True, constant_returned_cars=True, show=False, n_jobs=1):
    value = np.zeros((MAX_CARS + 1, MAX_CARS + 1))
    policy = np.zeros(value.shape, dtype=np.int)

    iterations = 0
    _, axes = plt.subplots(2, 3, figsize=(40, 20))
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    axes = axes.flatten()
    while True:
        fig = sns.heatmap(np.flipud(policy), cmap="YlGnBu", ax=axes[iterations])
        fig.set_ylabel('# cars at first location', fontsize=30)
        fig.set_yticks(list(reversed(range(MAX_CARS + 1))))
        fig.set_xlabel('# cars at second location', fontsize=30)
        fig.set_title('policy {}'.format(iterations), fontsize=30)

        # policy evaluation (in-place)
        k = 0
        while True:
            k = k + 1
            old_value = value.copy()            
            if n_jobs <=1:
                for i in range(MAX_CARS + 1):
                    for j in range(MAX_CARS + 1):
                        if in_place:
                            new_state_value = expected_return([i, j], policy[i, j], value, constant_rented_cars, constant_returned_cars)
                        else:
                            new_state_value = expected_return([i, j], policy[i, j], old_value, constant_rented_cars, constant_returned_cars)
                        value[i, j] = new_state_value
            else:
                value = Parallel(n_jobs=n_jobs)(delayed(expected_return)([i, j], policy[i, j], old_value, constant_rented_cars, constant_returned_cars) 
                                                for i in range(MAX_CARS + 1) 
                                                for j in range(MAX_CARS + 1)) 
                value = np.array(value)
                value = value.reshape(MAX_CARS + 1, MAX_CARS + 1)

            max_value_change = abs(old_value - value).max()
            if k % 10 == 0: 
                logging.info(f'after {k} iteration: max value change {max_value_change}')
            if max_value_change < 1e-4:
                break       
                
         
        # policy improvement
        policy_stable = True
        for i in range(MAX_CARS + 1):
            for j in range(MAX_CARS + 1):
                old_action = policy[i, j]
                action_returns = []
                for action in actions:
                    if (0 <= action <= i) or (-j <= action <= 0):
                        action_returns.append(expected_return([i, j], action, value, constant_rented_cars, constant_returned_cars))
                    else:
                        action_returns.append(-np.inf)
                new_action = actions[np.argmax(action_returns)]
                policy[i, j] = new_action

                if policy_stable and old_action != new_action:
                    policy_stable = False

                    
        logging.info('policy stable {}'.format(policy_stable))

        if policy_stable:
            fig = sns.heatmap(np.flipud(value), cmap="YlGnBu", ax=axes[-1])
            fig.set_ylabel('# cars at first location', fontsize=30)
            fig.set_yticks(list(reversed(range(MAX_CARS + 1))))
            fig.set_xlabel('# cars at second location', fontsize=30)
            fig.set_title('optimal value', fontsize=30)
            break

        iterations += 1

    plt.savefig('../images/figure_4_2.png')
    if show:
        plt.show()        
    plt.close()
#     print(f'poisson_cache={poisson_cache}')
    return value, policy


if __name__ == '__main__':
    figure_4_2()
