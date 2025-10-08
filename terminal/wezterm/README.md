# WezTerm 설정

## 주요 파일
- `.wezterm.lua`: 홈 디렉터리 루트에 위치하는 WezTerm 설정 파일입니다. 작업 공간, 상태 표시줄, 테마 등을 정의합니다.

## 레포 → 로컬 적용
```sh
cp terminal/wezterm/.wezterm.lua ~/.wezterm.lua
```
- 기존 파일이 있다면 `cp ~/.wezterm.lua ~/.wezterm.lua.backup.$(date +%Y%m%d%H%M)`으로 백업 후 덮어쓰세요.

## 로컬 → 레포 백업
```sh
cp ~/.wezterm.lua terminal/wezterm/.wezterm.lua
```

## 차이 비교
```sh
code --diff terminal/wezterm/.wezterm.lua ~/.wezterm.lua
# 또는
vim -d terminal/wezterm/.wezterm.lua ~/.wezterm.lua
```
