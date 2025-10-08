# Ghostty 설정

## 주요 파일
- `config`: `~/.config/ghostty/config`에 대응하는 메인 설정 파일입니다. Catppuccin 테마, 투명도, 폰트 등의 옵션을 정의합니다.

## 레포 → 로컬 적용
```sh
mkdir -p ~/.config/ghostty
cp terminal/ghostty/config ~/.config/ghostty/config
```
- 기존 파일이 있다면 `cp ~/.config/ghostty/config ~/.config/ghostty/config.backup.$(date +%Y%m%d%H%M)`으로 백업 후 덮어쓰세요.

## 로컬 → 레포 백업
```sh
cp ~/.config/ghostty/config terminal/ghostty/config
```

## 차이 비교
```sh
code --diff terminal/ghostty/config ~/.config/ghostty/config  # VS Code
# 또는
vim -d terminal/ghostty/config ~/.config/ghostty/config
```
