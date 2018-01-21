import os

def which_infrastructure():
    
    if os.path.isdir(os.path.join(os.getcwd(), 'wp-includes').strip()) or os.path.isdir(os.path.join(os.getcwd(), 'wp-admin').strip()):
        wordpress_install()
    elif os.path.isfile(os.path.join(os.getcwd(), 'artisan')):
        laravel_install()
    else:
        standard_install()

def standard_install():
    print("This is a standard install.") 
