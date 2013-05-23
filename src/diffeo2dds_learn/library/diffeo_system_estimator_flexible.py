from contracts import contract
from diffeo2dds import DiffeoSystem
from diffeo2dds_learn import (get_diffeo2ddslearn_config, logger,
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
        
    @contract(returns=DiffeoActionEstimatorInterface)
    def new_estimator(self):
        """ Instances a new estimator. """
        config = get_diffeo2ddslearn_config()
        _, estimator = config.diffeoaction_estimators.instance_smarter(self.diffeo_action_estimator)
        return estimator            
                    
    @contract(returns='int', command='array')
    def command_index(self, command):
        command = tuple(command)
        # logger.info('Checking command %s in %r' % (str(command), self.command_list))
        # logger.info('%s' % str(command in self.command_list))
        
        if not command in self.command_list:    
            logger.info('Adding new command %s' % str(command))
            self.command_list.append(command)
            self.estimators.append(self.new_estimator())
            
        index = self.command_list.index(command)
        return index 
         
    @contract(i='int,>=0,i', n='int,>=1,>=i')
    def parallel_process_hint(self, i, n):
        self.parallel_hint = (i, n)
        
    def merge(self, other):
        """ 
            Merges the values obtained by "other" with ours. 
            Note that we don't make a deep copy of structures.
        """
        for i in range(len(self.command_list)):
            # Note that they are not necessarily in the right order.
            command = self.command_list[i]
            if not command in other.command_list:
                logger.info('The other does not have %s' % str(command))
                logger.info('Ours: %s' % self.command_list)
                logger.info('His:  %s' % other.command_list)
                continue
            
            j = other.command_list.index(command)
            
            self.estimators[i].merge(other.estimators[j])
            
        # Now add the ones we don't have.
        for j in range(len(other.command_list)):
            command = other.command_list[j]
            
            if command in self.command_list:
                    continue
                
            logger.info('Adding command %s' % str(command))
            self.command_list.append(command)
            self.estimators.append(other.estimators[j])
        
    def update(self, y0, u0, y1):
        cmd_ind = self.command_index(u0)
        
        if self.parallel_hint is not None:
            # check to see if we need to take care of this
            i, n = self.parallel_hint
            ours = cmd_ind % n == i
            if not ours:
                return
        
        est = self.estimators[cmd_ind]
        est.update(y0, y1)
                
    @contract(returns=DiffeoSystem)            
    def get_value(self, prefix=''):
        n = len(self.estimators)
        action_list = []
        for i in range(n):
            command = np.array(self.command_list[i])
            name = prefix + str(list(command)).replace(' ', '')
            
            try:
                action = self.estimators[i].get_value()
            except DiffeoActionEstimatorInterface.NotReady:
                logger.info('Skipping command %r %r' % (i, command))
                continue
                
            action.command = command
            action.label = name
                            
            action_list.append(action)
            
        name = 'Uninterpreted Diffeomorphism System'
        self.system = DiffeoSystem(name, action_list)
        return self.system
    
    def display(self, report): 
        for i in range(len(self.estimators)):
            logger.info('Report for %d-th action' % i)
            with report.subsection('d%d' % i) as sub:
                self.estimators[i].display(sub)
            
