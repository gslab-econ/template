import yaml
import os
import subprocess

def print_provenance():
    PATHS = yaml.load(open('constants.yaml', 'rU'))
    header = 'Note: `Provenance.txt` is produced by `print_provenance.py`. Do not directly edit this file.\n\n'
    inputs = load_inputs()
    check_missing_inputs(PATHS, inputs)
    with open('%s/provenance.txt' % PATHS['input'], 'wb') as provenance:
        provenance.write(header)
        for f in inputs.keys():
            if not os.path.isfile('%s/%s' % (PATHS['input'], f)):
                raise IOError('%s does not exist.' % f)
            args   = ['git', '--no-pager', 'log', '-1', '--date=format:%Y-%m-%d %H:%M:%S',
                    '--format=%h at %cd', 'input/%s' % f]
            commit = subprocess.check_output(args).strip()
            if commit:
                provenance.write('`%s` is copied from `%s` and modified by commit %s.\n' % (f, inputs[f], commit))
            else:
                provenance.write('`%s` is copied from `%s` and has no commit history.\n' % (f, inputs[f]))

def load_inputs():
    PATHS = yaml.load(open('../analysis/constants.yaml', 'rU'))
    inputs = {'plot.eps' : '../analysis/%s/' % PATHS['build']['analysis'],
              'table.txt': '../analysis/%s/' % PATHS['build']['analysis']}
    return inputs

def check_missing_inputs(PATHS, inputs):
    for f in os.listdir('%s' % PATHS['input']):
        if f not in ['.DS_Store', 'provenance.txt'] + inputs.keys():
            raise IOError('The provenance of %s is not specified.' % f)