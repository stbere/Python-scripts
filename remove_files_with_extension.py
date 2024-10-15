import os

def remove_files_with_extension(directory, extension):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                print(f'Removing {file_path}')
                os.remove(file_path)

if __name__ == '__main__':
    target_directory = input("Enter the path to the directory: ")
    file_extension = input("Enter the file extension to remove (e.g., .md5, .xlsx, .ico, .png): ")
    remove_files_with_extension(target_directory, file_extension)