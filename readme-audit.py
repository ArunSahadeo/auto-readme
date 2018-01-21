from subprocess import check_output
from pathlib import Path
import os, sys

def getBashShell(list):
    for el in list:
        if "bash" in el: return el

available_shells = check_output('cat /etc/shells', shell=True).decode('UTF-8').splitlines()

bash_shell = getBashShell(available_shells)

the_readme = check_output('find . -maxdepth 1 -iname "readme.md" | sed "s|./||"', shell=True, executable=bash_shell)

the_readme = the_readme.decode('UTF-8').strip()

readme_path = os.path.join(os.getcwd(), the_readme).strip()

if not os.path.isfile(readme_path):
    print("README does not exist")
    sys.exit(1)

commit_count = int(check_output('git log --oneline {:s} | wc -l'.format(the_readme), shell=True, executable=bash_shell).decode('UTF-8'))

if commit_count > 1:
    print("Your README is up to date.")
    sys.exit(1)

output = check_output('compgen -ac', shell=True, executable=bash_shell)
commands = output.splitlines()

for line_number, line in enumerate(commands):
    commands[line_number] = line.decode('UTF-8')

readme_contents = open(the_readme, 'r')
readme_suffices = False

for line in readme_contents:
    if line.rstrip("\n") in commands:
        readme_suffices = True

if readme_suffices:
    print("Your README suffices.")
    sys.exit(1)

print("You need to update your README.")

with open(the_readme) as file:
    character_count = len(file.read())
    while int(check_output('stat -c "%s" {:s}'.format(the_readme), shell=True, executable=bash_shell).decode('UTF-8')) == character_count:
        os.system('{:s} {:s}'.format(os.getenv('EDITOR'), the_readme))
