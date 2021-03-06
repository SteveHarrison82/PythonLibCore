#!/usr/bin/env python

from __future__ import print_function
from os.path import abspath, dirname, join
import sys

from robot import run, rebot
from robotstatuschecker import process_output


curdir = dirname(abspath(__file__))
outdir = join(curdir, 'results')
tests = join(curdir, 'tests.robot')
sys.path.insert(0, join(curdir, '..', 'src'))
for variant in ['Hybrid', 'Dynamic']:
    output = join(outdir, variant + '.xml')
    rc = run(tests, name=variant, variable='LIBRARY:%sLibrary' % variant,
             output=output, report=None, log=None)
    if rc > 250:
        sys.exit(rc)
    process_output(output, verbose=False)
print('\nCombining results.')
rc = rebot(join(outdir, 'Hybrid.xml'), join(outdir, 'Dynamic.xml'),
           name='Acceptance Tests', outputdir=outdir)
if rc == 0:
    print('\nAll tests passed/failed as expected.')
else:
    print('\n%d test%s failed.' % (rc, 's' if rc != 1 else ''))
sys.exit(rc)
