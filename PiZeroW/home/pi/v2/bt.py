import bluetooth
import subprocess
status = subprocess.call("echo -e \"yes\" | bt-agent --capability=NoInputNoOutput -p pin.cfg &",shell=True)