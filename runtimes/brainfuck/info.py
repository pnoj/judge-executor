import shutil
import subprocess
import os

def get_box_id():
    return int(os.environ['ISOLATE_BOX_ID'])

def execute_command_subprocess(command, time_limit=None, check=True, verbose=False):
    if verbose:
        print(' '.join(command))
    return subprocess.run(command, capture_output=True, timeout=time_limit, text=True, check=check)

def run_command(file_name):
    return [file_name]

def name_binary(submission_contents):
    return 'submission.bf'

def name_code(submission_contents):
    return 'submission.bf'

def compile_command(file_name, memory_limit=1):
    return ["bash", "bfcc/compile.sh", str(int(memory_limit*(1024**2))), file_name]

def error_analyzer(error):
    pass

def compile_error_message(stdout, stderr):
    return stdout + "\n" + stderr

def find_executable():
    return shutil.which("python3")

def override_isolate_command(command, real_directory, virtual_directory, stdin, stdout, stderr, meta, time_limit=1, memory_limit=64, env=dict()):
    execute_command_subprocess(compile_command("/isolate/isolate/submission.bf", memory_limit), time_limit=12, check=True)
    os.chmod("/isolate/isolate/submission", 0o777)
    return ['isolate'] + ['--env={0}={1}'.format(i, env[i]) for i in env] + ['--dir={0}={1}:rw'.format(virtual_directory, os.path.join(real_directory, "isolate")), '--cg', '--wall-time='+str(time_limit), '--stdin='+stdin, '--stdout='+stdout, '--stderr='+stderr, '--meta='+os.path.join(real_directory, "meta"), f'--box-id', f'{get_box_id()}', '--run', '--', "/app/submission"]

language = "brainfuck"
