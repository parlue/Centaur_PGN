import bluetooth
import subprocess
status = subprocess.call("echo -e \"yes\" | bt-agent --capability=NoInputNoOutput -p /etc/pin.cfg &",shell=True)