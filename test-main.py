import os
import subprocess
import script_fetcher

# print('-----CWD ---')
# print(os.getcwd())
# print('===DIRS===')
# ls_result = subprocess.call('ls -lrt', shell=True)
# print(ls_result)

script_fetcher.get_script('script.txt')
