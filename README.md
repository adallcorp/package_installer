## uv install

**windows**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macos**

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## package extract to execute file
pyinstaller --onefile --name package_installer package_installer.py