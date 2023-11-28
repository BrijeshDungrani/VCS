import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
from FileOperation import FileOperations

class VersionGraph:
    def __init__(self, branch_files, vcs):
        self.G, self.node_positions = self.create_version_graph(branch_files)
        self.vcs = vcs

        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Version Graph')
        self.draw_graph()


    def on_node_click(self, event):
        if event.inaxes is not None and event.inaxes.get_title() == 'Version Graph':
            for node in self.G.nodes():
                if (
                    (self.node_positions[node][0] - 0.1 < event.xdata < self.node_positions[node][0] + 0.1) and
                    (self.node_positions[node][1] - 0.1 < event.ydata < self.node_positions[node][1] + 0.1)
                ):
                    response = simpledialog.askstring(
                        "Version Retrieval", f"Do you really want to retrieve version: {self.get_node_name_with_description(node)}?\nType 'yes' to confirm:"
                    )
                    if response and response.lower() == 'yes':
                        self.vcs.getVersion(node)
                    plt.draw()


    def create_version_graph(self, branch_files):
        G = nx.DiGraph()
        node_positions = {}
        x_spacing = 2  # Adjust this value to control horizontal spacing between nodes

        current_x = 0  # Initialize the x-coordinate for the current branch
        current_y = 0  # Initialize the y-coordinate for the current branch

        for branch_file in branch_files:
            version_list = FileOperations.read_version_names_from_file(branch_file)
            version_list = FileOperations.filter_result(version_list)

            for i in range(len(version_list) - 1):
                current_version = version_list[i]
                next_version = version_list[i + 1]

                G.add_edge(next_version, current_version)

                # Assign the x-coordinate with additional spacing for nodes within the same branch
                #if branch_file != r"C:\Versioning\Server\SimulationProject_server\info\branch2.txt" and i != 0:
                node_positions[current_version] = (current_x * x_spacing, current_y)
                node_positions[next_version] = ((current_x + 1) * x_spacing, current_y)


                current_x += 1  # Increase the x-coordinate for the next node

            # Move to the next horizontal row for the next branch
            current_y += 0.5
            current_x = 0  # Reset the x-coordinate for the next branch

        return G, node_positions



        #return G, node_positions
    def get_node_name_with_description(self, version_name):
        description = FileOperations.get_description_for_version(self.vcs.project_folder_info_path_server, version_name)
        return f"{version_name} and Description : ({description})"

    def draw_graph(self):
        pos = self.node_positions
        node_colors = ["skyblue" if not node.startswith(self.vcs.Last_retrieved_version) else "red" for node in self.G.nodes()]
        nx.draw(self.G, pos, with_labels=True, node_size=1000, node_color=node_colors, font_size=6, font_color="black")
        self.fig.canvas.mpl_connect('button_press_event', self.on_node_click)
        plt.show()


