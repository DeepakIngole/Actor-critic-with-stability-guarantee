import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env

class AntEnv_cost(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        self.des_v = 1.
        mujoco_env.MujocoEnv.__init__(self, 'ant.xml', 5)
        utils.EzPickle.__init__(self)

    def step(self, a):
        xposbefore = self.get_body_com("torso")[0]
        self.do_simulation(a, self.frame_skip)
        xposafter = self.get_body_com("torso")[0]
        forward_reward = (xposafter - xposbefore)/self.dt
        v = (xposafter - xposbefore) / self.dt
        run_cost = np.square(v - self.des_v)
        ctrl_cost = .5 * np.square(a).sum()
        contact_cost = 0.5 * 1e-3 * np.sum(
            np.square(np.clip(self.sim.data.cfrc_ext, -1, 1)))
        survive_reward = 1.0
        # reward = forward_reward - ctrl_cost - contact_cost + survive_reward
        reward = run_cost #+ ctrl_cost
        state = self.state_vector()
        # notdone = np.isfinite(state).all() \
        #     and state[2] >= 0.2 and state[2] <= 1.0
        # done = not notdone
        done = False
        ob = self._get_obs()
        l_rewards = max(abs(forward_reward)-0.9*3, 0)**2
        if abs(forward_reward)>3:
            violation_of_constraint = 1
        else:
            violation_of_constraint = 0
        self.l_rewards = l_rewards#- ctrl_cost - contact_cost + survive_reward
        # print(xposafter)
        return ob, reward,done, dict(
            reward_forward=forward_reward,
            violation_of_constraint=violation_of_constraint,
            reward_ctrl=-ctrl_cost,
            reward_contact=-contact_cost,
            reward_survive=survive_reward,
            l_rewards=self.l_rewards,
            reference=self.des_v,
            state_of_interest=v,
            )

    def _get_obs(self):
        return np.concatenate([
            self.sim.data.qpos.flat[2:],
            self.sim.data.qvel.flat,
            np.clip(self.sim.data.cfrc_ext, -1, 1).flat,
        ])

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(size=self.model.nq, low=-.1, high=.1)
        qvel = self.init_qvel + self.np_random.randn(self.model.nv) * .1
        self.set_state(qpos, qvel)
        return self._get_obs()

    def viewer_setup(self):
        self.viewer.cam.distance = self.model.stat.extent * 0.5
