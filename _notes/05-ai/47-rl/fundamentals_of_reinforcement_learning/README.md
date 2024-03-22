# Week 1

课程作业

- [Assignment1.ipynb](C:\xujian\eipi10\xuxiangwen.github.io\_notes\05-ai\47-rl\fundamentals_of_reinforcement_learning\week1\Bandits\Assignment1.ipynb)

## Week 2

### My Ideas

Ideas of MDP:

- buying and selling a single stock. 
  - states 
    - cash
    - the number of shares owned
    - current total capital (equal to cash + market value of owned shares)
    - stock purchase price
    - recent price
    - recent trading volume

  - actions ： Assuming only one action can be taken per day
    - buying
    - selling
    - waiting (that is, not making any transactions). 

  - rewards
    - buying has a reward of 0
    - selling results in a profit or loss
    - waiting for a day has a reward of -0.01% of the current total capital. 

-  Gomoku (also known as Five-in-a-Row). 
  - states 
    - the positions of all the pieces placed by both players. 

  - action
    - placing a piece. 

  - rewards 
    - winning the game results in a reward of 3, 
    - drawing the game results in a reward of 1
    - and losing the game results in a reward of 0.  

-  precise automatic irrigation system for plants. 
  - states
    - temperature
    - soil moisture
    - predicted rainfall for the next two days. The 

  - actions
    - watering 
    - waiting

  - rewards 
    - a penalty of -1 when the soil moisture exceeds the rated range
    - plant growth assessments.  


# Week 4

课程作业

- [Assignment2.ipynb](C:\xujian\eipi10\xuxiangwen.github.io\_notes\05-ai\47-rl\fundamentals_of_reinforcement_learning\week4\DynamicProgramming\Assignment2.ipynb)

