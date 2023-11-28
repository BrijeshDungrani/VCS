import tkinter as tk
from tkinter import messagebox
import dashboard  # Import the dashboard module

# Sample user credentials (replace with actual credentials)
user_credentials = {
    "username": "user",
    "password": "user"
}

def login():
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    if entered_username == user_credentials["username"] and entered_password == user_credentials["password"]:
        messagebox.showinfo("Login Successful", "Login successful")
        open_dashboard_window(entered_username)  # Pass the entered username to the dashboard
        root.destroy()  # Close the login window after successful login
    else:
        messagebox.showerror("Login Failed", "Login failed. Please check your username and password.")

def open_dashboard_window(username):
    # Call the show_dashboard function from the dashboard module with the username
    dashboard.show_dashboard(username)
    close_main_window()  # Close the main login window after redirecting to the dashboard

def close_main_window():
    root.destroy()

# Create the main login window
root = tk.Tk()
root.title("Login")

# Set the initial size of the window
root.geometry("400x200")

# Create and pack widgets for the login window
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")  # Mask the password input
password_entry.pack()

login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

# Start the tkinter main loop for the login window
root.mainloop()
