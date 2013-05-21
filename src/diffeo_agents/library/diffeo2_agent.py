from bootstrapping_olympics import (AgentInterface, UnsupportedSpec,
    get_boot_config)
from contracts import contract
from diffeo2dds_learn import get_diffeo2ddslearn_config
import numpy as np


__all__ = ['Diffeo2Agent']

class Diffeo2Agent(AgentInterface):
    '''
    
    '''
    
    @contract(explorer='string|code_spec',
              estimator='string|code_spec')
    def __init__(self, explorer, estimator, servo): 
        '''
        
        :param explorer: Explorer agent
        :param estimator: resolves to a DiffeoSystemEstimatorInterface
        :param servo: todo
        '''
        self.explorer_spec = explorer
        self.estimator_spec = estimator
        self.servo_spec = servo
        
    def init(self, boot_spec):
        if len(boot_spec.get_observations().shape()) != 2:
            msg = 'This agent can only work with 2D signals.'
            raise UnsupportedSpec(msg)

        estimators = get_diffeo2ddslearn_config().diffeosystem_estimators 
        _, self.diffeosystem_estimator = estimators.instance_smarter(self.estimator_spec)
        
        # initialize explorer
        agents = get_boot_config().agents
        _, self.explorer = agents.instance_smarter(self.explorer)
        self.explorer.init(boot_spec)
        
    def process_observations(self, obs):
 
        self.diffeosystem_estimator.update(y0=y0, u0=u0, y1=y1)
        
    def choose_commands(self):
        return self.explorer.choose_commands()

    def publish(self, pub):

        if self.last_data is not None:
            y0 = self.last_data.y0
            y1 = self.last_data.y1
            none = np.logical_and(y0 == 0, y1 == 0)
            x = y0 - y1
            x[none] = np.nan

            pub.array_as_image('y0', y0, filter='scale')
            pub.array_as_image('y1', y1, filter='scale')
            pub.array_as_image('motion', x, filter='posneg')

        if self.diffeo_dynamics.commands2dynamics:  # at least one
            de = self.diffeo_dynamics.commands2dynamics[0]
            field = de.get_similarity((10, 10))
            pub.array_as_image('field', field)

        self.diffeo_dynamics.publish(pub.section('commands'))



