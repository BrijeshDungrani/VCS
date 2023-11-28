from FileOperation import FileOperations
import tkinter as tk
import os
import shutil
import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries")
import cst.interface as cst
from VersionGraph import VersionGraph
from tkinter import simpledialog


class VersionControlSystem:
    def __init__(self):

        self.initialize_button = None
        self.create_version_button = None
        self.open_version_button = None
        self.generate_branch_button = None
        self.change_branch_button = None
        self.dashboard_window = None
        self.active_branch_label = None
        self.retrieved_version_label = None
        self.status_label = None

        self.file_operations = FileOperations()

        self.xdelta3_executable = r'C:\Versioning\xdelta3.exe'
        self.Cache_folder = r"C:\Versioning\Cache"
        self.server_folder = r"C:\Versioning\Server"
        self.working_directory = r'C:\Versioning'
        self.project_name = None
        self.project_folder = None
        self.full_project_name = None
        self.project_folder_path_server = None
        self.project_folder_path_cache = None
        self.project_folder_info_path = None
        self.project_folder_info_path_server = None
        self.patch_master_file = None
        self.project_active_branch_file = None
        self.project_retrieved_version_file = None
        self.connected_project_name = None
        self.Active_branch = None
        self.Last_retrieved_version = None
        self.Active_branch_patch_details_file = None
        self.connected_to_repository = False


    def determine_patch_file_name(self):
        # Read the active branch from project_active_branch_file
       
        with open(self.project_active_branch_file, "r") as f:
            active_branch = f.readline().strip()

        # Determine the patch file name based on the active branch
        patch_file_name = f"{active_branch}V1.xdelta"

        # Check if there are existing patch versions for the active branch
        while os.path.exists(os.path.join(self.project_folder_path_server, patch_file_name)):
            # If an existing patch version exists, increment it by 1
            version_number = int(patch_file_name.split("V")[1].split(".xdelta")[0])
            version_number += 1
            patch_file_name = f"{active_branch}V{version_number}.xdelta"

        return patch_file_name
    
    def update_status_indicator(self, status_label):
        if self.connected_to_repository:
            self.status_label.config(text="Connected", bg="green")
            FileOperations.write_log(f"Project is connected")
        else:
            self.status_label.config(text="Disconnected", bg="red")
            FileOperations.write_log(f"Project is not connected")

    def initialize_repository(self):
        if not self.is_project_initialized():
            try:
                FileOperations.write_log(f"Start initialiying project")

                self.connected_to_repository = True
                self.update_status_indicator(self.status_label)
                self.initialize_button.config(state="disabled")  # Disable the initialize button after initialization
                self.create_version_button.config(state="active")  # Activate the create version button
                self.open_version_button.config(state="active")  # Activate the open version button
                self.change_branch_button.config(state="active")
                self.generate_branch_button.config(state="active")

                # Connect to CST Studio Suite and get project information
                de = cst.DesignEnvironment.connect_to_any_or_new()
                active_project = de.active_project()
                project_filename = active_project.filename()
                full_project_name = os.path.basename(project_filename)

                # Remove '.cst' from the project name
                project_name = os.path.splitext(full_project_name)[0]

                # Create a folder with the project name at C:\Versioning\Server
                FileOperations.write_log(f"Creating server folder")
                os.makedirs(self.server_folder, exist_ok=True)
                FileOperations.write_log(f"Creating cache folder")
                os.makedirs(self.Cache_folder, exist_ok=True)

                # Rename project_folder_path to project_folder_path_server
                project_folder_path = os.path.join(self.server_folder, project_name)
                FileOperations.write_log(f"Creating server folder for project : {project_name}")
                self.project_folder_path_server = project_folder_path + "_server"

                os.makedirs(self.project_folder_path_server, exist_ok=True)

                self.project_folder_info_path_server = os.path.join(self.project_folder_path_server, 'info')
                FileOperations.write_log(f"Creating Server info folder")

                os.makedirs(self.project_folder_info_path_server, exist_ok=True)
                FileOperations.write_log(f"Creating Server master file")
                self.patch_master_file = os.path.join(self.project_folder_info_path_server, "master.txt")

                self.Active_branch_patch_details_file = os.path.join(self.project_folder_info_path_server, f"{self.Active_branch}.txt")


                with open(self.patch_master_file, "w") as f:
                    FileOperations.write_log(f"Appending Init in the master file")
                    f.write("Init\n")

                project_folder_cache_path = os.path.join(self.Cache_folder, project_name)
                self.project_folder_path_cache = project_folder_cache_path + "_cache"
                FileOperations.write_log(f"Creating cache folder for project : {project_name}")
                os.makedirs(self.project_folder_path_cache, exist_ok=True)

                self.project_folder_info_path = os.path.join(self.project_folder_path_cache, 'info')
                FileOperations.write_log(f"Creating cache info folder for project : {project_name}")
                os.makedirs(self.project_folder_info_path, exist_ok=True)
                self.project_active_branch_file = os.path.join(self.project_folder_info_path, "ActiveBranch.txt")

                with open(self.project_active_branch_file, "w") as f:
                    FileOperations.write_log(f"writing master in the active branch : {self.project_active_branch_file}")
                    f.write("master\n")
                    self.Active_branch = self.file_operations.get_active_branch_from_file(self.project_active_branch_file)

                self.project_retrieved_version_file = os.path.join(self.project_folder_info_path, "RetrievedVersion.txt")
                FileOperations.write_log(f"Creating retrieved version file")

                with open(self.project_retrieved_version_file, "w") as f:
                    f.write("\n")
                    self.Last_retrieved_version = None

                # Copy the connected project file to project_folder_path_server as 'base.cst'
                FileOperations.write_log(f"Sending base.cst to the server and cache directory")

                shutil.copy(project_filename, os.path.join(self.project_folder_path_server, "base.cst"))
                shutil.copy(project_filename, os.path.join(self.project_folder_path_cache, "base.cst"))


                

            except Exception as e:
                # Handle exceptions (e.g., CST Studio Suite not installed or project not available)
                error_label = tk.Label(self.dashboard_window, text=f"Error: {str(e)}")
                error_label.pack()

    def update_active_branch_label(self):
        self.Active_branch = self.file_operations.get_active_branch_from_file(self.project_active_branch_file)

        if self.Active_branch and self.active_branch_label:
            self.Active_branch_patch_details_file = os.path.join(self.project_folder_info_path_server, f"{self.Active_branch}.txt")

            self.active_branch_label.config(text=f"Active Branch: {self.Active_branch}")
        elif self.active_branch_label:
            self.active_branch_label.config(text="Active Branch: (not set)")


    def get_version_description_from_user(self):
        # Create a simple dialog for entering a version description
        description = simpledialog.askstring("Version Description", "Enter a description for the version:")
        return description
      
    def create_version(self):
        global dashboard_window
        try:
            version_description = self.get_version_description_from_user()
            if FileOperations.is_patch_synchronized_with_server(self.Active_branch_patch_details_file, self.project_folder_path_cache):
                FileOperations.write_log(f"Version description is : {version_description}")
                FileOperations.write_log(f"Working project is properly synchronized with repository")
                FileOperations.write_log(f"start crearing new version in the branch {self.Active_branch}")

                full_project_name = self.connected_project_name
                current_file_path = os.path.join(self.project_folder_path_cache, "current.cst")
                shutil.copy(full_project_name,current_file_path)

                if self.Active_branch == 'master':
                    base_file_to_check = 'base.cst'
                    last_file_to_check = 'last.cst'
                    original_file_path = os.path.join(self.project_folder_path_cache, last_file_to_check)

                else:
                    #print(self.Active_branch_patch_details_file)
                    base_file_to_check = f"retrieved_{FileOperations.read_last_line(self.Active_branch_patch_details_file)}.cst"
                    #print(base_file_to_check)

                    last_file_to_check = f"last_{self.Active_branch}.cst"
                    original_file_path = os.path.join(self.project_folder_path_cache, last_file_to_check)


                # Define the path for the original file (last.cst or base.cst if last.cst doesn't exist)
                temp = 'last'
                if not os.path.exists(original_file_path):
                    original_file_path = os.path.join(self.project_folder_path_cache, base_file_to_check)
                    temp = 'base'

                # Define the path for the patch file with .xdelta extension
                patch_file_name = self.determine_patch_file_name()
                patch_file_path = os.path.join(self.project_folder_path_cache, patch_file_name)

                # Generate the patch file
                FileOperations.write_log(f"Start Patch generation")
                FileOperations.write_log(f"Original file : {original_file_path}")
                FileOperations.write_log(f"Modifies file : {current_file_path}")
                FileOperations.write_log(f"Patch file name : {patch_file_name}")
                FileOperations.generate_patch(original_file_path, current_file_path, patch_file_path)

                if temp != 'base':
                    FileOperations.write_log(f"Deleting Last file : {original_file_path}")
                    FileOperations.delete_file(original_file_path)
                new_last_file = os.path.join(self.project_folder_path_cache, last_file_to_check)
                FileOperations.write_log(f"set up new last file : {new_last_file}")
                FileOperations.rename_file(current_file_path, new_last_file)

                # Send the patch file to the server
                FileOperations.write_log(f"send patch file {patch_file_name} to the server")
                FileOperations.sendToServer(patch_file_path, self.project_folder_path_server)

                FileOperations.write_log(f"Append the new patch file {patch_file_name} into the {self.Active_branch_patch_details_file}")
                self.prepend_text_to_file(self.Active_branch_patch_details_file, patch_file_name)

                self.post_patch_generation_on_server(patch_file_name,self.Active_branch,self.Active_branch_patch_details_file)

                 # Update the retrieved version label with the new last retrieved version
                patch_file_name, _ = os.path.splitext(patch_file_name)

                retrieved_file = os.path.join(self.project_folder_path_cache, 'info', 'RetrievedVersion.txt')
                FileOperations.write_log(f"Appending the latest version {patch_file_name} as a retrieved version into: {retrieved_file}")
                FileOperations.prepend_text_to_file(retrieved_file, patch_file_name)
                self.Last_retrieved_version = patch_file_name
                self.retrieved_version_label.config(text=f"Last Retrieved Version: {self.Last_retrieved_version}")

                FileOperations.append_description(self.project_folder_info_path_server,patch_file_name, version_description)
                FileOperations.write_log("Appending description")

                FileOperations.write_log(f"Version {patch_file_name} created successfully into branch {self.Active_branch}")
                # Display a success message
                success_label = tk.Label(self.dashboard_window, text="Version created successfully!")
                success_label.pack()

            else:
                # The patch is not synchronized, show an error message
                FileOperations.write_log(f"Working project is not properly synchronized with repository")
                FileOperations.write_log(f"Please synchronize before creating a new version.")


                error_label = tk.Label(self.dashboard_window, text="Please synchronize before creating a new version.\nOpen the latest version of the current branch.")
                error_label.pack()

        except Exception as e:
            # Handle exceptions if any errors occur during version creation
            FileOperations.write_log(f"Error creating version: {str(e)}")

            error_label = tk.Label(self.dashboard_window, text=f"Error creating version: {str(e)}")
            error_label.pack()

    def open_version(self):
        branch_files = FileOperations.get_all_branch(self.project_folder_info_path_server)
        FileOperations.write_log(f"Available branches are : {branch_files}")
        branch_files = FileOperations.get_full_branch_file_paths(self.project_folder_info_path_server,branch_files)
        FileOperations.write_log(f"Opening version graph")
        VG = VersionGraph(branch_files,self)

    def is_project_initialized(self):
        try:
            de = cst.DesignEnvironment.connect_to_any_or_new()
            active_project = de.active_project()
            return active_project.is_initialized()
        except Exception as e:
            return False
        
  
    def getVersion(self, node_name):     
        desired_version = node_name
        version_number = FileOperations.version_name_to_number(desired_version)
        branch_name = FileOperations.extract_branch_name(desired_version)

        FileOperations.write_log(f"Start retrieval of version : {node_name} and branch name is {branch_name}")

        final_version_file = os.path.join(self.project_folder_path_cache, f'retrieved_{desired_version}.cst')

        # Determine whether to generate through cache or not
        base_file, patch_files = FileOperations.find_version_in_cache(desired_version, self.project_folder_path_cache, self.project_folder_info_path_server)

        generateThroughCache = base_file is not None and patch_files is not None
        try:

            if os.path.exists(final_version_file):
                FileOperations.write_log(f"{final_version_file} exist in a cache directory. let's bring full version from there cache")
            elif generateThroughCache:
                FileOperations.write_log(f"Full version is not available in cache")
                FileOperations.write_log(f"Possible to generate full version through cache")
                FileOperations.write_log(f"We have base file : {base_file} and required patches : {patch_files} in a cache to generate requested version through cache data")

                FileOperations.write_log(f"Start applying patch and generate version in a cache")
                FileOperations.apply_patches(base_file, patch_files, final_version_file, self.project_folder_path_server)
                FileOperations.write_log(f"Generated version is available in a cache : {final_version_file}")

            else:
                FileOperations.write_log(f"There is no possibility to generated {desired_version} through cache")
                FileOperations.write_log(f"We must have to download it from the server")

                if version_number % 7 == 0:
                    ready_cst = os.path.join(self.project_folder_path_server, f'{desired_version}.cst')
                    FileOperations.write_log(f"The requested version is devidable by 7 so we can directly download it from server : {ready_cst} ")
                    FileOperations.write_log(f"Downloading {ready_cst} from server")
                    shutil.copy(ready_cst, final_version_file)
                else:
                    base_file, patch_files = FileOperations.find_base_version_and_patches(desired_version, self.project_folder_path_server)
                    FileOperations.write_log(f"Generating {desired_version} through {base_file} and {patch_files}")
                    FileOperations.apply_patches(base_file, patch_files, final_version_file, self.project_folder_path_server)
                    FileOperations.write_log(f"{final_version_file} is downloaded and available in the cache directory")

            FileOperations.write_log(f"closing the project")
            FileOperations.close_project()

            FileOperations.write_log(f"Deleting working project folder and cst file")
            FileOperations.delete_directory(self.project_folder)

            if os.path.exists(self.full_project_name):
                os.remove(self.full_project_name)

            FileOperations.write_log(f"Setting up the new desired version")
            working_version_file = os.path.join(self.working_directory, f'{desired_version}.cst')
            shutil.copy(final_version_file, working_version_file)

            if os.path.exists(working_version_file):
                os.rename(working_version_file, self.full_project_name)

            retrieved_file = os.path.join(self.project_folder_path_cache, 'info', 'RetrievedVersion.txt')
            FileOperations.write_log(f"updating {retrieved_file} with latest retrieved version")
            FileOperations.prepend_text_to_file(retrieved_file, desired_version)
            self.Last_retrieved_version = desired_version
            self.retrieved_version_label.config(text=f"Last Retrieved Version: {self.Last_retrieved_version}")
            FileOperations.write_log(f"updating active branch and file with {branch_name} branch")
            FileOperations.update_active_branch_to_file(self.project_active_branch_file,branch_name)  
            self.update_active_branch_label()
            FileOperations.write_log(f"Opening the project")
            FileOperations.open_project(self.full_project_name)
            FileOperations.write_log(f"Version retrieved successfully")

        except Exception as e:
            # Handle any exceptions here, e.g., log the error, display an error message, or take corrective action.
            FileOperations.write_log(f"An error occurred: {str(e)}")

    
    def create_new_branch(self):
        last_retrieved_version = self.Last_retrieved_version
        last_version_number = FileOperations.version_name_to_number(last_retrieved_version)
        print(f"Last version number is : {last_version_number}")
        # Ask the user if they want to create a new branch with the last retrieved version
        confirmation = tk.messagebox.askquestion(
            "Create New Branch",
            f"Do you want to create a new branch with the base version set to the last retrieved version ({last_retrieved_version})?",
        )

        if confirmation == "yes":
            new_branch_name = f"branch{last_version_number}"
            FileOperations.write_log(f"Generating new branch : {new_branch_name}")
            self.new_branch_file = os.path.join(self.project_folder_info_path_server, f"{new_branch_name}.txt")
            with open(self.new_branch_file, "w") as f:
                    FileOperations.write_log(f"New branch file {self.new_branch_file} created and {last_retrieved_version} appended as a base version of new branch : {new_branch_name}")                    
                    f.write(f"{last_retrieved_version}\n")
            FileOperations.write_log(f"Active branch file and label updated with newly created branch as an active branch")
            FileOperations.update_active_branch_to_file(self.project_active_branch_file,new_branch_name)  
            self.update_active_branch_label()
                    
    def get_active_branch_from_file(self, file_path):
        return self.file_operations.get_active_branch_from_file(file_path)

    def read_first_line(self, file_path):
        return self.file_operations.read_first_line(file_path)
    
    def prepend_text_to_file(self, file_path,text):
        return self.file_operations.prepend_text_to_file(file_path,text)
    
    def post_patch_generation_on_server(self, patch_file_name,active_branch, active_branch_file):
        try:
            FileOperations.write_log(f"Post patch generation start")
            # Extract the version number from the patch file name (e.g., 'masterV1.xdelta' -> 1)
            version_number = int(patch_file_name.split('V')[1].split('.')[0])            
            FileOperations.write_log(f"Version number is : {version_number}")
            # Check if the version number is divisible by 7
            if version_number % 7 == 0:
                FileOperations.write_log(f"Version number is divisable by 7, let's generate full version on server as a post operation on server")
                base_number = version_number - 7
                base_cst = f"{active_branch}V{base_number}.cst"
                new_base_cst = f"{active_branch}V{version_number}.cst"

                if version_number == 7:
                    FileOperations.write_log(f"It's first time genrating 7th version on server for branch : {active_branch}")

                    if active_branch == 'master':
                        base_cst = "base.cst"
                    else:
                        base_cst = f"{FileOperations.read_last_line(active_branch_file)}.cst"
                FileOperations.write_log(f"base cst is : {base_cst} and new fully version is : {new_base_cst}")

                
                FileOperations.write_log(f"Getting 7 patch files from {self.Active_branch_patch_details_file}")
                top_patches = FileOperations.read_top_lines(self.Active_branch_patch_details_file,7)
                FileOperations.write_log(f"Patches are : {top_patches}")
                
                base_file = os.path.join(self.project_folder_path_server, base_cst)

                final_version_file = os.path.join(self.project_folder_path_server, new_base_cst)

                FileOperations.apply_patches(base_file, top_patches, final_version_file, self.project_folder_path_server)
                FileOperations.write_log(f"New fully version has been generated on server as a post operation,new version files on server is {final_version_file}")
        except Exception as e:
            # Handle exceptions if any errors occur during post-patch generation
            # You can log or handle the error as needed
            pass

    
    
