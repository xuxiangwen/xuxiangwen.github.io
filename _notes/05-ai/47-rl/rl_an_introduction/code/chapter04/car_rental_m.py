import numpy as np

class State:
    def __init__(self, first_car_num, second_car_num):
        self.first_car_num = first_car_num
        self.second_car_num = second_car_num

class JackRental:
    def __init__(self, max_car_num=20, max_move_car_num=5, 
                 car_rent_lambda=(3, 4), car_return_lambda=(3, 2),
                 rent_reward=10, move_reward=-2, 
                 return_reward=0, send_back_reward=0,
                 discount=0.9, theta=1e-4):
        self.max_car_num = max_car_num
        self.max_move_car_num = max_move_car_num
        self.car_rent_lambda = car_rent_lambda
        self.car_return_lambda = car_return_lambda
        self.rent_reward = rent_reward
        self.move_reward = move_reward
        self.return_reward = return_reward
        self.send_back_reward = send_back_reward
        self.discount = discount
        self.theta = theta

    def get_move_actions(self, state):
        actions = []
        first_max_num = min(self.max_move_car_num, state[0])
        second_max_num = min(self.max_move_car_num, state[1])
        actions = list(range(0, first_max_num+1)) + list(range(-second_max_num, 0)) 
        return np.array(actions)
    
    def send_back(self,state):
        send_back_num = 0
        for i in range(len(state)):
            if state[i] > self.max_car_num:
                send_back_num = state[i] - self.max_car_num  
                state[i] = self.max_car_num
        return state, send_back_num*self.send_back_reward
             
    
    def rent(self, state):
        def rent_(car_num, rent_lambda):
            rent_num =  np.random.poisson(lam=rent_lambda)
            rent_num = min(rent_num, car_num) 
            car_num -= rent_num
            return car_num, self.rent_reward*rent_num
        
        reward = 0
        for i in range(len(state)):
            state[i], r = rent_(state[i], self.car_rent_lambda[i])
            reward += r 
        
        return state, reward
            
    def return_(self, state):
        def return__(car_num, return_lambda):
            return_num =  np.random.poisson(lam=return_lambda)
            car_num += return_num
            return car_num, self.return_reward*return_num
        
        reward = 0
        for i in range(len(state)):
            state[i], r = return__(state[i], self.car_return_lambda[i])
            reward += r    

        return state, reward     
        
    
    def move(self, state, move_car_num):
        if move_car_num == 0:  
            return self

        state[0] -= move_car_num
        state[1] += move_car_num     

        return state, abs(move_car_num)*self.move_reward   
    
    def run(self):
        # Initialization
        v = np.zeros((self.max_car_num, self.max_car_num))
        pi = np.zeros((self.max_car_num, self.max_car_num)) * np.nan 
        for i in range(self.max_car_num):
            for j in range(self.max_car_num):  
                state = (i, j)  
                pi[state] = np.array([])

        discount = self.discount
        k = 0
        while True:
            # Policy Evaluation
            while True:
                k = k + 1
                delta = 0
                new_v = np.zeros_like(v)
                for i in range(self.max_car_num):
                    for j in range(self.max_car_num):  
                        state = (i, j)                                    
                        actions = self.get_move_actions(state)
                        if np.isnan(pi[i,j]):
                            action = np.random.choice(actions)
                        else:
                            action = int(pi[i,j])
                        reward = 0
                        next_state, r = self.move(state, action)
                        reward += r
                        next_state, r = self.rent(next_state)
                        reward += r
                        next_state, r = self.return_(next_state) 
                        reward += r  
                        new_v[i, j] += reward + discount * v[next_state[0], next_state[1]]   
                        delta = max(delta, abs(new_v[i, j]-v[i,j])) 
                v = new_v
                if delta < self.theta:
                    break
            
            # Policy Improvement
            is_stable = True
            for i in range(self.max_car_num):
                for j in range(self.max_car_num):  
                    state = (i, j)                                    
                    actions = self.get_move_actions(state)    

                    actions_values = []
                    for action in actions:  
                        reward = 0
                        next_state, r = self.move(state, action)
                        reward += r
                        next_state, r = self.rent(next_state)
                        reward += r
                        next_state, r = self.return_(next_state) 
                        reward += r                                        
                        actions_values.append(reward + discount * v[next_state[0], next_state[1]])
                    old_action = int(pi[i, j])
                    action = actions[np.argmax(actions_values)]
                    pi[i, j] = action
                    if old_action != action:
                        is_stable = False
            if is_stable:
                break
        




                    # action_prob = 1/len(actions)
                    # for action in actions:
                    #     reward = 0
                    #     next_state, r = self.move(state, action)
                    #     reward += r
                    #     next_state, r = self.rent(next_state)
                    #     reward += r
                    #     next_state, r = self.return_(next_state) 
                    #     reward += r  
                    #     new_v[i, j] += action_prob * (reward + discount * v[next_state[0], next_state[1]])  
            




                    





    





if __name__ == '__main__':
    rental = JackRental()
    print(f'rental.get_actions(5, 4) = {rental.get_actions(5, 4)}')
    print(f'rental.get_actions(17, 16) = {rental.get_actions(17, 16)}')

