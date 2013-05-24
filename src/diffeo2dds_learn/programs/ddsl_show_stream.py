from .ddsl import DDSL
from diffeo2dds_learn import get_diffeo2ddslearn_config
from quickapp import QuickApp, QuickMultiCmdApp
from reprep import Report
import itertools
from quickapp.app_utils.subcontexts import iterate_context_names

__all__ = ['DDSLShowStream', 'make_stream_report', 'DDSLShow']

class DDSLShow(DDSL.get_sub(), QuickMultiCmdApp):
    cmd = 'show'

    def define_multicmd_options(self, params):
        pass
    
    def initial_setup(self):
        pass

class DDSLShowStream(DDSLShow.get_sub(), QuickApp): 
    """ Creates a report for the streams. """
    
    cmd = 'streams'
    usage = 'show-stream [<stream1> <stream2> ...]'
    
    def define_options(self, params):
        params.add_string('streams', help="Streams names, separated by ','.")
        params.add_int('nsamples', help="Number of samples to show image.")
        
    def define_jobs_context(self, context):
            
        config = get_diffeo2ddslearn_config()

        nsamples = self.options.nsamples
        which = self.options.streams    
        todo = config.streams.expand_names(which)
    
        self.info('given streams: %s' % which)
        self.info('using streams: %s' % todo)
         
        for c, id_stream in iterate_context_names(context, todo):
            report = c.comp_config(make_stream_report,
                                  id_stream, nsamples=nsamples)
            
            c.add_report(report, 'stream_report',
                                 id_stream=id_stream, nsamples=nsamples)
     
        
def make_stream_report(id_stream, nsamples):
    config = get_diffeo2ddslearn_config()
    stream = config.streams.instance(id_stream)
    r = Report(id_stream)
    data = itertools.islice(stream.read_all(), nsamples)
    
    for i, log_item in enumerate(data):
        with r.subsection('log_item%d' % i) as sub:
            log_item.display(sub)
         
    return r
