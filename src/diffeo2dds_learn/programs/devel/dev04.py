from .dev import Dev
from compmake import compmake_execution_stats
from diffeo2dds_learn.programs import DDSLLearn
from quickapp import QuickApp, iterate_context_names_quartet
from reprep import Report
from reprep.report_utils import StoreResults, StoreResultsDict
from reprep_tables.make_tables import jobs_tables_by_sample
import numpy as np

__all__ = ['Dev04']


class Dev04(Dev.get_sub(), QuickApp):  # @UndefinedVariable
    """ Formal benchmarks for some of the estimators. """
     
    cmd = 'dev04'
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        sizes = np.linspace(16, 256, 32).astype('int')
        # sizes = [16, 32, 64, 128, 256, 512]
        nobs = 500
        streams = ['test_gauss_drx1']
        estimators = ['test_ddsest_unc_refine0',
                      'test_ddsest_unc_refine0ns',  # don't stop
                      'test_ddsest_unc_fast_order']
        max_displs = [0.1, 0.15, 0.2, 0.25, 0.3]
        
        def should_do(estimator, shape):
            if estimator in ['test_ddsest_unc_refine0', 'test_ddsest_unc_refine0ns']:
                return True
            if estimator == 'test_ddsest_unc_fast_order':
                return shape <= 128 
            assert False, estimator
        
        results = StoreResults()
        comp_stats = StoreResults()
        
        combs = iterate_context_names_quartet(context, sizes, max_displs, streams, estimators)
        for c, shape, max_displ, stream, estimator in combs:
            if not should_do(estimator, shape):
                continue
            
            id_stream = stream + '_%s_%s' % (shape, nobs)
            key = dict(length=nobs, shape=shape, stream=stream, estimator=estimator,
                       id_stream=id_stream, max_displ=max_displ)
            learned = c.subtask(DDSLLearn, stream=id_stream, estimator=estimator,
                                max_displ=max_displ) 
            results[key] = learned
            comp_stats[key] = compmake_execution_stats(learned)

        source_descs = {}
        # For each sample, show the cpu for each algorithm
        jobs_tables_by_sample(context, id_table='cpu',
                    allstats=comp_stats,
                    one_table_for_each='id_stream',
                    cols_fields=[
                        'cpu_time',
                        'wall_time',
                    ],
                    rows_field='estimator',
                    source_descs=source_descs)

        estimators_subsets = get_estimators_subsets(estimators)
        # one plot for each group
        for id_group, estimators in estimators_subsets.items():
            c = context.child(id_group)
            group_runs = comp_stats.select(lambda k: k['estimator'] in estimators)
            report = c.comp(report_cputime, group_runs)
            c.add_report(report, 'cputime', group=id_group)
        
        
def get_estimators_subsets(estimators):
    groups = {}
    groups['all'] = estimators
    for e in estimators:
        groups[e] = [e]
    return groups


def report_cputime(allstats):
    allstats = StoreResultsDict(allstats)
    r = Report('cputime') 
    # each line is one estimator
    f = r.figure() 
    
    with f.plot('cputime_vs_shape') as pylab:
        plot_cputtime_vs_shape(pylab, allstats)
    
    with f.plot('cputime_vs_shape_displ') as pylab:
        plot_cputtime_vs_shape_by_estimator_displ(pylab, allstats)
        
    with f.plot('cputime_vs_displ') as pylab:
        plot_cputtime_vs_displ(pylab, allstats)
    
    return r


def plot_cputtime_vs_shape(pylab, allstats):
    for id_estimator, runs in allstats.groups_by_field_value('estimator'):
        xs, ys = [], []
        for shape, samples in runs.groups_by_field_value('shape'):
            cpu = list(samples.field_or_value_field('cpu_time'))
            xs.extend([shape] * len(cpu))
            ys.extend(cpu)
        pylab.semilogy(xs, ys, label=id_estimator)
    pylab.xlabel('shape (pixels)')
    pylab.ylabel('cpu (s)')
    pylab.legend() 


def plot_cputtime_vs_displ(pylab, allstats):
    for id_estimator, runs in allstats.groups_by_field_value('estimator'):
        xs, ys = [], []
        for max_displ, samples in runs.groups_by_field_value('max_displ'):
            cpu = list(samples.field_or_value_field('cpu_time'))
            xs.extend([max_displ] * len(cpu))
            ys.extend(cpu)
        pylab.semilogy(xs, ys, label=id_estimator)
    pylab.xlabel('max displacement (fraction)')
    pylab.ylabel('cpu (s)')
    pylab.legend() 
    

def plot_cputtime_vs_shape_by_estimator_displ(pylab, allstats):
    # style_estimator = [dict(), dict()]
    linestyles = ['--', ':']
    style_estimator = [dict(linestyle=l) for l in linestyles]
    
    style_displ = [dict(color='r'), dict(color='g'), dict(color='b')]
    
    for index_estimator, (id_estimator, runs) in enumerate(allstats.groups_by_field_value('estimator')):
        for index_displ, (max_displ, runs2) in enumerate(runs.groups_by_field_value('max_displ')):
            
            xs, cpus, lengths = [], [], []
            for shape, samples in runs2.groups_by_field_value('shape'):
                length = list(samples.field_or_value_field('length'))
                cpu = list(samples.field_or_value_field('cpu_time'))
                xs.extend([shape] * len(cpu))
                cpus.extend(cpu)
                lengths.extend(length)
            xs = np.array(xs)
            cpus = np.array(cpus)
            cpu_per_iteration = cpus / length

            label = '%s; displ=%.2f' % (id_estimator, max_displ)
            
            style = {}
            style.update(style_estimator[index_estimator % len(style_estimator)])
            style.update(style_displ[index_displ % len(style_displ)])
            pylab.semilogy(xs, cpu_per_iteration, label=label, **style)
            
    pylab.xlabel('shape (pixels)')
    pylab.ylabel('mean cpu per iteration (s)')
    # pylab.legend() 

    
