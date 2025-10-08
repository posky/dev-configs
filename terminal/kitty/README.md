# Kitty 설정

## 주요 파일
- `kitty.conf`: `~/.config/kitty/kitty.conf`에 대응하는 메인 설정입니다. 키바인딩, 글꼴, 창 레이아웃 등의 모든 세부 설정을 포함합니다.

## 레포 → 로컬 적용
```sh
mkdir -p ~/.config/kitty
cp terminal/kitty/kitty.conf ~/.config/kitty/kitty.conf
```
- 기존 파일이 있다면 `cp ~/.config/kitty/kitty.conf ~/.config/kitty/kitty.conf.backup.$(date +%Y%m%d%H%M)`으로 백업 후 덮어쓰세요.

## 로컬 → 레포 백업
```sh
cp ~/.config/kitty/kitty.conf terminal/kitty/kitty.conf
```

## 차이 비교
```sh
code --diff terminal/kitty/kitty.conf ~/.config/kitty/kitty.conf
# 또는
vim -d terminal/kitty/kitty.conf ~/.config/kitty/kitty.conf
```
