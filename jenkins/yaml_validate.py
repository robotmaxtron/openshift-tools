#!/usr/bin/env python
'''
python yaml validator for a git commit
'''
import shutil
import sys
import os
import glob
import tempfile
import subprocess
import yaml

def get_changes(oldrev, newrev, tempdir):
    '''Get a list of git changes from oldrev to newrev'''
    proc = subprocess.Popen(['/usr/bin/git', 'diff', '--name-only', oldrev,
                             newrev, '--diff-filter=ACM'], stdout=subprocess.PIPE)
    proc.wait()
    files = proc.stdout.read().strip().split('\n')

    # No file changes
    if not files:
        return []

    cmd = '/usr/bin/git archive %s %s | /bin/tar x -C %s' % (newrev, " ".join(files), tempdir)
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

    return [fmod for fmod in glob.glob('%s/**/*' % tempdir) if not os.path.isdir(fmod)]

def main():
    '''
    Perform yaml validation
    '''
    results = []
    try:
        tmpdir = tempfile.mkdtemp(prefix='jenkins-git-')
        old, new, _ = sys.argv[1:]

        for file_mod in get_changes(old, new, tmpdir):

            print "+++++++ Received: %s" % file_mod

            if not file_mod.endswith('.yml') or not file_mod.endswith('.yaml'):
                continue

            try:
                yaml.load(file_mod)
                results.append(True)

            except yaml.scanner.ScannerError as yerr:
                print yerr.message
                results.append(False)
    finally:
        shutil.rmtree(tmpdir)

    if not all(results):
        sys.exit(1)

if __name__ == "__main__":
    main()
