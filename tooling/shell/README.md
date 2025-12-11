# Shell 환경

## 목적
- macOS/Linux의 zsh + Oh My Zsh 설정과 Starship 프롬프트 구성을 버전 관리합니다.
- PowerShell 프로필, zellij 스크립트 등 터미널 관련 보조 스크립트를 함께 보관합니다.

## 주요 파일
- `zsh/.zshrc`: Oh My Zsh 로딩, 플러그인( `git`, `rust`, `zsh-autosuggestions`, `zsh-autocomplete`, `zsh-syntax-highlighting` )과 Starship 초기화를 정의합니다.
- `zsh/upgrade.sh`: Oh My Zsh 커스텀 플러그인/테마 디렉터리에서 `git pull`을 수행하는 보조 스크립트.
- `bin/zellij`: 다중 세션이 있을 때 fzf 유사 선택기(`sk`)로 세션을 고릅니다.
- `powerdev/tooling/shell/Microsoft.PowerShell_profile.ps1`: Windows PowerShell에서 Oh My Posh 테마를 로드합니다.

## 동기화 방법
### zsh 설정 레포 → 로컬
```sh
cp dev/tooling/shell/zsh/.zshrc ~/.zshrc
```
- 기존 설정이 있다면 먼저 백업(`cp ~/.zshrc ~/.zshrc.backup`) 후 반영하세요.
- Starship, fnm, fastfetch 등 의존 바이너리가 설치되어 있어야 오류 없이 초기화됩니다.

### zsh 설정 로컬 → 레포
```sh
cp ~/.zshrc dev/tooling/shell/zsh/.zshrc
```

### 설정 비교
```sh
code --diff dev/tooling/shell/zsh/.zshrc ~/.zshrc  # VS Code
# 또는
vim -d dev/tooling/shell/zsh/.zshrc ~/.zshrc
```
- `code` 명령이 없을 경우 위 예시처럼 `vim -d`를 사용하면 됩니다.

## 참고
- PowerShell 환경을 사용하는 경우 `dev/tooling/shell/powerdev/tooling/shell/Microsoft.PowerShell_profile.ps1`을 `%UserProfile%\Documents\PowerShell\` 경로에 복사하면 됩니다.
- zellij 단축 스크립트(`dev/tooling/shell/bin/zellij`)는 `sk`가 설치되어 있다는 가정이며, 없으면 기본 attach로 대체하거나 수정이 필요합니다.
