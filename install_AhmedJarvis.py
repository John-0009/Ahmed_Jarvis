import sys
import os
import subprocess
import hashlib
import getpass

# =============================================
#   AHMED J.A.R.V.I.S — SECURE INSTALLER
#   Password change karne ke liye:
#   python -c "import hashlib; print(hashlib.sha256('NEWPASSWORD'.encode()).hexdigest())"
#   Woh hash CORRECT_HASH mein paste karo
# =============================================

CORRECT_HASH = hashlib.sha256("AhmedJarvis2025".encode()).hexdigest()
JARVIS_REPO  = "https://github.com/YOUR_USERNAME/YOUR_REPO.git"  # <-- apna repo link yahan

REQUIRED_PACKAGES = [
    "google-genai",
    "sounddevice",
    "PyQt6",
    "requests",
    "pyautogui",
    "pillow",
    "opencv-python",
]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║                                                      ║")
    print("  ║          A H M E D   J . A . R . V . I . S          ║")
    print("  ║              Personal AI  —  Est. 2025               ║")
    print("  ║                                                      ║")
    print("  ║              [ SECURE  INSTALLER  v1.0 ]             ║")
    print("  ║                                                      ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print()

def denied_banner():
    clear()
    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║                                                      ║")
    print("  ║          A H M E D   J . A . R . V . I . S          ║")
    print("  ║                                                      ║")
    print("  ║   ✖   WRONG PASSWORD  —  ACCESS DENIED   ✖          ║")
    print("  ║       Installation has been cancelled.               ║")
    print("  ║                                                      ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print()

def ready_banner():
    clear()
    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║                                                      ║")
    print("  ║          A H M E D   J . A . R . V . I . S          ║")
    print("  ║                                                      ║")
    print("  ║          ✔   INSTALLATION COMPLETE, SIR   ✔         ║")
    print("  ║                                                      ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print()

def check_password():
    banner()
    print("  ┌─────────────────────────────────────────────────┐")
    print("  │   This system is private and access-protected.  │")
    print("  │   Unauthorized access is strictly prohibited.   │")
    print("  └─────────────────────────────────────────────────┘")
    print()
    for attempt in range(3):
        try:
            pwd = getpass.getpass(f"  🔐 Password (attempt {attempt+1}/3): ")
        except (KeyboardInterrupt, EOFError):
            print("\n\n  [!] Installer cancelled by user.")
            sys.exit(1)

        if hashlib.sha256(pwd.encode()).hexdigest() == CORRECT_HASH:
            print()
            print("  ✔  Access granted. Welcome, Sir.\n")
            return True
        else:
            remaining = 2 - attempt
            if remaining > 0:
                print(f"  ✖  Wrong password. {remaining} attempt(s) remaining.\n")
            else:
                denied_banner()
                sys.exit(1)

def check_python():
    print("  ──────────────────────────────────────────────────")
    print("  STEP 1 — Checking System Requirements")
    print("  ──────────────────────────────────────────────────")
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        print(f"  ✖  Python 3.10+ required. You have {v.major}.{v.minor}")
        print("     Download: https://www.python.org/downloads/")
        sys.exit(1)
    print(f"  ✔  Python {v.major}.{v.minor}.{v.micro} detected — OK")
    print()

def install_packages():
    print("  ──────────────────────────────────────────────────")
    print("  STEP 2 — Installing Required Packages")
    print("  ──────────────────────────────────────────────────")
    for pkg in REQUIRED_PACKAGES:
        print(f"  →  {pkg:<30}", end=" ", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
            capture_output=True
        )
        print("✔" if result.returncode == 0 else "✖ (check manually)")
    print()

def check_git():
    return subprocess.run(["git", "--version"], capture_output=True).returncode == 0

def clone_or_update():
    jarvis_dir = os.path.join(os.path.expanduser("~"), "AHMED-JARVIS")
    print("  ──────────────────────────────────────────────────")
    print("  STEP 3 — Downloading AHMED J.A.R.V.I.S")
    print("  ──────────────────────────────────────────────────")

    if os.path.exists(jarvis_dir):
        print("  →  Existing installation found — updating...")
        result = subprocess.run(
            ["git", "-C", jarvis_dir, "pull"],
            capture_output=True, text=True
        )
        print("  ✔  Updated successfully.\n" if result.returncode == 0 else "  !  Could not update (using existing files)\n")
    else:
        print("  →  Cloning from secure repository...")
        if not check_git():
            print("  ✖  Git not found.")
            print("     Install git from: https://git-scm.com")
            sys.exit(1)
        result = subprocess.run(
            ["git", "clone", JARVIS_REPO, jarvis_dir],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("  ✔  Download complete.\n")
        else:
            print(f"  ✖  Failed: {result.stderr}")
            sys.exit(1)
    return jarvis_dir

def launch_jarvis(jarvis_dir):
    main_py = os.path.join(jarvis_dir, "main.py")
    if not os.path.exists(main_py):
        print("  ✖  main.py not found. Please check installation.")
        sys.exit(1)

    ready_banner()
    print(f"  📁  Installed at: {jarvis_dir}")
    print()
    launch = input("  ▶  Launch AHMED J.A.R.V.I.S now? (y/n): ").strip().lower()
    if launch == "y":
        subprocess.Popen([sys.executable, main_py], cwd=jarvis_dir)
        print()
        print("  ✔  Jarvis is online, Sir. You may close this window.")
        print()
    else:
        print()
        print("  To launch later, open CMD and run:")
        print(f'  cd "{jarvis_dir}" && python main.py')
        print()

def main():
    check_password()
    check_python()
    install_packages()
    jarvis_dir = clone_or_update()
    launch_jarvis(jarvis_dir)

if __name__ == "__main__":
    main()
