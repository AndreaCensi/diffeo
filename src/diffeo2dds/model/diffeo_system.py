from .diffeo_action import DiffeoAction
from .plan_utils import plan_friendly
from .uncertain_image import UncertainImage
from conf_tools.utils import raise_x_not_found
from contracts import contract
from diffeo2dds import logger
from diffeo2s.utils import construct_matrix
from reprep import Report
import numpy as np
import warnings
from diffeo2dds.configuration.config_master import get_conftools_uncertain_images


__all__ = ['DiffeoSystem']


class DiffeoSystem(object):
    """
        A DiffeoSystem is a set of discretized diffeomorphisms.
        
        It has a set of DiffeoAction.
        
        Each DiffeoAction keeps track of forward and backward diffeos.
    """
    @contract(label='str', actions='list')
    def __init__(self, label, actions):
        """
            :param label: A descriptive label for the system.
            :param actions: a list of DiffeoAction objects.
        """
        self.label = label
        self.actions = actions
        
        for a in actions:
            # TODO: check that the discretization is the same
            assert isinstance(a, DiffeoAction)

    def inverse(self):
        """ Returns the DiffeoSystem with all actions
            reversed. """
        label = self.label + '_inv'
        actions = map(DiffeoAction.inverse, self.actions)
        return DiffeoSystem(label, actions)

    @contract(returns='int,>=1')
    def get_num_commands(self):
        return len(self.actions)
    
    @contract(returns='tuple(int,int)')
    def get_shape(self):
        """ Returns the resolution of these diffeomorphisms. """
        return self.actions[0].diffeo.get_shape()

    @contract(plan_length='K,>=1', returns='list[K](int)')
    def get_random_plan(self, plan_length):
        """ 
            Returns a random plan of the given length 
            --- a sequence of integers 
            each corresponding to one command.
        """
        n = len(self.actions)
        if n == 1:
            rplan = np.zeros((plan_length,), 'int')
        else:
            rplan = np.random.randint(low=0, high=(n - 1), size=plan_length)
        return rplan.tolist() 

    @contract(plan='seq[>=0](int)', y0=UncertainImage, returns=UncertainImage)
    def predict(self, y0, plan):
        """ 
            Predicts the result of applying the given plan to the image. 
        """
        self.check_valid_plan(plan)
        y1 = y0
        for p in plan:
            action = self.actions[p]
            y1 = action.predict(y1)
        return y1
    
    @contract(returns=DiffeoAction)
    def get_identity_action(self):
        """ Returns the identity action for this system """
        shape = self.get_shape()
        warnings.warn('This is not entirely correct')
        identity_cmd = 0 * self.actions[0].get_original_cmds()[0]
        return DiffeoAction.identity('id', shape, identity_cmd)
        
    @contract(plan='seq[>=0](int)', returns=DiffeoAction)
    def plan2action(self, plan):
        """ Creates the DiffeoAction for the given composition. """
        if len(plan) == 0:
            return self.get_identity_action()
        
        self.check_valid_plan(plan)
        a = self.actions[plan[0]]
        for i in plan[1:]:  # big bug was found here 
            a_i = self.actions[i]
            a = DiffeoAction.compose(a, a_i)  # XXX: check
        return a
    
    def check_valid_plan(self, plan):
        """ 
            Checks that the plan contains integers in the correct range. 
            Raises ValueError if not.
        """
        for i in plan:
            if i < 0 or i >= len(self.actions):
                msg = ("Invalid plan %s as there are only %d actions. " % 
                       (str(plan), len(self.actions)))
                raise ValueError(msg) 
    
    @contract(us='list[N](array)', returns='list[N](int)')
    def commands_to_indices(self, us):
        """ Given the sequence of commands (e.g. [[0,0,+100], [0,100,0],...]),
            return the corresponding indices. """
        return [self.command_to_index(u) for u in us]
    
    @contract(u='array[K]', returns='int,>=0')
    def command_to_index(self, u):
        """ Return the index for a given command. """
        for i, action in enumerate(self.actions):
            same = np.all(action.original_cmd == u)
            if same:
                return i
            
        msg = 'Could not find action corresponding to command %s.\n' % str(u)
        msg += 'This DiffeoSystem has %s' % [a.original_cmd for a in self.actions]
        if True:
            raise ValueError(msg)
        else:
            logger.error(msg)
            logger.error('I will continue just because Andrea needs to debug '
                         'other code. I will return the command 0.')
            return 0
    
    @contract(plan='seq[N](int,>=0)', returns='list[>=N](array)')
    def indices_to_commands(self, plan):
        """ Converts from indices to the original commands. 
        
            Note that because one DiffeoAction can correspond to more
            than one commands, the result might have a longer length.
        """
        cmd = []
        for x in plan:
            x_cmds = self.actions[x].get_original_cmds()
            cmd.extend(x_cmds)
        return cmd
  
    @contract(report=Report)  # , image=UncertainImage)
    def display(self, report, image=None):
        '''
            Displays this diffeo system in a report.
        
            :param report: instance of reprep.Report to fill.
            :param image: RGB image to use as test.
        '''
        if image is None:
            image = get_conftools_uncertain_images().instance('lena')
        overview = 'Displaying a discrete DDS with %d actions' % len(self.actions)
        
        if self.actions:
            overview += '\nResolution: %s' % str(self.get_shape())
            
        report.text('overview', overview)
    
        for i, action in enumerate(self.actions):
            print('dds.display action: %d' % i)
            sec = report.section('action%d' % i)
            action.display(report=sec, image=image)
            
    @contract(returns='array[NxN](>=0)')
    def actions_distance(self, distance):
        def entries(i, j):
            a1 = self.actions[i]
            a2 = self.actions[j]
            return distance(a1, a2)
        K = len(self.actions)
        return construct_matrix((K, K), entries)

        
    def actions_distance_L2(self):
        from diffeo2dds.library import diffeoaction_distance_L2
        return self.actions_distance(diffeoaction_distance_L2)

    def actions_distance_L2_infow(self):
        from diffeo2dds.library import diffeoaction_distance_L2_infow
        return self.actions_distance(diffeoaction_distance_L2_infow)
    
    def actions_anti_distance_L2(self):
        from diffeo2dds.library import diffeoaction_anti_distance_L2
        return self.actions_distance(diffeoaction_anti_distance_L2)

    def actions_anti_distance_L2_infow(self):
        from diffeo2dds.library import diffeoaction_anti_distance_L2_infow
        return self.actions_distance(diffeoaction_anti_distance_L2_infow)
        
    def actions_comm_distance_L2(self):
        from diffeo2dds.library import diffeoaction_comm_distance_L2
        return self.actions_distance(diffeoaction_comm_distance_L2)
        
    def actions_comm_distance_L2_infow(self):
        from diffeo2dds.library import diffeoaction_comm_distance_L2_infow
        return self.actions_distance(diffeoaction_comm_distance_L2_infow)
    
    def plan_friendly_labels(self, plan):
        """ Returns a friendly string using the actions' labels """
        names = []
        # tmp fix for some previous mistake
        # TODO: remove
        for i, a in enumerate(self.actions):
            if 'Uninterpreted' in a.label:
                label = '%d' % i
            else:
                label = a.label
            names.append(label)
        # names = [a.label for a in self.actions]
        
        return plan_friendly(plan, names=names)
    
    @contract(label='str', returns='int,>=0')
    def index_from_label(self, label):
        """ Get the index of the action with a given label. """
        for i, a in enumerate(self.actions):
            if a.label == label:
                return i
        raise_x_not_found('label', label, [a.label for a in self.actions])
            
    @contract(labels='seq(str|int)', returns='tuple(int)')
    def plan_from_labels(self, labels):
        """ Converts a list of labels to the integer representation.
            It also accepts integers directly to mean the actions. 
         """
        def convert(x):
            if isinstance(x, int):
                if x < 0 or x >= len(self.actions):
                    msg = 'Invalid index %s in %s' % (x, labels)
                    raise ValueError(msg)
                return x
            return self.index_from_label(x) 
        return map(convert, labels)
    
    def plan_with_simple_actions(self, plan):
        """ Tries to write a plan using the simplest actions available
            instead of the composite ones. """
        # first convert to commands
        commands = self.indices_to_commands(plan)
        # print('commands: %s' % str(commands))
        # then assume each simple command has an action
        return tuple(self.commands_to_indices(commands)) 
            
            
