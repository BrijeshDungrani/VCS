import shutil
import subprocess
import os
import sys
from datetime import datetime
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries")
import cst.interface as cst

class FileOperations:

    @staticmethod
    def read_first_line(file_path):
        try:
            with open(file_path, "r") as file:
                first_line = file.readline()
                return first_line.strip()  # Remove any leading/trailing whitespace and return the line
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}")
        return None

    @staticmethod
    def get_active_branch_from_file(project_active_branch_file):
        try:
            with open(project_active_branch_file, 'r') as file:
                active_branch = file.read().strip()
            return active_branch
        except FileNotFoundError:
            print(f"File '{project_active_branch_file}' not found.")
            return None
    @staticmethod
    def read_last_line(file_path):
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    return last_line  # Remove any leading/trailing whitespace and return the last line
                else:
                    return None  # The file is empty
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}")
        return None

    @staticmethod
    def get_all_branch(info_directory):
        try:
            branch_files = []
            for filename in os.listdir(info_directory):
                if filename.endswith(".txt") and 'description' not in filename:  # Adjust the file extension as needed
                    branch_name = os.path.splitext(filename)[0]  # Remove the ".txt" extension
                    branch_files.append(branch_name)

            return branch_files
        except Exception as e:
            print(f"An error occurred while getting branch filenames: {str(e)}")
            return []
    
    @staticmethod
    def get_full_branch_file_paths(info_server_path, branch_files):
        full_paths = [os.path.join(info_server_path, branch_file + '.txt') for branch_file in branch_files]
        return full_paths
    
    @staticmethod
    def is_patch_synchronized_with_server(active_branch_patch_details_file, cache_directory):
        last_patch_of_current_branch_on_server = FileOperations.read_first_line(active_branch_patch_details_file)

        if 'xdelta' in last_patch_of_current_branch_on_server:
            patch_to_check = os.path.join(cache_directory, last_patch_of_current_branch_on_server)
            
            if os.path.exists(patch_to_check):
                return True
            else:
                return False

        return True
    
    @staticmethod
    def append_description(server_info_path, patch_name, description):
        # Check if the description file exists or not
        description_file_path = os.path.join(server_info_path, "description.txt")

        if os.path.exists(description_file_path):
            # Description file exists, open it for appending
            with open(description_file_path, "a") as desc_file:
                desc_file.write(f"{patch_name}={description}\n")
        else:
            # Description file doesn't exist, create it and write the description
            with open(description_file_path, "w") as desc_file:
                desc_file.write(f"{patch_name}={description}\n")

    @staticmethod
    def get_description_for_version(server_info_path, version_name):
        description_file_path = os.path.join(server_info_path, "description.txt")

        if os.path.exists(description_file_path):
            # Description file exists, read descriptions as a dictionary
            descriptions = {}
            with open(description_file_path, "r") as desc_file:
                for line in desc_file:
                    parts = line.strip().split("=")
                    if len(parts) == 2:
                        patch_name, description = parts
                        descriptions[patch_name] = description
            return descriptions.get(version_name, "No description available")
        else:
            return "No description file found."

    @staticmethod
    def update_active_branch_to_file(project_active_branch_file, new_active_branch):
        try:
            with open(project_active_branch_file, 'w') as file:
                file.write(new_active_branch)
            print(f"Active branch updated to '{new_active_branch}' in file: {project_active_branch_file}")
        except FileNotFoundError:
            print(f"File '{project_active_branch_file}' not found.")
        except Exception as e:
            print(f"An error occurred while updating the active branch in the file: {str(e)}")


    @staticmethod
    def prepend_text_to_file(file_path, text):
        try:
            # Read the existing content of the file
            with open(file_path, "r") as file:
                existing_content = file.read()

            # Create the new content by prepending the provided text to the existing content
            new_content = text + "\n" + existing_content

            # Write the updated content back to the file
            with open(file_path, "w") as file:
                file.write(new_content)

            #print("Text prepended to the file successfully.")
        except Exception as e:
            print("An error occurred:", str(e))

    @staticmethod
    def rename_file(current_path, new_name):
        try:
            os.rename(current_path, new_name)
        except FileNotFoundError:
            print("File not found.")
        except FileExistsError:
            print(f"A file with the name '{new_name}' already exists.")
        except Exception as e:
            print(f"An error occurred while renaming the file: {str(e)}")

    @staticmethod
    def sendToServer(x,y):
        shutil.copy(x,y)

    @staticmethod 
    def delete_file(file_path):
            try:
                os.remove(file_path)
            except FileNotFoundError:
                print("File not found.")
            except PermissionError:
                print("Permission denied while deleting the file.")
            except Exception as e:
                print(f"An error occurred while deleting the file: {str(e)}")

    @staticmethod
    def read_version_names_from_file(file_path):
        result = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    result.append(line.strip())
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return result
    
    @staticmethod
    def filter_result(result):
        filtered_result = []

        for item in result:
            if isinstance(item, str):
                # Check for '.xdelta' and remove it
                if item.endswith('.xdelta'):
                    item = item[:-7]  # Remove the last 7 characters (".xdelta")

                # Check for 'masterVersion' and rename it to 'MV'
                if 'masterVersion' in item:
                    item = item.replace('masterVersion', 'MV')

            filtered_result.append(item)

        return filtered_result
    
    @staticmethod
    def read_top_lines(filename, number_of_lines):
        result = []
        try:
            with open(filename, 'r') as file:
                for i in range(number_of_lines):
                    line = file.readline()
                    if 'Init' in line:
                        continue
                    if not line:
                        break  # Reached the end of the file
                    result.append(line.strip())  # Append the line to the result list
        except Exception as e:
            # Handle exceptions if any errors occur during file reading
            # You can log or handle the error as needed
            pass

        return result[::-1]
    
    @staticmethod
    def delete_directory(directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)

    @staticmethod
    def open_project(cstFilePath):
        deNew = cst.DesignEnvironment.connect_to_any_or_new()
        prj = deNew.open_project(cstFilePath)
    
    @staticmethod
    def close_project():
        de = cst.DesignEnvironment.connect_to_any_or_new()
        de.close()
    
    @staticmethod
    def generate_patch(original_file, modified_file, patch_file):
        xdelta3_executable = r'C:\Versioning\xdelta3.exe'

        command = [
            xdelta3_executable,
            '-f',
            '-s', original_file,
            modified_file,
            patch_file
        ]
        
        subprocess.run(command, check=True)

    @staticmethod
    def apply_xdelta_patch(original_file, patch_file, generated_file):
        xdelta3_executable = r'C:\Versioning\xdelta3.exe'

        command = [
            xdelta3_executable,
            '-f',
            '-d',
            '-s', original_file,
            patch_file,
            generated_file
        ]
        subprocess.run(command, check=True)

    @staticmethod
    def apply_patches(base_file, patch_files, output_file, server_dir):
        generated_file = base_file
        intermediate_files = []

        for patch_file in patch_files:
            #print(f"Patch file is : {patch_file}")
            intermediate_file = FileOperations.apply_xdelta_patch_to_file(generated_file, os.path.join(server_dir, patch_file))
            intermediate_files.append(intermediate_file)
            generated_file = intermediate_file

        os.rename(generated_file, output_file)

        for intermediate_file in intermediate_files:
            if os.path.exists(intermediate_file):
                os.remove(intermediate_file)

    @staticmethod
    def apply_xdelta_patch_to_file(original_file, patch_file):
        generated_file = FileOperations.generate_temp_file_name(patch_file)
        FileOperations.apply_xdelta_patch(original_file, patch_file, generated_file)
        return generated_file

    @staticmethod
    def generate_temp_file_name(patch_file):
        patch_base_name = os.path.basename(patch_file)
        server_dir = r'C:\Versioning\Server\SimulationProject_server'
        return os.path.join(server_dir, f'temp_{patch_base_name[:-7]}.cst')

    @staticmethod
    def version_name_to_number(version_name):
        number = ''
        for char in reversed(version_name):
            if char == 'V':
                break
            number = char + number

        if number:
            number = int(number)
            return number
        else:
            return None
        
    @staticmethod
    def extract_branch_name(version_name):
        # Split the version name by 'V' and take the first part as the branch name
        parts = version_name.split('V', 1)
        if len(parts) > 0:
            return parts[0]
        else:
            return None
        

    
    @staticmethod
    def find_base_version_and_patches(desired_version, project_folder_path_server):
            version_number = FileOperations.version_name_to_number(desired_version)
            branch_name = FileOperations.extract_branch_name(desired_version)
            if version_number <= 7:
                if branch_name == 'master':
                    base_file = os.path.join(project_folder_path_server, 'base.cst')
                else:
                    server_info_dir = os.path.join(project_folder_path_server, 'info')
                    requested_branch_file = os.path.join(server_info_dir, branch_name + '.txt')
                    version_name = f'{FileOperations.read_last_line(requested_branch_file)}.cst'
                    base_file = os.path.join(project_folder_path_server, version_name)
                    
                return base_file, [os.path.join(project_folder_path_server, f'{branch_name}V{i}.xdelta') for i in range(1, version_number + 1)]
            else:
                base_version_number = (version_number // 7) * 7


                base_version = os.path.join(project_folder_path_server, f'{branch_name}V{base_version_number}.cst')
                patches = [os.path.join(project_folder_path_server, f'{branch_name}V{i}.xdelta') for i in range(base_version_number + 1, version_number + 1)]
                return base_version, patches

            return None, []
        


    @staticmethod
    def get_required_patch_files(folder_path, desired_version):
        required_patch_files = []

        for filename in os.listdir(folder_path):
            if filename.endswith('.xdelta'):
                version_name = filename.split('.')[0]

                if version_name <= desired_version:
                    required_patch_files.append(filename)

        return required_patch_files
    
    @staticmethod
    def find_version_in_cache(desired_version, cache_directory,server_info_dir, max_attempts=5):
        version_to_check = FileOperations.version_name_to_number(desired_version)
        branch_name = FileOperations.extract_branch_name(desired_version)
          # Get the numeric part of the desired_version
        patch_list = []  # Initialize an empty list for patch 
        #print(f'branch name is : {branch_name}')
        for _ in range(max_attempts):
            if version_to_check == 0:
                #print(f'version to check is :{version_to_check}')
                if branch_name == 'master':
                    version_name = 'base.cst'
                else:
                    requested_branch_file = os.path.join(server_info_dir, branch_name + '.txt')
                    version_name = f'retrieved_{FileOperations.read_last_line(requested_branch_file)}.cst'
                    #print(f"version_name : {version_name}")
            else:
                version_name = f'retrieved_{branch_name}V{version_to_check}.cst'
            #print(f"Checking for {version_name}")
            version_file = os.path.join(cache_directory, version_name)
            if os.path.exists(version_file):
                return version_file, list(reversed(patch_list))  # Return .cst file and the list of patch files in reverse order
            patch_list.append(f'{branch_name}V{version_to_check}.xdelta')  # Add the patch file to the list
            if version_to_check == 0:
                return None, None
            version_to_check -= 1
               
        return None, None
    
    @staticmethod
    def write_log(log_text, log_file_path=None):
        """
        Write log information to a log file with a timestamp. New entries are added to the top.

        Args:
            log_text (str): The text to be written to the log file.
            log_file_path (str): The path to the log file (default: None).

        Returns:
            bool: True if the log was written successfully, False otherwise.
        """


        try:
            if log_file_path is None:
                log_file_path = 'C:\\Versioning\\log.txt'

            log_directory = os.path.dirname(log_file_path)
            if not os.path.exists(log_directory):
                    os.makedirs(log_directory)
                

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - {log_text}"

            # Read the current contents of the log file
            with open(log_file_path, "r") as log_file:
                current_logs = log_file.read()

            # Create a new log content with the new entry on top
            new_log_content = f"{log_entry}\n{current_logs}"

            # Write the new log content back to the log file
            with open(log_file_path, "w") as log_file:
                log_file.write(new_log_content)

            return True
        except Exception as e:
            print(f"Error writing to log file: {str(e)}")
            return False



