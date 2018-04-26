import subprocess
print("\n\n<<<<<<<<<< TEST 2.0 | testing correctness of output >>>>>>>>>>")
subprocess.call("python3 test.py", shell=True)

print("\n\n<<<<<<<<<< TEST 5.0 | testing missing parameters >>>>>>>>>>")
print("================= currently testing qt3.14 =================")
subprocess.call("python neg_test.py qt3.14 1", shell=True)
print("================= currently testing moose ==================")
subprocess.call("python neg_test.py moose 1", shell=True)
subprocess.call("python test.py", shell=True)

