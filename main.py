import argparse
import os
import tarfile
import zipfile

class VShell:
    def __init__(self, fs_archive):
        self.fs_archive = fs_archive
        self.current_dir = '/'
        self.load_filesystem()

    def load_filesystem(self):
        if tarfile.is_tarfile(self.fs_archive):
            with tarfile.open(self.fs_archive, 'r') as tar:
                tar.extractall()

        elif zipfile.is_zipfile(self.fs_archive):
            with zipfile.ZipFile(self.fs_archive, 'r') as zipf:
                zipf.extractall()

    def run_command(self, command):
        if command.startswith("pwd"):
            print(self.current_dir)
        elif command.startswith("ls"):
            self.list_directory()
        elif command.startswith("cd"):
            self.change_directory(command.split(" ")[1])
        elif command.startswith("cat"):
            self.cat_file(command.split(" ")[1])

    def list_directory(self):
        with os.scandir(self.current_dir) as entries:
            for entry in entries:
                print(entry.name)


    def change_directory(self, directory):
        new_dir = os.path.join(self.current_dir, directory)
        if os.path.exists(new_dir) and os.path.isdir(new_dir):
            self.current_dir = new_dir
        else:
            print(f"Directory '{new_dir}' does not exist.")

    def cat_file(self, filename):
        file_path = os.path.join(self.current_dir, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                print(content)
        else:
            print(f"File '{file_path}' does not exist.")

    def run_script(self, script_file):
        with open(script_file, 'r') as script:
            for line in script:
                self.run_command(line.strip())

def main():
    parser = argparse.ArgumentParser(description="vshell - Virtual Shell Emulator")
    parser.add_argument("fs_archive", help="Filesystem archive (tar or zip)")
    parser.add_argument("--script", help="Script file to execute")
    args = parser.parse_args()

    vshell = VShell(args.fs_archive)

    if args.script:
        vshell.run_script(args.script)
    else:
        while True:
            command = input("$ ")
            if command.lower() == "exit":
                break
            vshell.run_command(command)

if __name__ == "__main__":
    main()
