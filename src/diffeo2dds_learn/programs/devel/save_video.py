from diffeo2dds_learn import get_conftools_streams

__all__ = ['video_visualize_diffeo_stream1', 'video_visualize_diffeo_stream1_robot']

def video_visualize_diffeo_stream1(id_stream, out):
    """ Creates a video for a stream. """
    import procgraph_diffeo  # @UnusedImport
    from procgraph import pg
    config = dict(out=out, stream=id_stream)
    pg('visualize_diffeo_stream1', config=config)
    return out

def video_visualize_diffeo_stream1_robot(id_robot, boot_root, out):
    """ Creates a video for the stream. """
     
    my_stream = 'robotstream-%s' % id_robot
     
    bootstream = ['diffeo_agents.library.BootStream',
                      dict(id_robot=id_robot,
                           boot_root=boot_root)]
    limit_stream = ['diffeo2dds_learn.library.LimitStream',
                      dict(n=1000, stream=bootstream)]
    
    streams = get_conftools_streams()
    streams.add_spec(my_stream, "", limit_stream)
                          
    return video_visualize_diffeo_stream1(my_stream, out)
