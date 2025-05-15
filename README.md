# 에이달 mcp servers

## uv 설치

> 설치에 앞서 먼저 **uv**를 설치해야 함.
> 아래 각각 windows, Mac OS 설치 방법이 있음.
> 터미널 창을 열고 아래 코드를 복사하여 붙여 넣으면 됨.

**windows**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macos**

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 패키지 실행

실행 가능한 명령어
- --help
- list(사용 가능한 **명령어** 리스트)
- install(패키지 **다운로드** 명령어)


```python
uv main.py --help
```