import json
import subprocess
import platform
from pathlib import Path
from typing import Dict, List


class PackageInstaller:
    """Package and MCP installer implementation."""

    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.is_mac = self.system == "darwin"

    def run_command(self, command: str) -> bool:
        """Run a shell command and return success status."""
        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running command '{command}': {e}")
            return False

    def check_command_exists(self, command: str) -> bool:
        """Check if a command exists in the system PATH."""
        try:
            where_cmd = "where" if self.is_windows else "which"
            subprocess.run(
                f"{where_cmd} {command}",
                shell=True,
                check=True,
                capture_output=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def check_mcp_exists(self, mcp_name: str) -> bool:
        """Check if a MCP exists in the system PATH."""
        config = self.get_claude_config_json()
        if config:
            mcp_servers = config.get("mcpServers", [])
            return mcp_name in mcp_servers
        return False

    def get_claude_config_json(self) -> str:
        """Get the claude config json file."""
        if self.is_mac:
            config_path = Path.joinpath(
                Path.home(),
                "Library",
                "Application Support",
                "Claude",
                "claude_desktop_config.json",
            )
        elif self.is_windows:
            config_path = Path.joinpath(
                Path.home(),
                "AppData",
                "Roaming",
                "Claude",
                "claude_desktop_config.json",
            )

        if config_path.exists():
            with open(config_path, "r") as f:
                return json.load(f)

        return None

    def get_available_packages(self) -> List[str]:
        """Get list of available packages."""
        return ["bun", "node"]

    def get_available_mcps(self) -> List[str]:
        """Get list of available MCPs."""
        return ["playwright"]

    def install_package(self, package_name: str) -> Dict[str, bool]:
        return {package_name: self.install_single_package(package_name)}

    def install_single_package(self, package_name: str) -> bool:
        """Install a single package."""
        install_methods = {
            "bun": self.install_bun,
            "node": self.install_node,
        }

        if package_name not in install_methods:
            print(f"Unknown package: {package_name}")
            return False

        print(f"\nInstalling {package_name}...")
        return install_methods[package_name]()

    def install_mcp(self, mcp_name: str) -> Dict[str, bool]:
        return {mcp_name: self.install_single_mcp(mcp_name)}

    def install_single_mcp(self, mcp_name: str) -> bool:
        """Install a single MCP."""
        install_methods = {
            "playwright": self.install_playwright,
        }

        if mcp_name not in install_methods:
            print(f"Unknown MCP: {mcp_name}")
            return False

        print(f"\nInstalling {mcp_name}...")
        return install_methods[mcp_name]()

    def install_bun(self) -> bool:
        """Install Bun runtime."""
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

        return self.run_command(command)

    def install_node(self) -> bool:
        """Install Node.js runtime."""
        if self.is_windows:
            if self.check_command_exists("fnm"):
                print("Node.js is already installed")
                return True

            command = (
                "winget install Schniz.fnm && "
                "refreshenv && "  # Refresh environment variables
                "$env:Path = [System.Environment]::"
                "GetEnvironmentVariable('Path','Machine') + ';' + "
                "[System.Environment]::"
                "GetEnvironmentVariable('Path','User') && "
                "fnm install 22"
            )

        elif self.is_mac:
            if self.check_command_exists("node"):
                print("Node.js is already installed")
                return True

            command = (
                "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/"
                "v0.40.1/install.sh | bash && "
                'export NVM_DIR="$HOME/.nvm" && '
                '[ -s "$NVM_DIR/nvm.sh" ] && \\. "$NVM_DIR/nvm.sh" && '
                '[ -s "$NVM_DIR/bash_completion" ] && '
                '\\. "$NVM_DIR/bash_completion" && '
                "nvm install 22"
            )

        return self.run_command(command)

    def install_playwright(self) -> bool:
        """Install Playwright MCP."""
        # TODO: Implement Playwright MCP installation
        return False
