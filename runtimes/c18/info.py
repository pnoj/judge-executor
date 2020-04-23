import shutil
import os

def run_command(file_name):
    os.chmod("/isolate/isolate/submission", 0o777)
    return [file_name]

def name_binary(submission_contents):
    return 'submission'

def name_code(submission_contents):
    return 'submission.c'

def compile_command(file_name):
    binary_path = os.path.dirname(file_name) + '/submission'
    return [find_executable(), '-o', binary_path, "-std=c18", file_name]

def error_analyzer(error):
    pass

def compile_error_message(stdout, stderr):
    return stdout + "\n" + stderr

def find_executable():
    return shutil.which("gcc")

language = "c18"
