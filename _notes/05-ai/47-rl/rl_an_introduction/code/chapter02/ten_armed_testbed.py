#######################################################################
# Copyright (C)                                                       #
# 2016-2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)             #
# 2016 Tian Jun(tianjun.cpp@gmail.com)                                #
# 2016 Artem Oboturov(oboturov@gmail.com)                             #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange
from joblib import Parallel, delayed

# Agg 渲染器是非交互式的后端，没有GUI界面，所以不显示图片，它是用来生成图像文件。
# matplotlib.use('Agg')


class Bandit:
    # @k_arm: # of arms
    # @epsilon: probability for exploration in epsilon-greedy algorithm
    # @initial: initial estimation for each action
    # @step_size: constant step size for updating estimations
    # @sample_averages: if True, use sample averages to update estimations instead of constant step size
    # @UCB_param: if not None, use UCB algorithm to select action
    # @gradient: if True, use gradient based bandit algorithm
    # @gradient_baseline: if True, use average reward as baseline for gradient based bandit algorithm
    # @random_walk_mean: 如果Bandit是非稳定的，该参数表示随机漫步的均值, 为了第二章2.5练习加的
    # @random_walk_sd: 如果Bandit是非稳定的，该参数表示随机漫步的标准方差, 为了第二章2.5练习加的
    def __init__(self, k_arm=10, epsilon=0., initial=0., step_size=0.1, sample_averages=False, UCB_param=None,
                 gradient=False, gradient_baseline=False, gradient_baseline_step_size=0, true_reward=0., 
                 random_walk_mean = None, random_walk_sd = None):
        self.k = k_arm
        self.step_size = step_size
        self.sample_averages = sample_averages
        self.indices = np.arange(self.k)
        self.time = 0
        self.UCB_param = UCB_param
        self.gradient = gradient
        self.gradient_baseline = gradient_baseline
        self.gradient_baseline_step_size = gradient_baseline_step_size
        self.gradient_baseline_reward = 0        
        self.average_reward = 0
        self.true_reward = true_reward
        self.epsilon = epsilon
        self.initial = initial
        self.random_walk_mean = random_walk_mean
        self.random_walk_sd = random_walk_sd
        if self.random_walk_mean is not None and self.random_walk_sd is not None:
            self.is_random_walk = True
        else:
            self.is_random_walk = False
            
    def to_string(self):
        attrs = []
        
        if self.true_reward > 0:
            attrs.append(f'true_reward={self.true_reward}')
        if self.is_random_walk:
            attrs.append(f'random_walk_mean={self.random_walk_mean}')
            attrs.append(f'random_walk_sd={self.random_walk_sd}')
        
        if self.epsilon <= 0:
            attrs.append(f'greedy')
        else:
            attrs.append(f'ε-greedy={self.epsilon}')        
        
        if self.UCB_param is not None:
            attrs.append(f'UCB_param={self.UCB_param}')            
        
        if self.gradient:             
            if self.gradient_baseline:  
                if self.gradient_baseline_step_size>0:
                    attrs.append(f'gradient_baseline_step_size={self.gradient_baseline_step_size}')  
                else:
                    attrs.append(f'gradient_baseline') 
            else:
                attrs.append(f'gradient')   
        
        if self.initial > 0:
            attrs.append(f'optimistic_initial={self.initial}')
            
        if self.sample_averages:
            attrs.append(f'sample_averages')
        else:
            attrs.append(f'step_size={self.step_size}')           
            
        attrs = ', '.join(attrs).strip()
        return f'Bandit({attrs})' 
                
    def random_walk(self):
        self.q_true = self.q_true + self.random_walk_mean + np.random.randn(self.k)*self.random_walk_sd     
        self.best_action = np.argmax(self.q_true)

    def reset(self):
        # real reward for each action
        self.init_q_true = np.random.randn(self.k) + self.true_reward
        self.q_true = self.init_q_true

        # estimation for each action
        self.init_q_estimation = np.zeros(self.k) + self.initial
        self.q_estimation = self.init_q_estimation

        # # of chosen times for each action
        self.action_count = np.zeros(self.k)

        self.best_action = np.argmax(self.q_true)

        self.time = 0
        self.average_reward = 0
        self.gradient_baseline_reward = 0  
        

    # get an action for this bandit
    def act(self):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.indices)

        if self.UCB_param is not None:
            UCB_estimation = self.q_estimation + \
                self.UCB_param * np.sqrt(np.log(self.time + 1) / (self.action_count + 1e-5))
            q_best = np.max(UCB_estimation)
            return np.random.choice(np.where(UCB_estimation == q_best)[0])

        if self.gradient:
            exp_est = np.exp(self.q_estimation)
            self.action_prob = exp_est / np.sum(exp_est)
            return np.random.choice(self.indices, p=self.action_prob)

        q_best = np.max(self.q_estimation)
        return np.random.choice(np.where(self.q_estimation == q_best)[0])

    # take an action, update estimation for this action
    def step(self, action):
        # generate the reward under N(real reward, 1)
        reward = np.random.randn() + self.q_true[action]
        self.time += 1
        self.action_count[action] += 1
        self.average_reward += (reward - self.average_reward) / self.time
        
        if self.sample_averages:
            # update estimation using sample averages
            self.q_estimation[action] += (reward - self.q_estimation[action]) / self.action_count[action]
        elif self.gradient:
            if self.gradient_baseline_step_size > 0:
                self.gradient_baseline_reward += self.gradient_baseline_step_size * (reward - self.gradient_baseline_reward) 
            else:
                self.gradient_baseline_reward = self.average_reward
            
            one_hot = np.zeros(self.k)
            one_hot[action] = 1
            if self.gradient_baseline:
                baseline = self.gradient_baseline_reward
            else:
                baseline = 0
            self.q_estimation += self.step_size * (reward - baseline) * (one_hot - self.action_prob)
        else:
            # update estimation with constant step size
            self.q_estimation[action] += self.step_size * (reward - self.q_estimation[action])
        return reward


def simulate(runs, time, bandits, n_jobs=5):    
    def simulate_one(bandit, i, j):
        bandit.reset()
        rewards = np.zeros(time)
        best_action_counts =np.zeros(time)
        for t in range(time):
            action = bandit.act()
            reward = bandit.step(action)
            if bandit.is_random_walk:
                bandit.random_walk()                
            rewards[t] = reward
            if action == bandit.best_action:
                best_action_counts[t] = 1   
        return rewards, best_action_counts, bandit
            
    rewards = np.zeros((len(bandits), runs, time))
    best_action_counts = np.zeros(rewards.shape)
    
    if n_jobs > runs:
        n_jobs = runs    

    for i, bandit in enumerate(bandits): 
        q_true = None
        q_estimation = None
        if n_jobs<=1:
            for r in trange(runs):
                re, be, bandit = simulate_one(bandit, i, r)
                rewards[i, r] = re
                best_action_counts[i, r] = be
        else:
            results = Parallel(n_jobs=n_jobs)(delayed(simulate_one)(bandit, i, r) for r in range(runs)) 
            for r, result in zip(range(runs), results):
                re, be, bandit = result
                rewards[i, r] = re
                best_action_counts[i, r] = be  
                
        last_half = int(time/2)
        mean_reward = np.mean(rewards[i,:,last_half:])                
        mean_best_action_count = np.mean(best_action_counts[i,:,last_half:])   
        print(f'{bandit.to_string()}\n    reward={mean_reward:0.02f}, best_action_rate={mean_best_action_count:0.02f}')
        if bandit.is_random_walk:
            print(f'    init_q_true={[round(q,2) for q in bandit.init_q_true]} \n    q_true={[round(q,2) for q in bandit.q_true]}')
 
    mean_best_action_counts = best_action_counts.mean(axis=1)
    mean_rewards = rewards.mean(axis=1)
    return mean_best_action_counts, mean_rewards


def figure_2_1(show=False):
    q = np.random.randn(10)
    plt.violinplot(dataset=np.random.randn(2000, 10) + q, showmeans=False)
    plt.scatter(range(1,len(q)+1), q, marker='_')
    for i in range(len(q)):
        plt.text(i+1+0.1, q[i], f'$q_*({i+1})$')
    plt.xlabel("Action")
    plt.ylabel("Reward distribution")
    plt.savefig('../images/figure_2_1.png')
    if show:
        plt.show()
#     plt.close()


def figure_2_2(runs=2000, time=1000, show=False, n_jobs=1):
    epsilons = [0, 0.1, 0.01]
    bandits = [Bandit(epsilon=eps, sample_averages=True) for eps in epsilons]
    best_action_counts, rewards = simulate(runs, time, bandits, n_jobs=n_jobs)

    plt.figure(figsize=(10, 20))

    plt.subplot(2, 1, 1)
    for eps, rewards in zip(epsilons, rewards):
        plt.plot(rewards, label='$\epsilon = %.02f$' % (eps))
    plt.xlabel('steps')
    plt.ylabel('average reward')
    plt.legend()

    plt.subplot(2, 1, 2)
    for eps, counts in zip(epsilons, best_action_counts):
        plt.plot(counts, label='$\epsilon = %.02f$' % (eps))
    plt.xlabel('steps')
    plt.ylabel('% optimal action')
    plt.legend()

    plt.savefig('../images/figure_2_2.png')
    if show:
        plt.show()
    plt.close()
    
def exercise_2_5(runs=2000, time=1000, show=False, n_jobs=1):
    bandits = []
    bandits.append(Bandit(epsilon=0.1, sample_averages=True, random_walk_mean=0, random_walk_sd=0.01))
    bandits.append(Bandit(epsilon=0.1, sample_averages=False, step_size=0.1, random_walk_mean=0, random_walk_sd=0.01))
    best_action_counts, rewards = simulate(runs, time, bandits, n_jobs=n_jobs)
    labels = ['sample_averages', r'$\alpha = 0.1$'] 

    plt.figure(figsize=(15, 15))

    plt.subplot(2, 1, 1)
    for label, rewards in zip(labels, rewards):
        plt.plot(rewards, label=label)
    plt.xlabel('steps')
    plt.ylabel('average reward')
    plt.legend()

    plt.subplot(2, 1, 2)
    for label, counts in zip(labels, best_action_counts):
        plt.plot(counts, label=label)
    plt.xlabel('steps')
    plt.ylabel('% optimal action')
    plt.legend()

    plt.savefig('../images/exercise_2_5.png')
    if show:
        plt.show()
    plt.close()    


def figure_2_3(runs=2000, time=1000, show=False, n_jobs=1):
    bandits = []
    bandits.append(Bandit(epsilon=0, initial=5, step_size=0.1))
    bandits.append(Bandit(epsilon=0.1, initial=0, step_size=0.1))
    best_action_counts, _ = simulate(runs, time, bandits, n_jobs=n_jobs)

    plt.plot(best_action_counts[0], label='$\epsilon = 0, q = 5$')
    plt.plot(best_action_counts[1], label='$\epsilon = 0.1, q = 0$')
    plt.xlabel('Steps')
    plt.ylabel('% optimal action')
    plt.legend()

    plt.savefig('../images/figure_2_3.png')
    if show:
        plt.show()
    
    plt.close()


def figure_2_4(runs=2000, time=1000, show=False, n_jobs=1):
    bandits = []
    bandits.append(Bandit(epsilon=0, UCB_param=2, sample_averages=True))
    bandits.append(Bandit(epsilon=0.1, sample_averages=True))
    _, average_rewards = simulate(runs, time, bandits, n_jobs=n_jobs)

    plt.plot(average_rewards[0], label='UCB $c = 2$')
    plt.plot(average_rewards[1], label='epsilon greedy $\epsilon = 0.1$')
    plt.xlabel('Steps')
    plt.ylabel('Average reward')
    plt.legend()

    plt.savefig('../images/figure_2_4.png')
    if show:
        plt.show()    
    plt.close()


def figure_2_5(runs=2000, time=1000, show=False, true_reward=4, n_jobs=1):
    bandits = []
    bandits.append(Bandit(gradient=True, step_size=0.1, gradient_baseline=True, true_reward=true_reward))
    bandits.append(Bandit(gradient=True, step_size=0.1, gradient_baseline=False, true_reward=true_reward))
    bandits.append(Bandit(gradient=True, step_size=0.4, gradient_baseline=True, true_reward=true_reward))
    bandits.append(Bandit(gradient=True, step_size=0.4, gradient_baseline=False, true_reward=true_reward))
    best_action_counts, _ = simulate(runs, time, bandits)
    labels = [r'$\alpha = 0.1$, with baseline',
              r'$\alpha = 0.1$, without baseline',
              r'$\alpha = 0.4$, with baseline',
              r'$\alpha = 0.4$, without baseline']

    for i in range(len(bandits)):
        plt.plot(best_action_counts[i], label=labels[i])
    plt.xlabel('Steps')
    plt.ylabel('% Optimal action')
    plt.legend()

    plt.savefig('../images/figure_2_5.png')
    if show:
        plt.show()
    plt.close()


def figure_2_6(runs=2000, time=1000, show=False, n_jobs=1):
    labels = ['ε-greedy sample_averages', 'ε-greedy', 'gradient bandit',
              'UCB', 'optimistic initialization']
    generators = [lambda epsilon: Bandit(epsilon=epsilon, sample_averages=True),
                  lambda epsilon: Bandit(epsilon=epsilon, sample_averages=False),
                  lambda alpha: Bandit(gradient=True, step_size=alpha, gradient_baseline=True),
                  lambda coef: Bandit(epsilon=0, UCB_param=coef, sample_averages=True),
                  lambda initial: Bandit(epsilon=0, initial=initial, step_size=0.1)]
    parameters = [np.arange(-7, -1, dtype=np.float),
                  np.arange(-7, -1, dtype=np.float),
                  np.arange(-5, 2, dtype=np.float),
                  np.arange(-4, 3, dtype=np.float),
                  np.arange(-2, 3, dtype=np.float)]

    bandits = []
    for generator, parameter in zip(generators, parameters):
        for param in parameter:
            bandits.append(generator(pow(2, param)))

    _, average_rewards = simulate(runs, time, bandits, n_jobs=n_jobs)
    # 仅计算最后一半时间的平均奖励
    last_half = int(time/2)
    rewards = np.mean(average_rewards[:,last_half:], axis=1)

    i = 0
    for label, parameter in zip(labels, parameters):
        l = len(parameter)
        plt.plot(parameter, rewards[i:i+l], label=label)
        i += l
    plt.xlabel('Parameter($2^x$)')
    plt.ylabel('Average reward')
    plt.legend()

    plt.savefig('../images/figure_2_6.png')
    if show:
        plt.show()
    plt.close()
    
def exercise_2_11(runs=2000, time=1000, show=False, n_jobs=1):
    labels = ['ε-greedy sample_averages', 'ε-greedy', 'gradient bandit', 'gradient with baseline_step_size',
              'UCB sample_averages', 'UCB', 'optimistic initialization']
    generators = [lambda epsilon: Bandit(epsilon=epsilon, sample_averages=True, random_walk_mean=0, random_walk_sd=0.01),
                  lambda epsilon: Bandit(epsilon=epsilon, sample_averages=False, random_walk_mean=0, random_walk_sd=0.01),
                  lambda alpha: Bandit(gradient=True, step_size=alpha, gradient_baseline=True, random_walk_mean=0, random_walk_sd=0.01),
                  lambda alpha: Bandit(gradient=True, step_size=alpha, gradient_baseline=True, gradient_baseline_step_size=0.1, random_walk_mean=0, random_walk_sd=0.01),
                  lambda coef: Bandit(epsilon=0, UCB_param=coef, sample_averages=True, random_walk_mean=0, random_walk_sd=0.01),
                  lambda coef: Bandit(epsilon=0, UCB_param=coef, sample_averages=False, random_walk_mean=0, random_walk_sd=0.01),
                  lambda initial: Bandit(epsilon=0, initial=initial, step_size=0.1, random_walk_mean=0, random_walk_sd=0.01)]
    parameters = [np.arange(-7, -1, dtype=np.float),
                  np.arange(-7, -1, dtype=np.float),
                  np.arange(-5, 2, dtype=np.float),
                  np.arange(-5, 2, dtype=np.float),
                  np.arange(-4, 3, dtype=np.float),
                  np.arange(-4, 3, dtype=np.float),
                  np.arange(-2, 3, dtype=np.float)]

    bandits = []
    for generator, parameter in zip(generators, parameters):
        for param in parameter:
            bandits.append(generator(pow(2, param)))

    _, average_rewards = simulate(runs, time, bandits, n_jobs=n_jobs)
    # 仅计算最后一半时间的平均奖励
    last_half = int(time/2)
    rewards = np.mean(average_rewards[:,last_half:], axis=1)

    i = 0
    for label, parameter in zip(labels, parameters):
        l = len(parameter)
        plt.plot(parameter, rewards[i:i+l], label=label)
        i += l
    plt.xlabel('Parameter($2^x$)')
    plt.ylabel('Average reward')
    plt.legend()

    plt.savefig('../images/exercise_2_11.png')
    if show:
        plt.show()
    plt.close()
        


if __name__ == '__main__':
    figure_2_1()
    figure_2_2()
    figure_2_3()
    figure_2_4()
    figure_2_5()
    figure_2_6()
