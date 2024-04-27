#######################################################################
# Copyright (C)                                                       #
# 2016-2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)             #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors 
import matplotlib.patches as mpatches
import random


class WindyGridWorld():

    def __init__(self, WORLD_HEIGHT=7, WORLD_WIDTH=10, ACTIONS=None, random_wind=False):
        # world height
        self.WORLD_HEIGHT = WORLD_HEIGHT
        
        # world width
        self.WORLD_WIDTH = WORLD_WIDTH
        
        # wind strength for each column
        self.WIND = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
    
        
        # probability for exploration
        self.EPSILON = 0.1
        
        # Sarsa step size
        self.ALPHA = 0.5
        
        # reward for each step
        self.REWARD = -1.0
        
        self.START = (3, 0)
        self.GOAL = (3, 7)
        if ACTIONS is None:
            self.ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        else:
            self.ACTIONS = ACTIONS

        self.grid_word = np.zeros((self.WORLD_HEIGHT, self.WORLD_WIDTH))
        for i, wind in enumerate(self.WIND):
            self.grid_word[:, i] = wind

        self.init_q_value()
        self.random_wind = random_wind

    def init_q_value(self):
        self.q_value = {(i, j):{} for j in range(self.WORLD_WIDTH) for i in range(self.WORLD_HEIGHT)}
        for state, action_values in self.q_value.items():
            for action in self.get_actions(state):
                action_values[action] = 0            
    
    def step(self, state, action, random_wind=False):
        def adjust(k, max_value):
            if k<0:
                return 0
            elif k>=max_value:
                return max_value-1
            else:
                return k
            
        i, j = state
        if self.random_wind:
            winds = [wind + np.random.choice([-1, 0, 1]) if wind>0 else wind for wind in self.WIND]
        else:
            winds = self.WIND
        new_state = list(np.array(state) + np.array(action))
        new_state[0] -= winds[j]
        new_state[0] = adjust(new_state[0], self.WORLD_HEIGHT)
        new_state[1] = adjust(new_state[1], self.WORLD_WIDTH)
        return tuple(new_state), winds[j]

    def get_actions(self, state):
        if (0, 0) in self.ACTIONS and self.WIND[state[1]] == 0:
            actions = self.ACTIONS.copy()
            actions.remove((0, 0))
            return actions
        else:
            return self.ACTIONS

    def random_policy(self, state):
        return random.choice(self.get_actions(state))

    def greedy_policy(self, state):
        if len(self.q_value[state])==0:
            return self.random_policy(state) 
            
        q_ = self.q_value[state]
        max_value = max(q_.values())
        max_actions = [k for k, v in q_.items() if v == max_value]
        acion = random.choice(max_actions)
        return acion     
        
    def greedy_soft_policy(self, state):
        if np.random.binomial(1, self.EPSILON) == 1:
            return self.random_policy(state)
        else:
            return self.greedy_policy(state)

                              
    # play for an episode
    def episode(self, state=None, policy=None):
        if policy is None:
            policy = self.greedy_soft_policy
     
        if state is None:
            state = self.START 


        q_value = self.q_value          
            
        # track the total time steps in this episode
        time = 0
    
        # choose an action based on epsilon-greedy algorithm
        action = policy(state)
    
        # keep going until get to the goal state
        while state != self.GOAL:
            next_state, _ = self.step(state, action)         
            next_action = policy(next_state)
            
            # Sarsa update
            q_value[state][action] += self.ALPHA * (self.REWARD + 
                                                    q_value[next_state][next_action] - 
                                                    q_value[state][action])
            state = next_state
            action = next_action
            time += 1
        return time
    
    def show_grid_world(self, ax=None):
        show_plot = False
        if ax is None:
            show_plot = True
            fig = plt.figure()
            ax = fig.gca()

        grid_word = self.grid_word
        width = grid_word.shape[1]
        height = grid_word.shape[0]
        winds = self.WIND        
        start = self.START
        goal = self.GOAL        
            
        # Racetrack background with custom colormap
        cmap = mcolors.ListedColormap(['white', 'lightgray', 'darkgray'])
        ax.imshow(grid_word[::-1], aspect='equal',  cmap=cmap) 
        
        margin = 0
        # Thin grid lines at minor tick mark locations
        ax.set_xticks(np.arange(-0.5 - margin, width + margin, 1), minor=True)
        ax.set_yticks(np.arange(-0.5 - margin, height, 1), minor=True)
        ax.grid(which='minor', color='black', linewidth=0.1)
        ax.tick_params(which='minor', length=0)
        ax.set_frame_on(False)
        
        
        # 添加轴标签
        ax.set_xticks(np.arange(width))
        ax.set_yticks(np.arange(height))
        ax.set_xticklabels([f'{w}|{wind}' for w, wind in zip(np.arange(width), winds)])
        ax.set_yticklabels(np.arange(height))
        
        # 显示开始位置和终止位置       
        ax.text(start[1], start[0], 'S', fontsize=12, ha='center', va='center')  
        ax.text(goal[1], goal[0], 'G', fontsize=12, ha='center', va='center')  
        
        if show_plot:
            plt.show()    

    def show_arrow(self, ax, position, direction, color="blue", width=0.02, head_width=0.02, zorder=2):
        position = np.array(position)[::-1]
        direction = np.array(direction)[::-1]
        patch = mpatches.FancyArrow(*(position), *direction, color=color,
                                    zorder=zorder, fill=True, width=width, head_width=head_width,
                                    length_includes_head=True)
        ax.add_patch(patch)     

    def show_optimal_policy(self, ax=None, title=None):    
        show_plot = False
        if title is None:
            title = f'optimal policy' 
            
        if ax is None:
            show_plot = True
            fig = plt.figure()
            ax = fig.gca()
            
        self.show_grid_world(ax)
        
        #ax.axis('off')
        ax.set_title(title)

        optimal_policy = []
        for i in range(0, self.WORLD_HEIGHT):
            optimal_policy.append([])
            for j in range(0, self.WORLD_WIDTH):
                state = (i, j)
                if state == self.GOAL:
                    optimal_policy[-1].append('G')
                    continue
                action = self.greedy_policy(state)
                optimal_policy[-1].append(action)
                self.show_arrow(ax, np.array(state)-np.array(action)/4, np.array(action)/2, width=0.02, head_width=0.1)
                
        if show_plot:
            plt.show()
        return optimal_policy

    def get_trajectory(self, state=None, q_value=None):
        if q_value is None:
            q_value = self.q_value        
        if state is None:
            state = self.START
        trajectory = []
        i = 0 
        while state != self.GOAL:
            values_ = q_value[state]
            action =  self.greedy_policy(state)
            next_state, wind = self.step(state, action)
            trajectory.append((state, action, wind))  
            state = next_state 
            if i == 50:
                print('there are some loop steps')
                return trajectory
            i += 1
        trajectory.append((self.GOAL, None))
        return trajectory        

    def show_trajectory(self, trajectory=None, ax=None, title=None, show_action=False, show_wind=False): 
        def show_arrow(position, direction, color="blue", width=0.02, head_width=0.02, zorder=2):
            position = np.array(position)[::-1]
            direction = np.array(direction)[::-1]
            patch = mpatches.FancyArrow(*(position), *direction, color=color,
                                        zorder=zorder, fill=True, width=width, head_width=head_width,
                                        length_includes_head=True)
            ax.add_patch(patch)             

        if trajectory is None:
            trajectory = self.get_trajectory()
        
        if title is None:
            title = f'return: {len(trajectory)-1}' 
            
        show_plot = False
        if ax is None:
            show_plot = True
            fig = plt.figure()
            ax = fig.gca()
            
        self.show_grid_world(ax)
        
        #ax.axis('off')
        ax.set_title(title)

        actions = []
        for i in range(1, len(trajectory)):
            previous_state = trajectory[i-1][0]
            previous_action = trajectory[i-1][1]
            previous_wind = trajectory[i-1][2]
            actions.append(previous_action)
            state = trajectory[i][0] 
            self.show_arrow(ax, previous_state, np.array(state) - np.array(previous_state))
            if show_action:
                self.show_arrow(ax, previous_state, np.array(previous_action)/2, color="green", width=0.01, head_width=0.05, zorder=3)
            if show_wind:
                self.show_arrow(ax, previous_state, (-previous_wind/2, 0) , color="red", width=0.01, head_width=0.05, zorder=3)

        if show_plot:
            plt.show()    
  
    def average_step(self, episodes=100):
        steps = []
        ep = 0        
        while ep < episodes:
            steps.append(len(self.get_trajectory())-1)
            ep += 1    
        return np.mean(steps)
        
    def train(self, episodes=200):
        self.init_q_value()
    
        steps = []
        ep = 0
        while ep < episodes:
            steps.append(self.episode())
            ep += 1    
        return steps
    
    def example_6_5(self, episodes=200):
        steps = self.train(episodes)
        steps = np.add.accumulate(steps)
    
        plt.plot(steps, np.arange(1, len(steps) + 1))
        plt.xlabel('Time steps')
        plt.ylabel('Episodes')
    
        plt.savefig('../images/figure_6_3.png')
        plt.show()
        plt.close()
        


if __name__ == '__main__':
    WindyGridWorld().example_6_5()

