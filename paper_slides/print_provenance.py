import yaml
import os
import subprocess

def print_provenance():
    header = 'Note: `Provenance.txt` is produced by `print_provenance.py`. Do not directly edit this file.\n\n'
    inputs = load_inputs()
    with open('input/provenance.txt', 'wb') as provenance:
        provenance.write(header)
        for f in inputs.keys():
            if not os.path.isfile('input/%s' % f):
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
