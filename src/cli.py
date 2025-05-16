"""Command-line interface for package installer."""

import argparse
import json
from typing import List

from .installer import PackageInstaller


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="패키지 매니저 설치 프로그램",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="사용 가능한 명령어")

    # Install command
    install_parser = subparsers.add_parser(
        "install",
        help="패키지 또는 MCP 설치",
        description="지정된 패키지 또는 MCP를 설치합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            사용 예시:
            %(prog)s bun             # bun만 설치
            %(prog)s node bun        # node와 bun 설치
        """,
    )

    install_parser.add_argument(
        "packages",
        nargs="+",
        help=("설치할 항목 (bun, node, playwright)"),
        metavar="ITEM",
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
        "command_name",
        choices=["install", "list", "config"],
        help="상세 정보를 볼 명령어",
    )

    subparsers.add_parser(
        "config",
        help="클로드 설정파일 표시",
        description="클로드 config.json 파일 상태를 보여줍니다.",
    )

    subparsers.add_parser(
        "mcp",
        help="클로드 MCP 서버 목록 표시",
        description="클로드 MCP 서버 목록을 표시합니다.",
    )

    return parser


def show_command_help(parser: argparse.ArgumentParser, command_name: str):
    """Show detailed help for a specific command."""
    if command_name == "install":
        print("\n[install 명령어 상세 정보]")
        print("-" * 40)
        print("사용법: uv run main.py install [PACKAGE...]")
        print("\n사용 가능한 인자:")
        print("  PACKAGE  설치할 패키지 이름 (선택사항)")
        print("\n설치 가능한 패키지:")
        print("  - bun   : Bun 자바스크립트 런타임")
        print("  - node  : Node.js 자바스크립트 런타임")
        print("\n예시:")
        print("  uv run main.py install bun      # bun만 설치")
        print("  uv run main.py install node bun  # node와 bun 설치")

    elif command_name == "list":
        print("\n[list 명령어 상세 정보]")
        print("-" * 40)
        print("사용법: uv run main.py list")
        print("\n설명: 설치 가능한 모든 패키지 목록을 표시합니다.")

    elif command_name == "config":
        print("\n[config 명령어 상세 정보]")
        print("-" * 40)
        print("사용법: uv run main.py config")
        print("\n설명: 클로드 config.json 파일 상태를 표시합니다.")


def list_packages(installer: PackageInstaller) -> None:
    """List available packages and their installation status."""
    print("\n사용 가능한 패키지:")
    print("-" * 20)
    for package in installer.get_available_packages():
        if installer.check_command_exists(package):
            print(f"- {package} (설치됨)")
        else:
            print(f"- {package}")

    print("\n사용 가능한 MCP:")
    print("-" * 20)
    for mcp in installer.get_available_mcps():
        if installer.check_command_exists(mcp):
            print(f"- {mcp} (설치됨)")
        else:
            print(f"- {mcp}")


def show_claude_config(installer: PackageInstaller) -> None:
    """Show the claude config."""
    config = installer.get_claude_config_json()
    for server in config:
        print(server)
    if config:
        print("\n클로드 설정파일 상태:")
        print("-" * 20)
        print(json.dumps(config, indent=2))
    else:
        print("클로드 설정파일이 존재하지 않습니다.")


def show_claude_mcp_servers(installer: PackageInstaller) -> None:
    """Show the claude MCP servers."""
    servers = installer.get_claude_config_json().get("mcpServers", [])
    if servers:
        print("\n클로드 MCP 서버 목록:")
        print("-" * 20)
        for server in servers:
            print(server)
    else:
        print("클로드 MCP 서버 목록이 존재하지 않습니다.")


def handle_install(installer: PackageInstaller, packages: List[str]) -> None:
    """Handle install command."""
    all_results = {}

    for item in packages:
        if item in installer.get_available_packages():
            results = installer.install_package(item)
            all_results.update(results)
        elif item in installer.get_available_mcps():
            results = installer.install_mcp(item)
            all_results.update(results)
        else:
            print(f"Unknown item: {item}")
            all_results[item] = False

    # Print summary
    print("\n설치 요약:")
    print("-" * 30)
    for name, success in all_results.items():
        status = "성공" if success else "실패"
        print(f"{name}: {status}")


def main() -> None:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    installer = PackageInstaller()

    if args.command == "show":
        show_command_help(parser, args.command_name)
        return

    if args.command == "list":
        list_packages(installer)
        return

    if args.command == "config":
        show_claude_config(installer)
        return

    if args.command == "mcp":
        show_claude_mcp_servers(installer)
        return

    if args.command == "install":
        handle_install(installer, args.packages)
        return

    # If no command is provided, show help
    parser.print_help()
