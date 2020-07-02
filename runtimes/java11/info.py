import shutil
import re
import os

public_class_regex = re.compile(r'public class ([^ \n-/\\{}"\'`~<>]*)')

def get_box_id():
    return int(os.environ['ISOLATE_BOX_ID'])

def get_public_class(submission_contents):
    public_class_match = re.search(public_class_regex, submission_contents)
    if public_class_match == None:
        raise Exception('No public class: your main class must be declared as a "public class"')
    else:
        return public_class_match.group(1)

def run_command(file_name):
    return [shutil.which("java"), "-cp", os.path.dirname(file_name), os.path.basename(file_name[:-6])]

def name_binary(submission_contents):
    public_class = get_public_class(submission_contents)
    return public_class + '.class'

def name_code(submission_contents):
    public_class = get_public_class(submission_contents)
    return public_class + '.java'

def compile_command(file_name):
    return [shutil.which("javac"), file_name]

def error_analyzer(error):
    pass

def compile_error_message(stdout, stderr):
    return stdout + "\n" + stderr

def override_isolate_command(command, real_directory, virtual_directory, stdin, stdout, stderr, meta, time_limit=1, memory_limit=64, env=dict()):
    return ['isolate'] + ['--env={0}={1}'.format(i, env[i]) for i in env] + ['--dir={0}={1}:rw'.format(virtual_directory, os.path.join(real_directory, "isolate")), '--cg', '--wall-time='+str(time_limit), '--stdin='+stdin, '--stdout='+stdout, '--stderr='+stderr, '--meta='+os.path.join(real_directory, "meta"), '--processes=25', f'--box-id', f'{get_box_id()}', '--run', '--'] + command + ['-Xmx'+str(int(memory_limit))+"m"]

language = "java11"
