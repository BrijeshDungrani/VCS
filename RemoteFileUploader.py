import paramiko

class RemoteFileUploader:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh_client = None
    
    def connect(self):
        try:
            # Create an SSH client instance
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.load_system_host_keys()  # Load known_hosts file

            # Connect to the remote server
            self.ssh_client.connect(self.hostname, port=self.port, username=self.username, password=self.password)
            return True
        except Exception as e:
            print(f"Error connecting to the remote server: {str(e)}")
            return False
    
    def upload_file(self, local_path, remote_path):
        if not self.ssh_client:
            print("Not connected to the remote server. Call 'connect()' first.")
            return False
        
        try:
            # Create an SFTP session for file transfer
            sftp = self.ssh_client.open_sftp()

            # Upload the local file to the remote server
            sftp.put(local_path, remote_path)

            # Close the SFTP session
            sftp.close()

            print(f"File '{local_path}' uploaded to '{remote_path}' on the remote server.")
            return True

        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return False
    
    def close(self):
        if self.ssh_client:
            self.ssh_client.close()

uploader = RemoteFileUploader("remote-server.com", 22, "your_username", "your_password")
if uploader.connect():
    uploader.upload_file("/path/to/local/file.txt", "/path/to/remote/file.txt")
    uploader.close()
