from bootstrapping_olympics import (RobotInterface, RobotObservations,
    EpisodeDesc, BootSpec, StreamSpec)
from bootstrapping_olympics.interfaces.streamels import (
    make_streamels_finite_commands, make_streamels_rgb_float)
from bootstrapping_olympics.utils.dates import unique_timestamp_string
from contracts import contract
from diffeo2dds import get_diffeo2dds_config
from diffeo2dds.model.uncertain_image import UncertainImage
from diffeo2dds_learn import get_diffeo2ddslearn_config
import numpy as np
import time
import warnings


__all__ = ['DiffeoSystemSimulation']


class DiffeoSystemSimulation(RobotInterface):
    """ 
        Simulation of a DiffeoSystem as a RobotInterface.
    """
    
    def __init__(self, image_stream, discdds):
        '''
        :param id_discdds: Which DDS dynamics to use.
        
        :param id_image_stream: What ImageStream to use. Each 
        image is used to start a new episode.
        
        '''
        diffeo2ddslearn_config = get_diffeo2ddslearn_config()
        self.id_image_stream, self.image_stream = \
            diffeo2ddslearn_config.image_streams.instance_smarter(image_stream)
        if self.id_image_stream is None:
            self.id_image_stream = 'image_stream'
            
        diffeo2dds_config = get_diffeo2dds_config() 
        self.id_discdds, self.discdds = \
            diffeo2dds_config.discdds.instance_smarter(discdds)

        if self.id_discdds is None:
            self.id_discdds = 'discdds'
            
        # get the first image, look how it is to get shape
        self.images = self.image_stream.read_all() 
        x0 = self.images.next()
        self.shape = x0.shape[:2] 
        
        
    @contract(returns=BootSpec)
    def get_spec(self):
        ncmds = self.discdds.get_num_commands()
        cmd = make_streamels_finite_commands(ncommands=ncmds, default=0)
        cmd_spec = StreamSpec(id_stream=None, streamels=cmd, extra={})
        obs_spec = StreamSpec(id_stream=None,
                              streamels=make_streamels_rgb_float(self.shape),
                              extra={})
        return BootSpec(obs_spec, cmd_spec)
    
    @contract(returns=EpisodeDesc)
    def new_episode(self):
        # initialize the state
        rgb = self.images.next()
        # TODO: reshape
        self.y = UncertainImage(rgb)
        id_environment = self.id_image_stream
        id_episode = unique_timestamp_string()
        self.timestamp = time.time()
        self.commands = np.array([0], dtype='int')
        self.commands_source = 'rest'
        return EpisodeDesc(id_episode, id_environment, extra=None)
        
    @contract(commands='array', commands_source='str')
    def set_commands(self, commands, commands_source):  # @UnusedVariable
        u = int(commands[0])
        warnings.warn('understand what was going on')
        self.y = self.discdds.predict(self.y, plan=[u])
        self.commands = commands
        self.commands_source = commands_source
        self.timestamp += 1
        
    @contract(returns=RobotObservations)
    def get_observations(self):
        rgb = self.y.get_values()
        timestamp = self.timestamp 
        observations = rgb
        commands = self.commands
        commands_source = self.commands_source
        episode_end = False
        robot_pose = None
        obs = RobotObservations(timestamp, observations,
                                commands, commands_source,
                                episode_end, robot_pose)
        return obs
    
    
    
