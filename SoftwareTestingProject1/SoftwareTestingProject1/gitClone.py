import subprocess
import os
from urllib.parse import urlparse
import psutil

import shutil

class GitCloning:
    def __init__(self):
       # self.repository_url=repository_url
       pass
    

    def clone_git_repository(self, repository_url):
        if repository_url is None:
            print("Repository URL cannot be None")
            raise ValueError("Repository URL cannot be None")
            
        try:
            # GitHub deposunun adını al
            repo_name = os.path.splitext(os.path.basename(urlparse(repository_url).path))[0]
                    
            # Masaüstü dizin yolunu belirle.
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            #Bu satır, masaüstü dizinini oluşturur. 
            os.makedirs(desktop_path, exist_ok=True)

            # Hedef dizini oluşturmadan önce aynı ısımle klasor varsa kontrol et
            target_dir = os.path.join(desktop_path, repo_name)
            counter = 1
            while os.path.exists(target_dir):
                target_dir = os.path.join(desktop_path, f"{repo_name} ({counter})")
                counter += 1
            os.makedirs(target_dir, exist_ok=True)

            # Git deposunu klonla
            subprocess.check_output(['git', 'clone', repository_url, target_dir], stderr=subprocess.STDOUT)        
            print("Cloned successfully")

        except subprocess.CalledProcessError as e:
            print("Failed to clone repository")
            print("Error:", e)
            return None
        
        return target_dir  # Klonlanan dizinin yolunu döndür

        
    
    def kill_processes_using_directory(self,directory):
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if proc.info['cmdline'] and directory in proc.cwd():
                    print(f"Terminating process: {proc.pid} - {proc.info['name']}")
                    proc.terminate()
                print("Processes using the directory are terminated successfully.")
        except Exception as e:
            print(f"Error while terminating processes: {e}")
    
    
    # def set_permissions(self,file_path):
    #     try:
    #         subprocess.run(['icacls', file_path, '/grant', '*S-1-1-0:(OI)(CI)F'], check=True)
    #         print(f"Permissions set successfully for: {file_path}")
    #     except subprocess.CalledProcessError as e:
    #         print(f"Failed to set permissions for: {file_path}")
    #         print("Error:", e)