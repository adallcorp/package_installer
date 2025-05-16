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

## 명령어 실행

실행 가능한 명령어
- list(사용 가능한 **명령어** 리스트)
- show(사용 가능한 **명령어**를 더욱 자세히 볼 수 있습니다.)
- install(패키지 **다운로드** 명령어)
- config(claude config 파일 확인)
- mcp(claude config에 설치된 서버 List)

> 모든 명령어 뒤에 "-h" or "--help"를 붙이면 상세하게 볼 수 있습니다.