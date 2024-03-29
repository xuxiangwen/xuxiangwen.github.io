import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors 
import matplotlib.patches as mpatches
import os
from datetime import datetime
# matplotlib.use('Agg')

import math
import pickle
import numpy as np
import random
import seaborn as sns
from tqdm import tqdm




class RaceTrack():

    def __init__(self, racetrack_csv, max_speed=5, epsilon=0.1, noise=0.1, gamma=0.1, q_path=None, reset_random=True, reward=-1, acceleration_reward=0):
        self.racetrack = np.fliplr(np.genfromtxt(racetrack_csv, delimiter=',', dtype=np.int32).T)
        self.actions = [(x, y) for y in range(-1, 2) for x in range(-1, 2)] 
        indices = np.where(self.racetrack == 2)
        self.starting_points = list(zip(indices[0], indices[1]))
        indices = np.where(self.racetrack == 3)
        self.ending_points = list(zip(indices[0], indices[1]))
        self.max_speed = max_speed
        self.state_actions = {}
        self.epsilon = epsilon
        self.noise = noise
        self.reset_random = reset_random
        self.reward = reward
        # 因为之前生成的轨迹中，有一些多余的弯曲（加减速造成的）
        # 设置这个量来减少不必要的加减速。
        self.acceleration_reward = acceleration_reward
        if q_path is None:
            self.q = {}
        else:
            self.q = self.load_q(q_path)           
        self.c = {}   
        self.gamma = gamma

    def show_trajectory(self, last_state, player_trajectory, ax=None, title=None): 
        def show_state(position, speed):
            position = np.array(position)
            speed = np.array(speed)
            if (speed == 0).all() :
                patch = mpatches.Circle(position, radius=0.15, color='black', zorder=1)
            else:
                position = np.array(position)
                speed = np.array(speed)
                patch = mpatches.FancyArrow(*(position), *speed, color='blue',
                                            zorder=2, fill=True, width=0.05, head_width=0.25,
                                            length_includes_head=True)
            ax.add_patch(patch)

        if title is None:
            title = f'return: {-len(player_trajectory)}' 
            
        show_plot = False
        if ax is None:
            show_plot = True
            fig = plt.figure()
            ax = fig.gca()
        
        # Racetrack background with custom colormap
        cmap = mcolors.ListedColormap(['white', 'gray', 'red', 'green'])
        ax.imshow(self.racetrack.T, aspect='equal', origin='lower', cmap=cmap)
        
        # Major tick marks max_speed step apart
        ax.set_xticks(np.arange(0, self.racetrack.shape[0], self.max_speed), minor=False)
        ax.set_yticks(np.arange(0, self.racetrack.shape[1], self.max_speed), minor=False)
        
        margin = 1
        # Thin grid lines at minor tick mark locations
        ax.set_xticks(np.arange(-0.5 - margin, self.racetrack.shape[0] + margin, 1), minor=True)
        ax.set_yticks(np.arange(-0.5 - margin, self.racetrack.shape[1] + margin, 1), minor=True)
        ax.grid(which='minor', color='black', linewidth=0.05)
        ax.tick_params(which='minor', length=0)
        ax.set_frame_on(False)

        ax.set_title(title)

        show_state(player_trajectory[0][0][0], (0,0))
        for (position, _), _, speed, _ in player_trajectory:
            show_state(position, speed)
        position, _ = last_state
        show_state(position, (0,0))

        if show_plot:
            plt.show() 

    def save_q(self, q, q_path='q.pickle'):
        with open(q_path, 'wb') as f:
            pickle.dump(q, f)        
        
    def load_q(self, q_path='q.pickle'):
        with open(q_path, 'rb') as f:
            return pickle.load(f)

    # function form of target policy of player
    def greedy_target_policy_player(self, state):
        if state not in self.q or len(self.q[state])==0:
            return random.choice(self.get_actions(state))
        q_ = self.q[state]
        max_value = max(q_.values())
        max_actions = [k for k, v in q_.items() if v == max_value]
        acion = random.choice(max_actions)
        return acion

    def greedy_soft_target_policy_player(self, state):
        if np.random.rand() >= self.epsilon:
            return self.greedy_target_policy_player(state)
        return self.random_behavior_policy_player(state)
    
    # function form of behavior policy of player
    def random_behavior_policy_player(self, state):
        return random.choice(self.get_actions(state))

    # 得到某一个状态下，可以选择的状态
    def get_actions(self, state, verbose=0):
        if state in self.state_actions:
            return self.state_actions[state]
        position, speed = state  
        dx, dy = speed
        actions = [(ax, ay) for ax, ay in self.actions
                   if abs(dx + ax) <= self.max_speed
                   and abs(dy + ay) <= self.max_speed
                   and not ((0, 0) == (dx + ax, dy + ay))
                  ]
        if verbose == 1:
            print(f"state={state}, actions={actions}")
        self.state_actions[state] = actions
        return actions       
        
    def is_over_boundary(self, position):
        if position[0]<0 or position[0]>=self.racetrack.shape[0]:
            return True
        if position[1]<0 or position[1]>=self.racetrack.shape[1]:
            return True  
        if self.racetrack[position]==0:
            return True
        return False    


    def run(self, position, speed, start_state=None, verbose=0):  
        if verbose==1:
            print(f'-'*20)
        max_speed = np.max(np.abs(speed))
        new_position = position
        new_speed = speed
        i = 1
        while i<=max_speed:
            new_position = (
                position[0] + 0.5 + i*speed[0]/max_speed,
                position[1] + 0.5 + i*speed[1]/max_speed
            )            
            if verbose==1:
                print(f'new_position={new_position}')

            x = np.floor(new_position[0])
            y = np.floor(new_position[1])
            new_position = (
                np.int32(x if x!=new_position[0] else x-1),
                np.int32(y if y!=new_position[1] else y-1),
            )     
            if verbose==1:
                print(f'new_position={new_position}')

            # 如果汽车撞到赛道边界，它将被移回到起跑线上的随机位置，两个速度分量都重置为0。
            if self.is_over_boundary(new_position):
                if start_state is not None:
                    new_position, action = start_state
                else:
                    new_position = random.choice(self.starting_points)
                    new_speed = (0, 0)
                break
            elif new_position in self.ending_points:
                break
            i+=1
        state = (new_position, new_speed)
        return state   
        
    # play a game
    # @policy_player: specify policy for player
    def play(self, policy_player=None, start_position=None, noise=None, verbose=0):
        if policy_player is None:
            policy_player = self.greedy_soft_target_policy_player     
        if noise is None:
            noise = self.noise   
        # 轨迹 trajectory of player 
        player_trajectory = []

        # 每个回合开始，在起跑线随机选择一个位置，且速度分量都为0。
        if start_position is not None:
            start_state = (start_position, (0, 0))
        else:
            start_state = (random.choice(self.starting_points), (0, 0))
        is_ending = False
        i = 0
        state = start_state
        while not is_ending:
            action = policy_player(state)               
            position, speed = state   
            
            # 每个时间步，速度有 0.1 的可能性保持原样。
            if np.random.rand()>=self.noise:
                new_speed = (speed[0] + action[0], speed[1] + action[1])
            else:
                new_speed = speed
            if verbose==1:
                print(f'state={state}')
            player_trajectory.append((state, action, new_speed, self.racetrack[position]))
            if self.reset_random:
                state = self.run(position, new_speed)
            else:
                state = self.run(position, new_speed, start_state) 
            is_ending = state[0] in self.ending_points
        return state, player_trajectory
    
    # Monte Carlo Sample with On-Policy
    def monte_carlo_on_policy(self, episodes):
        pass
    
    
    # Monte Carlo Sample with Off-Policy
    def monte_carlo_off_policy(self, episodes, behavior_policy_player=None, 
                               target_policy_player=None, save_episodes=None, 
                               save_path='model', reset_random=True):
        if behavior_policy_player is None:
            behavior_policy_player = self.greedy_soft_target_policy_player
        if target_policy_player is None:
            target_policy_player = self.greedy_target_policy_player
        if save_episodes is None:
            save_episodes = [episodes] 
        if save_path is not None and not os.path.exists(save_path):
            os.makedirs(save_path)
               
        for i in tqdm(range(0, episodes)):
            _, player_trajectory = self.play(behavior_policy_player, )

            g = 0
            w = 1
            gamma = 0.1
            for state, action, _, _ in player_trajectory[::-1]:
                g = self.gamma*g + self.reward + self.acceleration_reward*np.sum(np.abs(action))
                if state not in self.c:
                    self.c[state] = {}
                if action not in self.c[state]:
                    self.c[state][action] = 0
                self.c[state][action] = self.c[state][action] + w
                if state not in self.q:
                    self.q[state] = {}
                if action not in self.q[state]:
                    self.q[state][action] = 0
                self.q[state][action]= self.q[state][action]+ w/self.c[state][action]*(g - self.q[state][action])
                if action != target_policy_player(state):
                    break
                w /= (1 - self.epsilon + self.epsilon/len(self.get_actions(state)))
            if (i+1) in save_episodes:
                self.save_q(self.q, q_path=os.path.join(save_path, f'{i+1}.pickle'))

if __name__ == '__main__':
    pass
