import requests
from flask import Flask, request
import os

import info
import isolate

app = Flask(__name__)

@app.route('/')
def status():
    executor_status = {
        "language": info.language,
        "status": config['status'],
    }
    return executor_status

@app.route('/compile', methods=["POST"])
def compile():
    submission_file = request.files["submission"]    
    try:
        config["submission_content"] = submission_file.read().decode('utf-8')
    except UnicodeDecodeError:
        submission_file.close()
        return {"status": "CE", "message": "Error while decoding submission"}
    submission_file.close()
    os.makedirs("submission", exist_ok=True)
    config["submission_code_path"] = os.path.join("submission", info.name_code(config['submission_content']))
    with open(config["submission_code_path"], "w") as submission_code_file:
        submission_code_file.write(config["submission_content"])
    try:
        compile_process = isolate.execute_command_subprocess(info.compile_command(config["submission_code_path"]), time_limit=10, check=False)
        compile_process.check_returncode()
        config['status'] = 'loaded'
        config['submission_binary_path'] = os.path.join("submission", info.name_binary(config['submission_content']))
        return {"status": "CC"}
    except isolate.subprocess.TimeoutExpired:
        return {"status": "CE", "message": "Compilation Timed Out"}
    except:
        return {"status": "CE", "message": info.compile_error_message(compile_process.stdout, compile_process.stderr)}

@app.route('/run', methods=["POST"])
def run():
    if config['status'] != 'loaded':
        return {"status": "EE", "message": "Submission not loaded"}
    
    if "stdin" in request.form:
        stdin = request.form["stdin"]
    else:
        stdin = ""

    if "env" in request.form:
        env = json.loads(request.form["env"])
    else:
        env = dict()

    if "time_limit" in request.form:
        time_limit = float(request.form["time_limit"])
    else:
        time_limit = 1

    if "memory_limit" in request.form:
        memory_limit = float(request.form["memory_limit"])
    else:
        memory_limit = 64

    status = isolate.run(config["submission_binary_path"], stdin, time_limit, memory_limit, env)

    return status

@app.before_first_request
def setup():
    global config
    config = dict()
    if "EXECUTOR_CALLBCK" in os.environ:
        config["callback"] = os.environ['EXECUTOR_CALLBACK']
        requests.get(config["callback"])
    config["status"] = "ready"

