import subprocess
subprocess.call("python neg_test.py qt3.14 1", shell=True)
subprocess.call("python neg_test.py moose 1", shell=True)
subprocess.call("python test.py", shell=True)

