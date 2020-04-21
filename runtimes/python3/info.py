def run_command(file_name):
    return ['/usr/bin/python3', file_name]

def name_binary(submission_contents):
    return 'submission.py'

def name_code(submission_contents):
    return 'submission.py'

def compile_command(file_name):
    return ['/usr/bin/python3', '-m', 'py_compile', file_name]

def error_analyzer(error):
    pass

def compile_error_message(stdout, stderr):
    return stdout + "\n" + stderr

language = "python3"
