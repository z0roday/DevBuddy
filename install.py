import sys
import subprocess
import shutil
import os
import requests
from devbuddy.animations import animate_install

def check_command(command):
    """Check if a command exists."""
    return shutil.which(command) is not None

def install_package(package, pip=True):
    """Install a package using pip or npm."""
    if pip and check_command(package.split('>=')[0]):
        print(f"{package} is already installed.")
        return
    if not pip and check_command(package.split('/')[0]):
        print(f"{package} is already installed.")
        return
    try:
        if pip:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"{package} installed successfully!")
        else:
            npm_path = shutil.which("npm") or r"C:\Program Files\nodejs\npm.cmd"
            subprocess.run([npm_path, "install", "-g", package], check=True, shell=True)
            print(f"{package} installed successfully!")
    except subprocess.CalledProcessError:
        print(f"{package} installation failed.")

def install_language(language):
    """Install a language runtime if not present."""
    if language == "node":
        if check_command("node"):
            print("Node.js is already installed.")
            return True
        if input("Node.js is not installed. Should I install it? (y/n): ").lower() == 'y':
            animate_install("Node.js")
            url = "https://nodejs.org/dist/v20.17.0/node-v20.17.0-x64.msi"
            installer = "node-installer.msi"
            with open(installer, "wb") as f:
                f.write(requests.get(url, stream=True).content)
            subprocess.run(["msiexec", "/i", installer, "/quiet"], check=True)
            os.remove(installer)
            if check_command("node"):
                print("Node.js installed successfully!")
                return True
            else:
                print("Node.js installation failed.")
                return False
        return False
    elif language == "php":
        if check_command("php"):
            print("PHP is already installed.")
            return True
        if input("PHP is not installed. Should I install it? (y/n): ").lower() == 'y':
            animate_install("PHP")
            url = "https://windows.php.net/downloads/releases/php-8.3.13-nts-Win32-vs16-x64.zip"
            zip_file = "php.zip"
            try:
                with open(zip_file, "wb") as f:
                    f.write(requests.get(url, stream=True).content)
                with ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall("C:\\PHP")
                os.environ["PATH"] += os.pathsep + "C:\\PHP"
                os.remove(zip_file)
                if check_command("php"):
                    print("PHP installed successfully!")
                    return True
                else:
                    print("PHP installation failed.")
                    return False
            except Exception as e:
                print(f"PHP installation failed: {e}")
                return False
        return False
    elif language == "java":
        if check_command("java"):
            print("Java is already installed.")
            return True
        if input("Java is not installed. Should I install it? (y/n): ").lower() == 'y':
            animate_install("Java")
            print("Java requires manual installation due to Oracle licensing. Download from: https://www.oracle.com/java/technologies/javase-downloads.html")
            return False
        return False
    return True

def setup_devbuddy():
    """Setup DevBuddy with all prerequisites."""
    os.environ["PATH"] += os.pathsep + r"C:\Program Files\nodejs" + os.pathsep + r"C:\PHP"

    if check_command("dbuddy"):
        action = input("DevBuddy is already installed. Update (u), Uninstall (r), Check missing (c)? (u/r/c): ").lower()
        if action == 'u':
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "."], check=True)
            print("DevBuddy updated successfully!")
            return
        elif action == 'r':
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "z0roday-devbuddy", "-y"], check=True)
            print("DevBuddy uninstalled. Running fresh setup...")
        elif action == 'c':
            pass
        else:
            print("Invalid choice. Exiting.")
            return
    
    response = input("Do you want to install all tools and frameworks? (y/n): ").lower()
    install_all = response == 'y'
    
    if not check_command("python"):
        print("Error: Python is not installed. Download from: https://www.python.org/downloads/")
        sys.exit(1)
    
    print("Installing DevBuddy dependencies...")
    python_deps = ["click", "black", "autopep8", "django", "flask", "fastapi", "uvicorn", "requests"]
    js_deps = ["@vue/cli", "create-react-app", "@angular/cli"]
    php_deps = ["laravel/laravel"]
    
    for dep in python_deps:
        install_package(dep, pip=True)
    
    js_installed = False
    if install_all or input("Install JavaScript frameworks? (y/n): ").lower() == 'y':
        if install_language("node"):
            js_installed = True
            for dep in js_deps:
                install_package(dep, pip=False)
    if not js_installed:
        print("JavaScript frameworks skipped. Use 'dbuddy install js-frameworks' to install later.")
    
    php_installed = False
    if install_all or input("Install PHP frameworks? (y/n): ").lower() == 'y':
        if install_language("php"):
            php_installed = True
            if not check_command("composer"):
                animate_install("Composer")
                url = "https://getcomposer.org/Composer-Setup.exe"
                installer = "composer-setup.exe"
                with open(installer, "wb") as f:
                    f.write(requests.get(url).content)
                subprocess.run([installer, "/silent"], check=True)
                os.remove(installer)
                if check_command("composer"):
                    print("Composer installed successfully!")
                else:
                    print("Composer installation failed.")
            if check_command("composer"):
                install_package("laravel/laravel", pip=False)
    if not php_installed:
        print("PHP frameworks skipped. Use 'dbuddy install php-frameworks' to install later.")
    
    java_installed = False
    if install_all or input("Install Java frameworks? (y/n): ").lower() == 'y':
        java_installed = install_language("java")
    if not java_installed:
        print("Java frameworks skipped. Use 'dbuddy install java-frameworks' to install later.")
    
    print("Installing z0roday-devbuddy...")
    subprocess.run([sys.executable, "-m", "pip", "install", "."], check=True)
    print("DevBuddy installed successfully! Use 'dbuddy' to start.")

if __name__ == "__main__":
    setup_devbuddy()