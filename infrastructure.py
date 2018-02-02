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

def parse_DB(db_params):
    driver = db_params['driver']
    theme_name = None
    if driver.lower() == str('mysql').lower():
        import pymysql.cursors
        mysql_connection = pymysql.connect(
            host=db_params['host'],
            user=db_params['user'],
            password=db_params['pass'],
            db=db_params['database'],
            charset=db_params['charset'],
            cursorclass=pymysql.cursors.DictCursor
        )
    try:
        with mysql_connection.cursor() as cursor:
            sql = 'SELECT option_value FROM {:s}options WHERE option_name = "template"'.format(db_params['prefix'])
            cursor.execute(sql)
            result = cursor.fetchone()
            theme_name = result['option_value']
    finally:
        mysql_connection.close()

    return theme_name

def wordpress_install(the_readme, bash_shell):
    connection_params = dict([
        ('host', ''),
        ('database', ''),
        ('user', ''),
        ('pass', ''),
        ('prefix', ''),
        ('charset', ''),
        ('driver', '')
    ])

    package_dependencies = []

    accepted_drivers = [
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
        elif key.lower() == str('db_charset').lower():
            connection_params['charset'] = value
        else:
            continue

    try:
        YAML_config = yaml.safe_load(get_config()) or {}
        config_options = open(YAML_config, 'r')
        config_options = yaml.load(config_options)

        if config_options['database_driver'] and config_options['database_driver'] in accepted_drivers:
            connection_params['driver'] = config_options['database_driver']

        if config_options['dependencies']:
            for dependency in config_options['dependencies']:
                package_dependencies.append(dependency)

    except yaml.scanner.ScannerError as e:
        raise Exception(e)
    except Exception as e:
        print(type(e))

    wp_theme = parse_DB(connection_params) if True else False

    if not wp_theme:
        raise Exception("No active theme could be found for this WordPress installation")
        
    path_to_theme = os.path.join(os.getcwd(), 'wp-content', 'themes', wp_theme)

    if not os.path.isdir(path_to_theme):
        raise Exception("{:s} is not a valid theme path".format(path_to_theme))
        
    os.chdir(path_to_theme)

    for package_dependency in package_dependencies:
        if os.path.isfile(os.path.join(os.getcwd(), package_dependency)):
            print(package_dependency)
            

def laravel_install(the_readme, bash_shell):
    print("Laravel!!!")

def standard_install(the_readme, bash_shell):
    with open(the_readme) as file:
        character_count = len(file.read())
        while int(check_output('stat -c "%s" {:s}'.format(the_readme), shell=True, executable=bash_shell).decode('UTF-8')) == character_count:
            os.system('{:s} {:s}'.format(os.getenv('EDITOR'), the_readme))
