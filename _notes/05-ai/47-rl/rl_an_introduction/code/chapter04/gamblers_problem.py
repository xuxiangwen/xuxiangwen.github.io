#######################################################################
# Copyright (C)                                                       #
# 2016-2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)             #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# matplotlib.use('Agg')

# goal
GOAL = 100

# all states, including state 0 and state 100
STATES = np.arange(GOAL + 1)

# probability of head
HEAD_PROB = 0.4


def figure_4_3():
    # state value
    state_value = np.zeros(GOAL + 1)
    policy = np.zeros(GOAL + 1)
    state_value[GOAL] = 1.0

    sweeps_history = []

    # value iteration
    iteration = 0
    while True:
        iteration = iteration + 1
        old_state_value = state_value.copy()
        sweeps_history.append(old_state_value)

        for state in STATES[1:GOAL]:
            # get possilbe actions for current state
            actions = np.arange(1, min(state, GOAL - state) + 1)
            action_returns = []
            for action in actions:
                action_returns.append(
                    HEAD_PROB * state_value[state + action] + (1 - HEAD_PROB) * state_value[state - action])
            
            new_value = np.max(action_returns)
            policy[state] = actions[np.argmax(np.round(action_returns, 7)) ]
#             policy[state] = actions[np.argmax(action_returns) ]
            state_value[state] = new_value
        delta = abs(state_value - old_state_value).max()
        if iteration % 1 == 0: 
            print(f'after {iteration} iteration: max value change {np.round(delta, 10)}')        
        if delta < 1e-9:
            sweeps_history.append(state_value)
            break

    # compute the optimal policy
#     policy = np.zeros(GOAL + 1)
#     for state in STATES[1:GOAL]:
#         actions = np.arange(1, min(state, GOAL - state) + 1)
#         action_returns = []
#         for action in actions:
#             action_returns.append(
#                 HEAD_PROB * state_value[state + action] + (1 - HEAD_PROB) * state_value[state - action])

#         policy[state] = actions[np.argmax(np.round(action_returns, 5)) ]
#         policy[state] = actions[np.argmax(np.round(action_returns, 7)) ]
#         policy[state] = actions[np.argmax(action_returns) ]


    plt.figure(figsize=(10, 12))

    plt.subplot(2, 1, 1)
    for sweep, state_value in enumerate(sweeps_history):
        plt.plot(state_value, label='sweep {}'.format(sweep))
    plt.xlabel('Capital')
    plt.ylabel('Value estimates')
    plt.legend(loc='best')

    plt.subplot(2, 1, 2)
    plt.step(STATES, policy)
    plt.xlabel('Capital')
    plt.ylabel('Final policy (stake)')

#     plt.savefig('../images/figure_4_3.png')
    plt.show()
    plt.close()


if __name__ == '__main__':
    figure_4_3()
