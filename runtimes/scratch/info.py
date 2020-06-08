import shutil

def run_command(file_name):
    return [find_executable(), file_name]

def name_binary(submission_contents):
    return 'submission.scrape'

def name_code(submission_contents):
    return 'submission.json'

def compile_command(file_name):
    return ['scrapec', '--json', file_name, "-o", "/app/submission/submission.scrape"]

def error_analyzer(error):
    pass

def compile_error_message(stdout, stderr):
    return stdout + "\n" + stderr

def find_executable():
    return shutil.which("scrape")

language = "scratch"
