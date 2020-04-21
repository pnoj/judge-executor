import subprocess
import shutil
import os
import sys

import info

def execute_command_subprocess(command, time_limit=None, check=True, verbose=False):
    if verbose:
        print(' '.join(command))
    return subprocess.run(command, capture_output=True, timeout=time_limit, text=True, check=check)

def setup():
    execute_command_subprocess(['isolate', '--cg', '--init'])

def cleanup():
    execute_command_subprocess(['isolate', '--cleanup'])

def execute_command(command, real_directory, virtual_directory, stdin, stdout, stderr, meta, time_limit=1, memory_limit=64, env=dict(), verbose=False):
    process_result = execute_command_subprocess(['isolate'] + ['--env={0}={1}'.format(i, env[i]) for i in env] + ['--dir={0}={1}:rw'.format(virtual_directory, os.path.join(real_directory, "isolate")), '--cg', '--wall-time='+str(time_limit), '--cg-mem='+str(int(memory_limit*1024)), '--stdin='+stdin, '--stdout='+stdout, '--stderr='+stderr, '--meta='+os.path.join(real_directory, "meta"), '--run', '--'] + command, check=False, verbose=verbose)
    if verbose:
        print(process_result.stdout)
        print(process_result.stderr)

def run(program_path, stdin, time_limit, memory_limit, env=dict(), isolate_dir=None):
    cleanup()

    setup()

    if isolate_dir == None:
        if "ISOLATE_DIRECTORY" in os.environ:
            isolate_dir = os.environ['ISOLATE_DIRECTORY']
        else:
            isolate_dir = '/isolate'

    os.makedirs(isolate_dir, exist_ok=True)
    os.chmod(isolate_dir, 0o777)
    os.makedirs(os.path.join(isolate_dir, "isolate"), exist_ok=True)
    os.chmod(os.path.join(isolate_dir, "isolate"), 0o777)

    shutil.copyfile(program_path, os.path.join(isolate_dir, "isolate", os.path.basename(program_path)))

    if os.path.exists(stdin):
        shutil.copyfile(stdin, os.path.join(isolate_dir, "isolate", "in"))
    else:
        with open(os.path.join(isolate_dir, "isolate", "in"), "w") as stdin_file:
            stdin_file.write(stdin)

    execute_command(info.run_command(os.path.join("/app", os.path.basename(program_path))), isolate_dir, "/app", "/app/in", "/app/out", "/app/err", "/app/meta", time_limit, memory_limit, env)

    with open(os.path.join(isolate_dir, "isolate", "out"), "r") as stdout_file:
        stdout = stdout_file.read()
    
    with open(os.path.join(isolate_dir, "isolate", "err"), "r") as stderr_file:
        stderr = stderr_file.read()

    with open(os.path.join(isolate_dir, "meta"), "r") as meta_file:
        meta = meta_file.read()

    meta_dict = dict()

    for line in meta.strip("\n").split("\n"):
        line_tup = line.split(":")
        meta_dict[line_tup[0]] = line_tup[1]

    result = dict()
    if "status" in meta_dict:
        if float(meta_dict['cg-mem']) > memory_limit*1024:
            result['status'] = 'MLE'
            result['output'] = None 
        elif meta_dict['status'] == "RE":
            result['status'] = 'IR'
            result['message'] = meta_dict['message']
            result['output'] = stderr
        elif meta_dict['status'] == "SG":
            result['status'] = 'RTE'
            result['message'] = meta_dict['message']
            result['output'] = stderr
        elif meta_dict['status'] == "TO":
            result['status'] = 'TLE'
            result['output'] = None 
        else:
            result['status'] = 'IE'
            result['output'] = None 
    else:
        if sys.getsizeof(stdout) > 67108864:
            result['status'] = 'OLE'
            result['output'] = None 
        else:
            result['status'] = 'EC'
            result['output'] = stdout

    result['resource'] = {'time': float(meta_dict['time-wall']), 'memory': float(meta_dict['cg-mem'])/1024}

    cleanup()

    shutil.rmtree(isolate_dir)

    return result
