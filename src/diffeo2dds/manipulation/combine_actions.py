from . import contract
from ..configuration import get_diffeo2dds_config
from ..model import DiffeoSystem


__all__ = ['DDSCompositeActions']


@contract(actions='list(dict)')
def DDSCompositeActions(id_dds, label, actions):
    """ 
        Creates a new DDS by combining actions from another.
    
        ``actions`` is a list of dictionaries. Each dict must have
        the fields "plan" and "label".
    """
    
    dds = get_diffeo2dds_config().discdds.instance(id_dds)
    
    def make_composite_action(plan):
        plan = dds.plan_from_labels(plan)
        composite = dds.plan2action(plan)
        # composite.label = label
        return composite
        
    new_actions = [make_composite_action(**a) for a in actions]
    return DiffeoSystem(label, new_actions)
    
