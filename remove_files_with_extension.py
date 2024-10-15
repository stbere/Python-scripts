import os

# This script removes files with a specified extension from a given directory and its subdirectories.
# To use this script:
# 1. Save it to a file, for example, `remove_files_with_extension.py` just like I have it named here.
# 2. Run the script using Python. You can do this by opening a terminal or command prompt,
#    navigating to the directory where the script is saved, and running `python remove_files_with_extension.py`.
# 3. Enter the path to the directory you want to clean up when prompted.
# 4. Enter the file extension you want to remove (e.g., .md5, .xlsx, .ico, .png).

def remove_files_with_extension(directory, extension):
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file ends with the specified extension
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                print(f'Removing {file_path}')
                os.remove(file_path)  # Remove the file

if __name__ == '__main__':
    # This line below will prompt the user to enter the path to the directory
    target_directory = input("Enter the path to the directory: ")
    
    # This next line below (you will see it in the terminal when you run the script) will prompt the user to enter the file extension to remove
    # Example extensions: .md5, .xlsx, .ico, .png, .jpeg, .pdf, whatever you are hating on and want removed out of your folders!
    file_extension = input("Enter the file extension to remove (e.g., .md5, .xlsx, .ico, .png): ")
    
    # Call the function to remove files with the specified extension
    remove_files_with_extension(target_directory, file_extension)
