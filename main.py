import subprocess
import platform
import argparse
import json
import os

from pathlib import Path
from typing import Dict, List


class PackageInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.is_mac = self.system == "darwin"

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
                f"{where_cmd} {command}",
                shell=True,
                check=True,
                capture_output=True,
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

        return self.run_command(command)

    def install_node(self) -> bool:
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

    def get_available_packages(self) -> List[str]:
        return ["bun", "node"]

    def install_package(self, package_name: str) -> bool:
        install_methods = {
            "bun": self.install_bun,
            "node": self.install_node,
        }

        if package_name not in install_methods:
            print(f"Unknown package: {package_name}")
            return False

        print(f"\nInstalling {package_name}...")
        return install_methods[package_name]()

    def mcp_server_list(self) -> bool:
        pass

    def install_playwright(self) -> bool:
        pass

    def get_claude_config(self) -> Dict:
        """Read Claude Desktop configuration file."""
        if self.is_windows:
            appdata = Path(os.getenv("APPDATA", ""))
            config_path = appdata / "Claude" / "claude_desktop_config.json"
        elif self.is_mac:
            base_path = "Library/Application Support/Claude"
            config_path = Path.home().joinpath(base_path, "claude_desktop_config.json")
        else:
            raise RuntimeError("This feature is only supported on Windows and macOS")

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="패키지 매니저 설치 프로그램",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="사용 가능한 명령어")

    # Install command
    install_parser = subparsers.add_parser(
        "install",
        help="패키지 매니저 설치",
        description="지정된 패키지 매니저를 설치합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  %(prog)s bun             # bun만 설치
  %(prog)s node bun        # node와 bun 설치
  %(prog)s                # 모든 패키지 설치
""",
    )
    install_parser.add_argument(
        "packages",
        nargs="*",
        help="설치할 패키지 목록 (bun, node). "
        "지정되지 않으면 모든 패키지를 설치합니다.",
        metavar="PACKAGE",
    )

    # List command
    subparsers.add_parser(
        "list",
        help="사용 가능한 패키지 매니저 목록 표시",
        description="설치 가능한 모든 패키지 매니저 목록을 표시합니다.",
    )

    # Show arguments command
    show_parser = subparsers.add_parser(
        "show",
        help="명령어 상세 정보 표시",
        description="특정 명령어의 상세 정보와 사용 가능한 인자들을 표시합니다.",
    )
    show_parser.add_argument(
        "command_name", choices=["install", "list"], help="상세 정보를 볼 명령어"
    )

    # Config command
    subparsers.add_parser(
        "config",
        help="Claude Desktop 설정 파일 표시",
        description="Claude Desktop의 설정 파일 내용을 표시합니다.",
    )

    return parser


def show_command_help(parser: argparse.ArgumentParser, command_name: str) -> None:
    """특정 명령어의 상세 도움말을 표시합니다."""
    if command_name == "install":
        print("\n[install 명령어 상세 정보]")
        print("-" * 40)
        print("사용법: package_installer install [PACKAGE...]")
        print("\n사용 가능한 인자:")
        print("  PACKAGE  설치할 패키지 이름 (선택사항)")
        print("\n설치 가능한 패키지:")
        print("  - bun   : Bun 자바스크립트 런타임")
        print("  - node  : Node.js 자바스크립트 런타임")
        print("\n예시:")
        print("  package_installer install bun      # bun만 설치")
        print("  package_installer install node bun  # node와 bun 설치")
        print("  package_installer install         # 모든 패키지 설치")

    elif command_name == "list":
        print("\n[list 명령어 상세 정보]")
        print("-" * 40)
        print("사용법: package_installer list")
        print("\n설명: 설치 가능한 모든 패키지 목록을 표시합니다.")


def main():
    parser = create_parser()
    args = parser.parse_args()

    installer = PackageInstaller()

    if args.command == "show":
        show_command_help(parser, args.command_name)
        return

    if args.command == "list":
        print("\n사용 가능한 패키지:")
        print("-" * 20)
        for package in installer.get_available_packages():
            print(f"- {package}")
        return

    if args.command == "config":
        try:
            config = installer.get_claude_config()
            print("\nClaude Desktop 설정:")
            print("-" * 40)
            print(json.dumps(config, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        return

    if args.command == "install":
        packages_to_install = (
            args.packages if args.packages else installer.get_available_packages()
        )

        results: Dict[str, bool] = {}
        for package in packages_to_install:
            results[package] = installer.install_package(package)

        # Print summary
        print("\n설치 요약:")
        print("-" * 30)
        for name, success in results.items():
            status = "성공" if success else "실패"
            print(f"{name}: {status}")
        return

    # If no command is provided, show help
    parser.print_help()


if __name__ == "__main__":
    main()
