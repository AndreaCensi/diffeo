import os

from diffeo2dds import logger, get_diffeo2dds_config, UncertainImage
from reprep import Report

from .d2dds import Diffeo2dds


__all__ = ['Diffeo2ddsShow']


class Diffeo2ddsShow(Diffeo2dds.get_sub()):
    """ Creates a report for a DDS. """
    
    cmd = 'show'
    usage = 'show-discdds  [-i <image>] [<discdds1> <discdds2> ...]'
    
    def define_program_options(self, params):
        params.accept_extra()
        params.add_string('output', short='o', help="Output directory",
                          default='out/d2dds_makedds')
        
        params.add_string('image', short='i', help="ID image.", default='lena')
        
    def go(self):
        outdir = self.options.output
        which = self.options.get_extra()
            
        diffeo2dds_config = get_diffeo2dds_config()
        
        if not which:
            todo = diffeo2dds_config.discdds.keys()  
        else:
            todo = diffeo2dds_config.discdds.expand_names(which)
    
        id_image = self.options.image
        image = UncertainImage(diffeo2dds_config.images.instance(id_image))
        
        for id_dds in todo:
            self.info('Writing %s' % id_dds)
            dds = diffeo2dds_config.discdds.instance(id_dds) 
            report = Report(id_dds)
            
            dds.display(report, image=image)
        
            write_report_files(report, basename=os.path.join(outdir, id_dds))    

         


def write_report_files(report, basename):
    # TODO: hdf output
    filename = basename + '.html'
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        
    logger.info('Writing to %r.' % filename)
    report.to_html(filename, write_pickle=True)
