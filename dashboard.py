import tkinter as tk
import sys
import os
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries")
import cst.interface as cst
from FileOperation import FileOperations
from VCS import VersionControlSystem

class Dashboard:
    def __init__(self, username):
        self.connected_to_repository = False
        self.dashboard_window = None
        self.vcs = VersionControlSystem()
        self.username = username



    def change_branch(self):
        if self.connected_to_repository:
            FileOperations.write_log(f"\n Start:Changing Branch ")
            branch_list = self.vcs.file_operations.get_all_branch(self.vcs.project_folder_info_path_server)
            FileOperations.write_log(f"Available branches to switch:")
            if not branch_list:
                tk.messagebox.showinfo("No Branches", "No branches available.")
                FileOperations.write_log(f"No available branches to switch")
                return

            # Create a pop-up dialog to select a branch
            branch_selection_window = tk.Toplevel(self.dashboard_window)
            branch_selection_window.title("Select Branch")

            branch_label = tk.Label(branch_selection_window, text="Select a branch:")
            branch_label.pack()

            branch_listbox = tk.Listbox(branch_selection_window)
            for branch in branch_list:
                branch_listbox.insert(tk.END, branch)
            branch_listbox.pack()

            def select_branch():
                selected_index = branch_listbox.curselection()
                if selected_index:
                    selected_branch = branch_listbox.get(selected_index[0])
                    FileOperations.write_log(f"Selected branch to switch is : {selected_branch}")
                    self.vcs.file_operations.update_active_branch_to_file(self.vcs.project_active_branch_file, selected_branch)
                    FileOperations.write_log(f"Active branch is {selected_branch} and it is updated in{self.vcs.project_active_branch_file}")
                    self.vcs.update_active_branch_label()
                    branch_selection_window.destroy()

            select_button = tk.Button(branch_selection_window, text="Select", command=select_branch)
            select_button.pack()



    def show_dashboard(self):
        self.dashboard_window = tk.Tk()
        self.dashboard_window.title("Dashboard")
        self.dashboard_window.geometry("400x200")
        FileOperations.write_log('Dashboard initialized')
        welcome_label = tk.Label(self.dashboard_window, text=f"Welcome, {self.username}!")
        welcome_label.pack()

        button_frame = tk.Frame(self.dashboard_window)
        button_frame.pack()

        self.vcs.initialize_button = tk.Button(button_frame, text="Initialize", command=self.vcs.initialize_repository)
        self.vcs.initialize_button.pack(side="left", padx=5)

        self.vcs.create_version_button = tk.Button(button_frame, text="Create Version", command=self.vcs.create_version, state="disabled")
        self.vcs.create_version_button.pack(side="left", padx=5)

        self.vcs.open_version_button = tk.Button(button_frame, text="Open Version", command=self.vcs.open_version, state="disabled")
        self.vcs.open_version_button.pack(side="left", padx=5)

        self.vcs.generate_branch_button = tk.Button(button_frame, text="Generate New Branch", command=self.vcs.create_new_branch, state="disabled")
        self.vcs.generate_branch_button.pack(side="left", padx=5)

        self.vcs.change_branch_button = tk.Button(self.dashboard_window, text="Change Branch", command=self.change_branch,state="disabled")
        self.vcs.change_branch_button.pack()



        self.vcs.status_label = tk.Label(self.dashboard_window, text="Disconnected", bg="red", width=10)
        self.vcs.status_label.pack()


        try:
            # Connect to CST Studio Suite and get project information
            de = cst.DesignEnvironment.connect_to_any_or_new()
            active_project = de.active_project()
            self.vcs.full_project_name = active_project.filename()
            self.vcs.project_folder = active_project.folder()
            self.vcs.connected_project_name = self.vcs.full_project_name
            self.vcs.project_name = os.path.splitext(os.path.basename(self.vcs.full_project_name))[0]
            project_folder_path = os.path.join(self.vcs.server_folder, self.vcs.project_name)
            self.vcs.project_folder_path_server = project_folder_path + "_server"
            project_folder_cache_path = os.path.join(self.vcs.Cache_folder, self.vcs.project_name)
            self.vcs.project_folder_path_cache = project_folder_cache_path + "_cache"
            self.vcs.project_folder_info_path = os.path.join(self.vcs.project_folder_path_cache, 'info')
            self.vcs.project_folder_info_path_server = os.path.join(self.vcs.project_folder_path_server, 'info')
            self.vcs.patch_master_file = os.path.join(self.vcs.project_folder_info_path_server, "master.txt")
            self.vcs.project_active_branch_file = os.path.join(self.vcs.project_folder_info_path, "ActiveBranch.txt")
            self.vcs.project_retrieved_version_file = os.path.join(self.vcs.project_folder_info_path, "RetrievedVersion.txt")


            base_file_path = os.path.join(self.vcs.project_folder_path_server, "base.cst")
            if os.path.exists(base_file_path):
                self.vcs.create_version_button.config(state="active")
                self.vcs.open_version_button.config(state="active")
                self.vcs.generate_branch_button.config(state="active")
                self.vcs.change_branch_button.config(state="active")
                self.vcs.initialize_button.config(state="disabled")
                self.vcs.status_label.config(text="Connected", bg="green")
                self.connected_to_repository = True
                FileOperations.write_log(f'Connected with : {self.vcs.full_project_name}')
                self.vcs.Active_branch = self.vcs.file_operations.get_active_branch_from_file(self.vcs.project_active_branch_file)
                self.vcs.Active_branch_patch_details_file = os.path.join(self.vcs.project_folder_info_path_server, f"{self.vcs.Active_branch}.txt")
                self.vcs.Last_retrieved_version = self.vcs.read_first_line(self.vcs.project_retrieved_version_file)
            #self.vcs.update_status_indicator(self.vcs.status_label)

            project_info_label = tk.Label(self.dashboard_window, text=f"Connected Project: {self.vcs.project_name}\nProject Folder: {self.vcs.project_folder}")
            project_info_label.pack()

            active_branch_label = tk.Label(self.dashboard_window, text=f"Active Branch: {self.vcs.Active_branch}")
            active_branch_label.pack()
            self.vcs.active_branch_label = active_branch_label

            retrieved_version_label = tk.Label(self.dashboard_window, text=f"Last Retrieved Version: {self.vcs.Last_retrieved_version}")
            retrieved_version_label.pack()
            self.vcs.retrieved_version_label = retrieved_version_label  # Save a reference to the label in your VersionControlSystem instance


        except Exception as e:
            error_label = tk.Label(self.dashboard_window, text=f"Error: {str(e)}")
            error_label.pack()
        self.vcs.dashboard_window = self.dashboard_window 
        self.dashboard_window.mainloop()

    

if __name__ == "__main__":
    username = "Max"
    dashboard = Dashboard(username)
    dashboard.show_dashboard()
