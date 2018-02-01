import os, re, sys
import yaml, yaml.scanner
from subprocess import check_output

def get_config():
    acceptedConfigs = [
        'config.yaml',
        'config.yml'
    ]

    config = None

    for acceptedConfig in acceptedConfigs:
        if os.path.isfile(os.path.join(os.getcwd(), acceptedConfig)):
            config = acceptedConfig
            break
        else:
            continue

    return config


def which_infrastructure(the_readme, bash_shell):
    
    if os.path.isdir(os.path.join(os.getcwd(), 'wp-includes').strip()) or os.path.isdir(os.path.join(os.getcwd(), 'wp-admin').strip()):
        wordpress_install(the_readme, bash_shell)
    elif os.path.isfile(os.path.join(os.getcwd(), 'artisan')):
        laravel_install(the_readme, bash_shell)
    else:
        standard_install(the_readme, bash_shell)

def wordpress_install(the_readme, bash_shell):
    connection_params = dict([
        ('host', ''),
        ('database', ''),
        ('user', ''),
        ('pass', ''),
        ('prefix', ''),
        ('driver', '')
    ])

    accepted_database_drivers = [
        'mysql',
    ]

    define_pattern = re.compile(r"""\bdefine\(\s*('|")(.*)\1\s*,\s*('|")(.*)\3\)\s*;""")
    assign_pattern = re.compile(r"""(^|;)\s*\$([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)\s*=\s*('|")(.*)\3\s*;""")

    config_vars = {}

    for line in open("wp-config.php"):
        for match in define_pattern.finditer(line):
            config_vars[match.group(2)]=match.group(4)
        for match in assign_pattern.finditer(line):
            config_vars[match.group(2)]=match.group(4)

    for key, value in config_vars.items():
        if key.lower() == str('db_host').lower():
            connection_params['host'] = value
        elif key.lower() == str('db_name').lower():
            connection_params['database'] = value
        elif key.lower() == str('db_user').lower():
            connection_params['user'] = value
        elif key.lower() == str('db_password').lower():
            connection_params['pass'] = value
        elif key.lower() == str('table_prefix').lower():
            connection_params['prefix'] = value
        else:
            continue

    try:
        YAML_config = yaml.safe_load(get_config()) or {}
        config_options = open(YAML_config, 'r')
        config_options = yaml.load(config_options)

        for option in config_options:
            if option.lower() == str('database_driver').lower():
                connection_params['driver'] = config_options[option]

    except yaml.scanner.ScannerError as e:
        raise Exception(e)
    except Exception as e:
        print(type(e))

def laravel_install(the_readme, bash_shell):
    print("Laravel!!!")

def standard_install(the_readme, bash_shell):
    with open(the_readme) as file:
        character_count = len(file.read())
        while int(check_output('stat -c "%s" {:s}'.format(the_readme), shell=True, executable=bash_shell).decode('UTF-8')) == character_count:
            os.system('{:s} {:s}'.format(os.getenv('EDITOR'), the_readme))
