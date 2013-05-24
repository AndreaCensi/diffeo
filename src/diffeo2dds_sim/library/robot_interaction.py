from bootstrapping_olympics import get_boot_config
from bootstrapping_olympics.misc import bd_sequence_from_robot_agent
from diffeo2dds_learn import Stream, LogItem
import itertools
from contracts import contract

__all__ = ['RobotInteractionStream']


class RobotInteractionStream(Stream):
    
    @contract(robot='str|code_spec', agent='str|code_spec',
              obs_per_episode='int,>=1')
    def __init__(self, robot, agent, obs_per_episode):
        """
        
        """
        boot_config = get_boot_config()
        self.id_robot, self.robot = boot_config.robots.instance_smarter(robot)
        self.id_agent, self.agent = boot_config.agents.instance_smarter(agent)
        if self.id_robot is None:
            self.id_robot = 'robot'
        if self.id_agent is None:
            self.id_agent = 'agent'
            
        self.obs_per_episode = obs_per_episode
            
    def read_all(self):
        """ Yields a LogItem sequence. """
        id_robot = self.id_robot
        robot = self.robot
        id_agent = self.id_agent
        agent = self.agent
        sleep_wait = 0
        
        agent.init(robot.get_spec())
        
        while True:
            episode_desc = robot.new_episode()
            id_environment = episode_desc.id_environment
            id_episode = episode_desc.id_episode
            bd_seq = bd_sequence_from_robot_agent(id_robot, robot, id_agent, agent,
                                     sleep_wait, id_episode, id_environment,
                                     check_valid_values=True)
    
            # number of observations in this episode
            nobs = 0
            for bd1, bd2 in pairwise(bd_seq):
                u = bd1['commands']
                y0 = bd1['observations']
                y1 = bd2['observations']
                log_item = LogItem(y0=y0, y1=y1, u=u, x0=None)
                yield log_item

                nobs += 1
                if nobs >= self.obs_per_episode:
                    break
            

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)
