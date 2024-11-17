import os
import subprocess
import sys
import platform
import zipfile
import tarfile
import urllib.request
import shutil

def install_packages():
    """Install required Python packages from requirements.txt."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_yt_dlp():
    """Ensure yt-dlp is installed and available."""
    try:
        subprocess.run(["yt-dlp", "--version"], check=True)
        print("yt-dlp is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing yt-dlp...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])

def setup_ffmpeg():
    """Ensure ffmpeg is installed and in the system PATH."""
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print("ffmpeg is already installed and in PATH.")
        return

    # Download and setup ffmpeg based on the OS
    ffmpeg_url = ""
    system = platform.system()
    
    if system == "Windows":
        ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n5.1-latest-win64-gpl.zip"
    elif system == "Linux":
        ffmpeg_url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
    elif system == "Darwin":  # macOS
        ffmpeg_url = "https://evermeet.cx/ffmpeg/getrelease/ffmpeg.zip"

    if not ffmpeg_url:
        print("ffmpeg installation is not supported on this OS.")
        return
    
    print("Downloading ffmpeg...")
    ffmpeg_archive = "ffmpeg.zip" if system in ["Windows", "Darwin"] else "ffmpeg.tar.xz"
    urllib.request.urlretrieve(ffmpeg_url, ffmpeg_archive)
    
    ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
    os.makedirs(ffmpeg_dir, exist_ok=True)

    # Extract the ffmpeg archive
    if ffmpeg_archive.endswith(".zip"):
        with zipfile.ZipFile(ffmpeg_archive, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
    elif ffmpeg_archive.endswith(".tar.xz"):
        with tarfile.open(ffmpeg_archive, 'r:xz') as tar_ref:
            tar_ref.extractall(ffmpeg_dir)

    # Locate ffmpeg executable within the extracted files
    ffmpeg_executable = None
    for root, dirs, files in os.walk(ffmpeg_dir):
        for file in files:
            if file == "ffmpeg" or file == "ffmpeg.exe":
                ffmpeg_executable = os.path.join(root, file)
                break

    if not ffmpeg_executable:
        print("ffmpeg download failed or could not find the executable.")
        return

    # Add ffmpeg to PATH
    ffmpeg_bin_path = os.path.dirname(ffmpeg_executable)
    os.environ["PATH"] += os.pathsep + ffmpeg_bin_path

    # Permanent PATH addition (Windows only)
    if system == "Windows":
        import winreg as reg
        reg_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path, 0, reg.KEY_ALL_ACCESS) as key:
            current_path = reg.QueryValueEx(key, "Path")[0]
            if ffmpeg_bin_path not in current_path:
                new_path = current_path + ";" + ffmpeg_bin_path
                reg.SetValueEx(key, "Path", 0, reg.REG_EXPAND_SZ, new_path)

    print("ffmpeg is set up successfully.")

if __name__ == "__main__":
    install_packages()
    setup_yt_dlp()
    setup_ffmpeg()
    print("Setup complete. Please restart the terminal or command prompt to apply PATH changes if on Windows.")
