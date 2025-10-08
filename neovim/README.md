# Neovim 설정

## 목적
- LazyVim과 NvChad 두 가지 프로필을 병행 관리하면서, 로컬 `~/.config/nvim`과 레포 간 설정을 동기화합니다.
- 스크립트에 의존하지 않고 명령어 수준에서 백업/적용 절차를 명확히 합니다.

## 디렉터리 구조
- `lazyvim/`: LazyVim 기반 설정. `lua/config/*.lua`와 `lua/plugins/*.lua`에서 플러그인/옵션을 오버라이드합니다.
- `nvchad/`: NvChad 커스텀 설정. `lua/custom/` 트리를 중심으로 확장하며, VSCode 네오빔 확장 대응을 위해 `init.lua`를 제공합니다.

## 공통 요구 사항
- Neovim 설정 경로는 macOS/Linux 기준 `~/.config/nvim`으로 가정합니다.
- 동기화 전에는 반드시 기존 설정을 백업하세요. 예) `cp -R ~/.config/nvim ~/.config/nvim.backup.$(date +%Y%m%d%H%M)`.
- `rm -rf`는 파괴적이므로 실행 전에 대상 경로를 두 번 확인합니다.

## LazyVim 워크플로우
### 로컬 → 레포 백업
```sh
rm -rf neovim/lazyvim/lua
cp -R ~/.config/nvim/lua neovim/lazyvim/
```
- 레포에서 삭제 후 복사하므로 Git diff를 반드시 확인하세요.

### 레포 → 로컬 배포 (수동)
```sh
cp -R neovim/lazyvim/lua ~/.config/nvim/lua
```
- LazyVim 버전 업데이트 시 `lua/config/lazy.lua`에서 불러오는 LazyVim 플러그인 목록을 확인하세요.

## NvChad 워크플로우
### 로컬 → 레포 백업
```sh
rm -rf neovim/nvchad/lua/custom
cp -R ~/.config/nvim/lua/custom neovim/nvchad/lua/
```
- NvChad는 `lua/custom`만 관리하므로 다른 디렉터리는 삭제하지 않습니다.

### 레포 → 로컬 적용
```sh
rm -rf ~/.config/nvim/lua/custom
cp -R neovim/nvchad/lua/custom ~/.config/nvim/lua/
```
- `init.lua`는 VSCode 네오빔 확장 환경을 감지하여 `custom.vscode` 설정을 로드합니다.

## 운영 팁
- 두 프로필을 번갈아 사용한다면 `~/.config/nvim`을 symlink로 분리 (`~/.config/nvim-lazyvim`, `~/.config/nvim-nvchad`)한 뒤 필요한 시점에 교체하는 방식을 고려하세요.
- LazyVim과 NvChad 모두 플러그인 버전이 잦게 변하므로, 업데이트 후에는 `nvim --headless "+Lazy! sync" +qa` 혹은 `:NvChadUpdate` 등 각 프레임워크의 동기화 명령을 실행해 주세요.
- 레포에 새 파일을 추가했다면 상단 명령어로 복사했을 때 누락이 없는지 확인하고, 필요하면 디렉터리 단위를 조정하세요.
