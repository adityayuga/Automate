import os
import sys
import getpass


# define for global variable
base_path = '/var/www/'
default_os_user = 'ss'
default_os_group = 'ss'


# download laravel from the source
# create project based input name given
def download_laravel(name):
    path = base_path + name
    composer_command = 'composer create-project --prefer-dist laravel/laravel'
    cmd = '%s %s' % (composer_command, path)
    os.system(cmd)


# normalize input string
def normalize_input_string(str):
    # change space with underscore
    str.replace(' ', '_')
    # lowering case
    str.lower()

    return str


# validate project name
def validate_project_name(name):
    # check name already exist or not
    if os.path.exists(base_path + name):
        return False

    return True


# set permission for project directory
def set_project_permission(name, user, group):
    # set write rule
    project_path = base_path + name
    storage_path = project_path + '/storage'
    chmod_command = 'chmod -R 775'
    chown_command = 'chown -R %s:%s' % (user, group)
    cmd = '%s %s' % (chmod_command, storage_path)
    os.system(cmd)
    cmd = '%s %s' % (chown_command, project_path)
    os.system(cmd)


# set env file laravel
def set_env_file(project_name, db_name, db_user, db_password):
    project_path = base_path + project_name
    env_example_path = project_path + '/.env.example'
    env_path = project_path + '/.env'
    env_example_file = open(env_example_path, 'r')
    env_file = open(env_path, 'w')

    for line in env_example_file.readlines():
        # set config
        if 'APP_NAME' in line:
            env_file.write('APP_NAME=' + project_name + '\n')
        elif 'DB_DATABASE' in line:
            env_file.write('DB_DATABASE=' + db_name + '\n')
        elif 'DB_USERNAME' in line:
            env_file.write('DB_USERNAME=' + db_user + '\n')
        elif 'DB_PASSWORD' in line:
            env_file.write('DB_PASSWORD=' + db_password + '\n')
        else:
            env_file.write(line)

    env_example_file.close()
    env_file.close()


# get input name of the project
def ask_project_name():
    name = input('Enter project name: ')
    name = normalize_input_string(name)
    return name


# get input name of the database
def ask_database_name():
    name = input('Enter database name: ')
    name = normalize_input_string(name)
    return name


# get input name of the database user
def ask_database_user():
    user = input('Enter database user: ')
    user = normalize_input_string(user)
    return user


# get input name of the database password
def ask_database_password():
    return getpass.getpass('Enter database password: ')


# run
os.system('sudo su')
# ask project name and other credential
project_name = ask_project_name()
db_name = ask_database_name()
db_user = ask_database_user()
db_password = ask_database_password()

# validate project name, if fail, print error
if not validate_project_name(project_name):
    os.system('exit')
    sys.exit()

# install laravel
download_laravel(project_name)
# setting permission on laravel project folder
set_project_permission(project_name, default_os_user, default_os_group)
# setting env file
set_env_file(project_name, db_name, db_user, db_password)

# end
os.system('exit')
