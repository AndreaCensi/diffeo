from .uncertain_image import UncertainImage
from contracts import contract
from diffeo2d import Diffeomorphism2D
from reprep import Report
import warnings
    
__all__ = ['DiffeoAction']


class DiffeoAction(object):
    """ 
        An "action" is described by a pair of diffeomorphism.
        
    """
    @contract(diffeo=Diffeomorphism2D,
              diffeo_inv=Diffeomorphism2D,
              label=str,
              original_cmd='None|array|list[>=1](array)')
    def __init__(self, label, diffeo, diffeo_inv, original_cmd):
        """
            :param label: A descriptive label for the command.
            :param diffeo: The diffeomorphism.
            :param diffeo_inv: The inverse of the diffeomorphism.
            :param original_cmd: A list of original commands (e.g. [[0,100],[0,100]])
        """
        self.label = label
        self.diffeo = diffeo
        self.diffeo_inv = diffeo_inv
        self.original_cmd = original_cmd
    
    def __str__(self):
        return "DiffeoAction(%s, %s)" % (self.label, self.get_original_cmds())
    
    def inverse(self):
        """ Return the action with swapped diffeomorphisms. """
        # label = '(i%s)' % self.label
        # let's just use the same label
        label = self.label
        
        diffeo = self.diffeo_inv  # <-- note swapped
        diffeo_inv = self.diffeo  # <-- note swapped
        cmd = [-x for x in self.get_original_cmds()]
        return DiffeoAction(label, diffeo, diffeo_inv, cmd)
    
    def __sizeof__(self):
        """ Returns approximate size in bytes. """
        m = 0
        m += self.diffeo.__sizeof__()
        m += self.diffeo_inv.__sizeof__()
        return m

    @staticmethod
    def identity(label, shape, original_cmd):
        """ Constructs the identity action of the given shape. """
        diffeo = Diffeomorphism2D.identity(shape)
        diffeo_inv = diffeo
        return DiffeoAction(label, diffeo, diffeo_inv, original_cmd)
    
    @contract(returns=Diffeomorphism2D)
    def get_diffeo2d_forward(self):
        return self.diffeo
    
    @contract(returns=Diffeomorphism2D)
    def get_diffeo2d_backward(self):
        return self.diffeo_inv
    
    @contract(returns='list[>=1](array)')
    def get_original_cmds(self):
        """ Returns the commands as a list """
        if isinstance(self.original_cmd, list):
            return self.original_cmd
        else:
            return [self.original_cmd]
        
    @contract(y0=UncertainImage, returns=UncertainImage)
    def predict(self, y0, apply_function='self.diffeo.apply'):
        """ 
            Returns the prediction of applying this action to the 
            given input y0. 
        """
        warnings.warn('remove this hack!')
        apply_function = eval(apply_function) 
        y1, var1 = apply_function(y0.get_values(),
                                     y0.scalar_uncertainty)
        return UncertainImage(y1, var1) 
        
    @contract(report=Report)
    def display(self, report, image=None):  # @UnusedVariable
        report.text('summary', 'Label: %s\noriginal: %s' % 
                    (self.label, self.original_cmd))
        report.data('label', self.label)
        report.data('original_cmd', self.original_cmd)
        
        with report.subsection('forward') as s1:
            self.diffeo.display(s1)
             
        with report.subsection('backward') as s2:
            self.diffeo_inv.display(s2)
            
        if image is not None:
            with report.subsection('predictions') as pred:
                self.display_prediction(pred, image.resize(self.diffeo.d.shape[:2]))    
        
        if False:
            with report.subsection('composition') as sub:
                with sub.subsection('d12') as ssub:
                    d12 = Diffeomorphism2D.compose(self.diffeo, self.diffeo_inv)
                    d12.display(ssub)
                with sub.subsection('d21') as ssub:
                    d21 = Diffeomorphism2D.compose(self.diffeo_inv, self.diffeo)
                    d21.display(ssub)
                
        
    def display_prediction(self, report, image):
        num_pred = 6
        
        f = report.figure(cols=num_pred + 1)
        
        y_pred = image
        
        f.data_rgb('start_rgb', y_pred.get_rgba(), caption='Start Image')
        
        for i in xrange(1, num_pred):
            y_pred = self.predict(y_pred, 'self.diffeo.apply')
            f.data_rgb('pred%s_rgb' % i, y_pred.get_rgba(), caption='Prediction %s' % i)
    
    @staticmethod
    def compose(a1, a2):
        label = '%s%s' % (a1.label, a2.label)
        # This is the correct order
        diffeo = Diffeomorphism2D.compose(a2.diffeo, a1.diffeo)
        diffeo_inv = Diffeomorphism2D.compose(a1.diffeo_inv, a2.diffeo_inv)
        # This was the wrong order
        # diffeo = Diffeomorphism2D.compose(a1.diffeo, a2.diffeo)
        # diffeo_inv = Diffeomorphism2D.compose(a2.diffeo_inv, a1.diffeo_inv)
        original_cmds = a1.get_original_cmds() + a2.get_original_cmds()
        return DiffeoAction(label, diffeo, diffeo_inv, original_cmds)
        
 
