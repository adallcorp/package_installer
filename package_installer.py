#!/usr/bin/env python3
import subprocess
import platform
from typing import Dict


class PackageInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.is_mac = self.system == "darwin"
        self.is_linux = self.system == "linux"

    def run_command(self, command: str) -> bool:
        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running command '{command}': {e}")
            return False

    def check_command_exists(self, command: str) -> bool:
        try:
            where_cmd = "where" if self.is_windows else "which"
            subprocess.run(
                f"{where_cmd} {command}", shell=True, check=True, capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def install_bun(self) -> bool:
        if self.check_command_exists("bun"):
            print("Bun is already installed")
            return True

        if self.is_windows:
            print("Bun installation on Windows requires PowerShell...")
            command = 'powershell -c "irm bun.sh/install.ps1|iex"'
        elif self.is_mac:
            if self.check_command_exists("brew"):
                command = "brew install bun"
            else:
                command = "curl -fsSL https://bun.sh/install | bash"
        else:  # Linux
            command = "curl -fsSL https://bun.sh/install | bash"

        return self.run_command(command)

    def install_node(self) -> bool:
        if self.check_command_exists("node"):
            print("Node.js is already installed")
            return True

        if self.is_windows:
            command = (
                "winget install Schniz.fnm && "
                "refreshenv && "  # Refresh environment variables
                "$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + "
                "[System.Environment]::GetEnvironmentVariable('Path','User') && "
                "fnm install 22"
            )
        elif self.is_mac:
            command = (
                "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash && "
                'export NVM_DIR="$HOME/.nvm" && '
                '[ -s "$NVM_DIR/nvm.sh" ] && \\. "$NVM_DIR/nvm.sh" && '  # Load nvm
                '[ -s "$NVM_DIR/bash_completion" ] && \\. "$NVM_DIR/bash_completion" && '  # Load completion
                "nvm install 22"
            )

        else:  # Linux
            command = (
                "curl -fsSL https://deb.nodesource.com/setup_lts.x | "
                "sudo -E bash - && sudo apt-get install -y nodejs"
            )

        return self.run_command(command)

    def install_uv(self) -> bool:
        if self.check_command_exists("uv"):
            print("uv is already installed")
            return True

        if self.is_windows:
            command = (
                'powershell -Command "irm https://astral.sh/uv/install.ps1' ' | iex"'
            )
        else:  # Mac and Linux
            command = "curl -LsSf https://astral.sh/uv/install.sh | sh"

        return self.run_command(command)


def main():
    installer = PackageInstaller()

    print("Starting installation of package managers...")

    # Install each package manager
    installers = [
        ("Bun", installer.install_bun),
        ("Node.js", installer.install_node),
        ("uv", installer.install_uv),
    ]

    results: Dict[str, bool] = {}
    for name, install_func in installers:
        print(f"\nInstalling {name}...")
        results[name] = install_func()

    # Print summary
    print("\nInstallation Summary:")
    print("-" * 30)
    for name, success in results.items():
        status = "Success" if success else "Failed"
        print(f"{name}: {status}")


if __name__ == "__main__":
    main()
