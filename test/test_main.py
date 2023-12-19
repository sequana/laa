import os
import subprocess
import sys

from sequana_pipelines.laa.main import main

from click.testing import CliRunner

from . import test_dir


ref_file = f"{test_dir}/data/AB038249.fa"
def test_standalone_subprocess(tmpdir):
    input_dir = os.sep.join((test_dir, 'data'))
    cmd = ["test", "--input-directory", input_dir, "--working-directory", str(tmpdir), "--force", "--reference-file", ref_file]
    subprocess.call(cmd)


def test_standalone_script(tmpdir):
    input_dir = os.sep.join((test_dir, 'data'))
    args = ["--input-directory", input_dir, "--working-directory", str(tmpdir), "--force", "--reference-file", ref_file]
    runner = CliRunner()
    results = runner.invoke(main, args)

    assert results.exit_code == 0


def test_version():
    cmd = ["sequana_laa"," --version"]
    subprocess.call(cmd)

