import time
import subprocess
from kopf.testing import KopfRunner

def test_operator():
    with KopfRunner(['run', '-A', '--verbose', 'service/handlers.py']) as runner:
        # do something while the operator is running.

        subprocess.run("kubectl apply -f exemples/op-cmi-cr.yml", shell=True, check=True)
        time.sleep(1)  # give it some time to react and to sleep and to retry
    
    # print("stderr: ", runner.stderr)
    print("exc_info: ", runner.exc_info)
    print("output: ", runner.output)
    assert runner.exit_code == 0
    assert runner.exception is None

def clean_up():
    with KopfRunner(['run', '-A', '--verbose', 'service/handlers.py']) as runner:
        subprocess.run("kubectl delete -f exemples/op-cmi-cr.yml", shell=True, check=True)


    
    

if __name__ == "__main__":
    test_operator()
    clean_up()