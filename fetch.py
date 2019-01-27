import sys
import platform
import cpuinfo
import os
import distro
import socket
import getpass
import re

from time import localtime, strftime
from subprocess import check_output

resolution_regex = r"\d+x\d+"
ram_regex = r"\d+"

host_array = []
host_array.append(getpass.getuser())
host_array.append(socket.gethostname())
host = "@".join(host_array)

distro_array = []
distro_array.append(distro.name(pretty=False))
distro_array.append(distro.version(pretty=False))
distro_info = " ".join(distro_array)

operating_system = platform.system()
kernel = platform.platform(terse=True)
current_datetime = strftime("%A, %B %d %Y, %H:%M:%S", localtime())
cpu = " ".join(cpuinfo.get_cpu_info()["brand"].split())
ram_output = check_output(["awk \"/MemTotal/ {print $2}\" /proc/meminfo"], shell = True)
ram_regexed = re.compile(ram_regex).search(ram_output.decode("utf-8"))
ram_in_mb = round(int(ram_regexed.group())/1024)
resolution_output = check_output(["xrandr | grep \"*\""], shell=True)
screen_resolution = re.compile(resolution_regex).search(resolution_output.decode("utf-8"))

if sys.platform == "linux" or platform == "linux2":
    DISPLAY = """
       a88888.       {host} 
      d888888b.      
      8P"YP"Y88      OS: {distro_info}
      8|o||o|88      Kernel: {kernel}
      8'    .88      CPU: {cpu} 
      8`._.' Y8.     Memory: {ram_in_mb} MB
     d/      `8b.    Resolution: {screen_resolution}
   .dP   .     Y8b.  Time: {current_datetime}
  d8:'   "   `::88b. 
 d8"           `Y88b
:8P     '       :888
 8a.    :      _a88P
 ._/"Yaa_ :    .| 88P|
 \    YP"      `| 8P  `.
 /     \._____.d|    .'
 `--..__)888888P`._.'
    """
else:
    print("fetch.py currently only supports GNU/Linux.")
    exit()

print(DISPLAY.format(
    host = host,
    os = operating_system,
    distro_info = distro_info,
    kernel = kernel,
    cpu = cpu,
    ram_in_mb = ram_in_mb,
    screen_resolution = screen_resolution.group(),
    current_datetime = current_datetime
))
