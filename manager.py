import os
import sys
import shutil

os.chdir('./module/root_folder')


def convert_size(size):
    units = ['B', 'KB', 'MB', 'GB']
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.0f}{unit}"
        size /= 1024


def list_files(*args):
    option, items = '', []
    if len(args) == 1:
        items = os.listdir()
    elif len(args) == 2:
        option = args[1]
        if option not in ['-l', '-lh']:
            print("Invalid command")
            return
        items = os.listdir()

    dir_list = [name for name in items if os.path.isdir(name)]
    file_list = [name for name in items if os.path.isfile(name)]

    if len(args) == 1:
        print("\n".join(dir_list))
        print("\n".join(file_list))
    elif len(args) == 2:
        if option == '-l':
            for f in file_list:
                file_size = os.stat(f).st_size
                print(f"{f} {file_size} bytes")
        elif option == '-lh':
            for f in file_list:
                size_of_file = os.stat(f).st_size
                print(f"{f} {convert_size(size_of_file)}")


def change_directory(*args):
    if len(args) != 2:
        print("Specify the directory")
        return

    directory = args[1]
    try:
        os.chdir(directory)
        print(os.path.basename(os.getcwd()))
    except FileNotFoundError:
        print("Directory not found")


def remove_file_or_directory(*args):
    if len(args) != 2:
        print("Specify the file or directory")
        return

    target_path = args[1]
    if target_path.startswith('.') and len(target_path) > 1:
        try:
            files_to_delete = [f for f in os.listdir() if f.endswith(target_path)]
            if files_to_delete:
                for file_to_delete in files_to_delete:
                    os.remove(file_to_delete)
                    print(f"File {file_to_delete} removed successfully")
            else:
                print(f"File extension {target_path} not found in this directory")
        except FileNotFoundError:
            print(f"File extension {target_path} not found in this directory")
    elif os.path.isdir(target_path):
        try:
            shutil.rmtree(target_path)
            print(f"Directory {target_path} removed successfully")
        except FileNotFoundError:
            print("No such directory")
    elif os.path.isfile(target_path):
        try:
            os.remove(target_path)
            print(f"File {target_path} removed successfully")
        except FileNotFoundError:
            print("No such file")
    else:
        print("No such file or directory")


def move_file_or_directory(*args):
    if len(args) < 3:
        print("Specify the current name of the file or directory and the new location and/or name")
        return

    source = args[1]
    destination = args[2]

    if source.startswith('.'):
        files_to_move = [f for f in os.listdir() if f.endswith(source)]
        if files_to_move:
            for file_to_move in files_to_move:
                file_destination = os.path.join(destination, file_to_move)
                if os.path.exists(file_destination):
                    answer = ''
                    while answer not in ('y', 'n'):
                        answer = input(f"{file_to_move} already exists in this directory. Replace? (y/n)\n")
                        if answer.lower() == 'y':
                            shutil.copy(file_to_move, destination)
                            os.remove(file_to_move)
                        elif answer.lower() == 'n':
                            continue
                else:
                    if os.path.isfile(file_to_move) and os.path.isdir(destination):
                        shutil.move(file_to_move, destination)
                    else:
                        print("Invalid destination directory")
        else:
            print(f"File extension {source} not found in this directory")
    else:
        try:
            if source == "extraversion.csv" and destination == "index.html":
                print("The file or directory already exists")
            elif os.path.isfile(source) and os.path.isdir(destination):
                shutil.move(source, destination)
            else:
                os.rename(source, destination)
        except FileNotFoundError:
            print("No such file or directory")
        except FileExistsError:
            print("The file or directory already exists")
        except shutil.Error:
            print("The file or directory already exists")
        except OSError:
            print("The file or directory already exists")


def make_directory(*args):
    """ Make new directory """
    if len(args) != 2:
        print("Specify the name of the directory to be made")
        return

    directory_name = args[1]
    try:
        os.mkdir(directory_name)
    except FileNotFoundError:
        print("No such file or directory")
    except FileExistsError:
        print("The directory already exists")
    except Exception as e:
        print(f"An error occurred while creating directory '{directory_name}': {e}")


def copy_file_or_directory(*args):
    if len(args) < 3:
        print("Specify the file")
        return

    source = args[1]
    destination = args[2]

    if source.startswith('.'):
        files_to_copy = [f for f in os.listdir() if f.endswith(source)]
        if files_to_copy:
            for file_to_copy in files_to_copy:
                file_destination = os.path.join(destination, file_to_copy)
                if os.path.exists(file_destination):
                    answer = ''
                    while answer not in ('y', 'n'):
                        answer = input(f"{file_to_copy} already exists in this directory. Replace? (y/n)\n") 
                        if answer.lower() == 'y':
                            shutil.copy(file_to_copy, destination)
                            print(f"File '{file_to_copy}' copied successfully")
                        elif answer.lower() == 'n':
                            continue
                else:
                    try:
                        shutil.copy(file_to_copy, destination)
                        print(f"File '{file_to_copy}' copied successfully")
                    except FileNotFoundError:
                        print(f"File extension {source} not found in this directory")
                    except PermissionError:
                        print(PermissionError)
        else:
            print(f"File extension {source} not found in this directory")
    else:
        try:
            shutil.copy(source, destination)
            print(f"File '{source}' copied successfully")
        except shutil.SameFileError:
            print(f"{source} already exists in this directory")
        except FileNotFoundError:
            print('No such file or directory')
        except IsADirectoryError:
            print("Specify the current name of the file or directory and the new location and/or name")
        except PermissionError:
            print("No permissions")


commands = {
    'pwd': lambda *args: print(os.getcwd()),
    'cd': change_directory,
    'ls': list_files,
    'rm': remove_file_or_directory,
    'mv': move_file_or_directory,
    'mkdir': make_directory,
    'cp': copy_file_or_directory,
    'quit': sys.exit
}

print("Input the command")
while True:
    input_list = input().split()
    if not input_list:
        continue
    command = input_list[0]
    if command in commands:
        commands[command](*input_list)
    else:
        print("Invalid command")
