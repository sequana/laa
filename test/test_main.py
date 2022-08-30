import os
import subprocess
import sys

import sequana_pipelines.laa.main as m

from . import test_dir


ref_file = f"{test_dir}/data/AB038249.fa"
def test_standalone_subprocess(tmpdir):
    input_dir = os.sep.join((test_dir, 'data'))
    cmd = ["test", "--input-directory", input_dir, "--working-directory", str(tmpdir), "--force", "--reference-file", ref_file]
    subprocess.call(cmd)


def test_standalone_script(tmpdir):
    input_dir = os.sep.join((test_dir, 'data'))
    sys.argv = ["test", "--input-directory", input_dir, "--working-directory", str(tmpdir), "--force",
"--reference-file", ref_file]
    m.main()


def test_version():
    cmd = ["sequana_laa"," --version"]
    subprocess.call(cmd)

