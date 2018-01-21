import os

def which_infrastructure():
    
    if os.path.isdir(os.path.join(os.getcwd(), 'wp-includes').strip()) or os.path.isdir(os.path.join(os.getcwd(), 'wp-admin').strip()):
        wordpress_install()
    elif os.path.isfile(os.path.join(os.getcwd(), 'artisan')):
        laravel_install()
    else:
        standard_install()

def standard_install():
    with open(the_readme) as file:
        character_count = len(file.read())
        while int(check_output('stat -c "%s" {:s}'.format(the_readme), shell=True, executable=bash_shell).decode('UTF-8')) == character_count:
            os.system('{:s} {:s}'.format(os.getenv('EDITOR'), the_readme))
