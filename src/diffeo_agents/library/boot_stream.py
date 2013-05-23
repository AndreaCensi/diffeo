from bootstrapping_olympics.library.nuisances import scipy_image_resample
from bootstrapping_olympics.programs.manager import DataCentral
from diffeo2dds_learn import LogItem, Stream
import itertools

class BootStream(Stream):
    """ Yields the data from boot_olympics logs as a diffeo Stream. """
     
    def __init__(self, boot_root, id_robot, shape):
        self.boot_root = boot_root
        self.id_robot = id_robot
        self.shape = shape
        
    def read_all(self):
        print('boot_root: %s' % self.boot_root)
        data_central = DataCentral(self.boot_root)
        log_index = data_central.get_log_index()
        observations = log_index.read_all_robot_streams(id_robot=self.id_robot)
        pairs = pairwise(observations)
        i = 0
        for bd1, bd2 in pairs:
            i += 1
            if i % 100 == 1:
                print('read %d' % i)
            y0 = bd1['observations']
            y1 = bd2['observations']
            u = bd1['commands']
            if self.shape is not None:
                y0 = scipy_image_resample(y0, self.shape)
                y1 = scipy_image_resample(y1, self.shape)
            log_item = LogItem(y0=y0, y1=y1, u=u, x0=None)
            yield log_item
        

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)
