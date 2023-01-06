#Author: Changjae Han
#Class: CS540
#Date: Dec 11 2022


import gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict


EPISODES =  20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0

if __name__ == "__main__":

    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v1")
    env.seed(1)
    env.action_space.np_random.seed(1)


    # You will need to update the Q_table in your iteration
    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()

        ##########################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING ABOVE THIS LINE
        # TODO: Replace the following with Q-Learning

        while (not done): #if not done

            #two cases that whether value from random generator is less than EPSILON or not 
            if random.uniform(0,1) < EPSILON:
                action = env.action_space.sample()
            else:
                prediction = np.array([Q_table[(obs,i)] for i in range(env.action_space.n)])
                action =  np.argmax(prediction)

            new_obs,reward,done,info = env.step(action) #make step
            episode_reward += reward # update episode reward 

            prediction = np.array([Q_table[(new_obs,i)] for i in range(env.action_space.n)]) #make new prediction for new_obs

            # Find max_Q value by using np.argmax
            max_Q = prediction[np.argmax(prediction)]

            Q_table[(obs,action)] = (1 - LEARNING_RATE) * Q_table[(obs,action)] + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_Q) #update Q_table

            obs = new_obs #update obs

        Q_table[(obs,action)] = (1 - LEARNING_RATE) * Q_table[(obs,action)] + LEARNING_RATE * reward #if done
        
        EPSILON = EPSILON * EPSILON_DECAY #update EPSILON

        # END of TODO
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE
        ##########################################################

        # record the reward for this episode
        episode_reward_record.append(episode_reward) 

        
        if i%100 ==0 and i>0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    #### DO NOT MODIFY ######
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    model_file.close()
    #########################
