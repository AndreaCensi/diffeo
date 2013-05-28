from contracts import contract
from diffeo2dds import DiffeoSystem
from diffeo2dds_learn import (get_diffeo2ddslearn_config,
    DiffeoSystemEstimatorInterface, DiffeoActionEstimatorInterface)
import numpy as np


__all__ = ['DiffeoSystemEstimatorFlexible']


class DiffeoSystemEstimatorFlexible(DiffeoSystemEstimatorInterface):
    '''
        This estimator can use an arbitrary DiffeoActionEstimator. 
    '''

    @contract(diffeo_action_estimator='str|code_spec')    
    def __init__(self, diffeo_action_estimator):
        '''

        '''
        self.command_list = []
        self.estimators = []
        
        self.diffeo_action_estimator = diffeo_action_estimator
        
        # becomes (i, n) if parallel_process_hint is called
        self.parallel_hint = None   
    
    def set_max_displ(self, max_displ): 
        self.max_displ = max_displ
        
    @contract(returns=DiffeoActionEstimatorInterface)
    def new_estimator(self):
        """ Instances a new estimator. """
        c = get_diffeo2ddslearn_config()
        _, estimator = \
        c.diffeoaction_estimators.instance_smarter(self.diffeo_action_estimator)
        estimator.set_max_displ(self.max_displ)
        return estimator            
                    
    @contract(returns='int', command='array')
    def command_index(self, command):
        command = tuple(command)
        
        if not command in self.command_list:    
            self.command_list.append(command)
            self.estimators.append(None)
            index = self.command_list.index(command)
            self.info('Adding new command #%d %s' % (index, str(command)))
            
        index = self.command_list.index(command)
        return index 
         
    @contract(i='int,>=0,i', n='int,>=1,>=i')
    def parallel_process_hint(self, i, n):
        self.parallel_hint = (i, n)
        
        
    def summary(self):
        s = 'Summary:'
        s += '\n parallel hint: %r' % str(self.parallel_hint)
        for i, command in enumerate(self.command_list):
            s += '\n #%s - %s - %s' % (i, command, self.estimators[i])
        return s
    
    def merge(self, other):
        """ 
            Merges the values obtained by "other" with ours. 
            Note that we don't make a deep copy of structures.
        """
        self.info('merging')
        self.info('self: ' + self.summary())
        self.info('other: ' + other.summary())
        if self.parallel_hint is not None:
            ilist, n = self.parallel_hint
            if not isinstance(ilist, list):
                ilist = list([ilist])
            jlist, _ = other.parallel_hint
            if not isinstance(jlist, list):
                jlist = list([jlist])
            ilist.extend(jlist)
            self.parallel_hint = ilist, n
                
        for i, command in enumerate(self.command_list):
            # Note that they are not necessarily in the right order.
            command = self.command_list[i]
            if not command in other.command_list:
                self.info('The other does not have %s' % str(command))
                self.info('Ours: %s' % self.command_list)
                self.info('His:  %s' % other.command_list)
                continue
            
            j = other.command_list.index(command)
            
            a = self.estimators[i] is not None
            b = other.estimators[j] is not None
            if a and b:
                self.info('merging i = %d  j = %d command = %s' % (i, j, command))
                self.estimators[i].merge(other.estimators[j])
            elif a and not b:
                pass
            elif b and not a:
                self.estimators[i] = other.estimators[j]
            else:
                pass
            
        # Now add the ones we don't have.
        for j in range(len(other.command_list)):
            command = other.command_list[j]
            
            if command in self.command_list:
                    continue
                
            self.info('Adding command %s' % str(command))
            self.command_list.append(command)
            self.estimators.append(other.estimators[j])
    
    def _should_estimate_this(self, u):
        cmd_ind = self.command_index(u)
        if self.parallel_hint is None:
            return True
        else:
            # check to see if we need to take care of this
            i, n = self.parallel_hint
            ours = cmd_ind % n == i
            return ours
        
    
    def update(self, y0, u0, y1):
        if not self._should_estimate_this(u0):
            return
        
        cmd_ind = self.command_index(u0)
        if self.estimators[cmd_ind] is None:
            self.estimators[cmd_ind] = self.new_estimator()
            self.log_add_child('action%d_est' % cmd_ind, self.estimators[cmd_ind])
            
        est = self.estimators[cmd_ind]
        est.update(y0, y1)
                
    @contract(returns=DiffeoSystem)            
    def get_value(self, prefix=''):
        n = len(self.estimators)
        action_list = []
        for i in range(n):
            command = np.array(self.command_list[i])
            name = prefix + str(list(command)).replace(' ', '')
            
            if self.estimators[i] is None:
                continue
                
            try:
                action = self.estimators[i].get_value()
            except DiffeoActionEstimatorInterface.NotReady as e:
                self.info('Skipping command %r %r: %s' % (i, command, e))
                continue
            
            action.original_cmd = command
            action.label = name                            
            action_list.append(action)
            
        if not action_list:
            msg = 'No diffeo actions are ready yet.'
            self.warn(msg)
            # raise DiffeoActionEstimatorInterface.NotReady(msg)
        
        name = 'Uninterpreted Diffeomorphism System'
        self.system = DiffeoSystem(name, action_list)
        return self.system
    
    def display(self, report): 
        for i, est in enumerate(self.estimators):
            self.info('Report for %d-th action' % i)
            with report.subsection('d%d' % i) as sub:
                sub.text('command', str(self.command_list[i]))
                if est is None:
                    sub.text('warn', 'Action for this command was not'
                             'estimated - parallel hint %s' 
                             % str(self.parallel_hint))
                else:
                    self.estimators[i].display(sub)
            
