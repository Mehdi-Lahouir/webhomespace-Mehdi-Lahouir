import hashlib
import subprocess
from model import user
from passlib.hash import sha512_crypt
from dataclasses import dataclass
import crypt

@dataclass
class UserAccount:
    def Login(self, User: user) -> bool:
        username = User.name
        password = User.password
        sudo_password="42316421"
        command = f"echo {sudo_password} | sudo -S cat /etc/shadow | grep {username}"
        output = subprocess.check_output(command, shell=True)
        if output:
            hashed_password = output.decode().strip().split(":")[1]
            if crypt.crypt(password, hashed_password) == hashed_password:
                return True
            else:
                return False

    def zipfile(self,User:user)->bool:
        username=User.name
        password=User.password
        hostname='rike-VirtualBox'
        command = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{hostname} 'cd /home/{username} && tar czvf - .' | cat > /tmp/homedir.zip"
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            raise Exception("Failed to create zip file")
        else:
            return True
    
    def getFiles(self,username):

        cmd = f'sudo ls -la /home/{username}'  
        output = subprocess.check_output(cmd.split(), universal_newlines=True)
        lines = output.strip().split('\n')[1:]
        files = []
        for line in lines:
            parts = line.split()
            if len(parts) < 9:  
                continue
            filetype = 'Directory' if parts[0].startswith('d') else 'File'
            filename = parts[-1]
            modified = ' '.join(parts[5:8])
            size = int(parts[4])
            files.append({'name': filename, 'type': filetype, 'size': size, 'modified': modified})
        return files
    def getFiles(self,username,name):

        cmd = f'sudo ls -la /home/{username}/{name}'  
        output = subprocess.check_output(cmd.split(), universal_newlines=True)
        lines = output.strip().split('\n')[1:]
        files = []
        for line in lines:
            parts = line.split()
            if len(parts) < 9:  
                continue
            filetype = 'Directory' if parts[0].startswith('d') else 'File'
            filename = parts[-1]
            modified = ' '.join(parts[5:8])
            size = int(parts[4])
            files.append({'name': filename, 'type': filetype, 'size': size, 'modified': modified})
        return files
    def get_total_size(self,username,password):
        command = "sudo -S du -sh /home/{username}"
        output = subprocess.check_output(command, shell=True, input=password.encode(), universal_newlines=True)
        size = output.split()[0]
        return size
    def get_num_dirs(self,username,password):
        command = "sudo -S ls -l /home/{username} | grep '^d' | wc -l"
        output = subprocess.check_output(command, shell=True, input=password.encode(), universal_newlines=True)
        num_directories = int(output.strip())

        return num_directories
    def get_num_files(self,username,password):
        command = "sudo -S ls -l /home/{username} | grep '^f' | wc -l"
        output = subprocess.check_output(command, shell=True, input=password.encode(), universal_newlines=True)
        num_files= int(output.strip())

        return num_files