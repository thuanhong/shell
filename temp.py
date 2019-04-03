

import subprocess
result = subprocess.Popen(["ls", "-l"])
print(result.communicate()[0])