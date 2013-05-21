from compmake.utils import safe_pickle_dump, safe_pickle_load
from conf_tools.load_entries import write_entries
import os

__all__ = ['load_pickle', 'ds_dump']
           
def ds_dump(dds, path, name, desc):
    '''
        Save the summarized diffeomorphisms system to a pickle file
    
        :param path: output directory
        :param name: name of this system
    '''
    
    if not os.path.exists(path):
        os.makedirs(path)

    basename = os.path.join(path, '%s.discdds' % name)
    pickle_file = basename + '.pickle'
    filename_yaml = basename + '.yaml'

    safe_pickle_dump(dds, pickle_file)
            
    spec = {
       'id': name,
       'desc': desc,
       'code': ['diffeo2dds.load_pickle',
                {'file:pickle': name + '.discdds.pickle'}]
    }
    write_entries([spec], filename_yaml)


def load_pickle(pickle):
    return safe_pickle_load(pickle)
    
