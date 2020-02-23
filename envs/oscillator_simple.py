"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from http://incompleteideas.net/sutton/book/code/pole.c
permalink: https://perma.cc/C9ZM-652R
"""

import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import csv
import matplotlib.pyplot as plt

class oscillator(gym.Env):

    def __init__(self):
        self.p1 = 1.0
        self.p2 = 1.0
        self.p3 = 1.0
        self.dt = 1.
        self.t = 0
        # Angle limit set to 2 * theta_threshold_radians so failing observation is still within bounds
        high = np.array([1, 1, 1])

        self.action_space = spaces.Box(low=np.array([-10.]), high=np.array([10.]), dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]



    def step(self, action, impulse=0, process_noise=np.zeros([6])):

        u1, u2 = action

        m1, m2, m3, p1, p2, p3 = self.state
        m1_dot = self.c1 / (1 + np.square(p3)) - self.c2 * m1 + self.b1 * u1
        p1_dot = self.c3 * m1 - self.c4*p1

        m2_dot = self.c1 / (1 + np.square(p1)) - self.c2 * m2 + self.b2 * u2
        p2_dot = self.c3 * m2 - self.c4 * p2

        m3_dot = self.c1 / (1 + np.square(p2)) - self.c2 * m3
        p3_dot = self.c3 * m3 - self.c4 * p3

        m1 = m1 + m1_dot * self.dt
        m2 = m2 + m2_dot * self.dt
        m3 = m3 + m3_dot * self.dt

        p1 = p1 + p1_dot * self.dt
        p2 = p2 + p2_dot * self.dt
        p3 = p3 + p3_dot * self.dt

        self.state = np.array([m1, m2, m3, p1, p2, p3])
        self.t = self.t + 1
        r1, r2 = self.reference(self.t)
        cost =   np.square(p1-r1) + 1 * np.square(p2-r2) #+ 0.05 *u1 + 0.05* u2
        done = False
        return np.array([m1, m2, m3, p1, p2, p3, r1, r2]), cost, done, dict()

    def reset(self):
        self.state = self.np_random.uniform(low= 0, high=5, size=(6,))
        # self.state = np.array([1,2,3,1,2,3])
        self.t = 0
        m1, m2, m3, p1, p2, p3 = self.state
        r1, r2 = self.reference(self.t)
        # self.state[0] = self.np_random.uniform(low=5, high=6)
        return np.array([m1, m2, m3, p1, p2, p3, r1, r2])

    def reference(self, t):
        r1 = 8+7*np.sin((2*np.pi)*t/200)
        r2 = 8+7*np.sin((2*np.pi)*(t + 200/3)/200)
        return r1, r2

    def reference2(self, t):
        r1 = 8
        r2 = 8 + 7 * np.sin((2 * np.pi) * (t + 200 / 3) / 200)
        return r1, r2

    def render(self, mode='human'):

        return


if __name__=='__main__':
    env = oscillator()
    T = 600
    path = []
    t1 = []
    s = env.reset()
    for i in range(int(T/env.dt)):
        s, r, done, info = env.step(np.array([0,0]))
        path.append(s)
        t1.append(i * env.dt)

    # path2 = []
    # t2 = []
    # env.dt = 1
    # s = env.reset()
    # for i in range(int(T / env.dt)):
    #     s, r, done, info = env.step(np.array([0, 0]))
    #     path2.append(s)
    #     t2.append(i * env.dt)
    #
    # path3 = []
    # t3 = []
    # env.dt = 0.01
    # s = env.reset()
    # for i in range(int(T / env.dt)):
    #     s, r, done, info = env.step(np.array([0, 0]))
    #     path3.append(s)
    #     t3.append(i * env.dt)
    #
    # path4 = []
    # t4 = []
    # env.dt = 0.001
    # s = env.reset()
    # for i in range(int(T / env.dt)):
    #     s, r, done, info = env.step(np.array([0, 0]))
    #     path4.append(s)
    #     t4.append(i * env.dt)

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111)
    ax.plot(t1, path, color='blue', label='0.1')
    # ax.plot(t2, path2, color='red',label='1')
    #
    # ax.plot(t3, path3, color='black', label='0.01')
    # ax.plot(t4, path4, color='orange', label='0.001')
    handles, labels = ax.get_legend_handles_labels()

    ax.legend(handles, labels, loc=2, fancybox=False, shadow=False)
    plt.show()
    print('done')




