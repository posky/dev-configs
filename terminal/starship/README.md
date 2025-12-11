# Starship 프롬프트

## 주요 파일
- `starship.toml`: Starship 프롬프트 전체 구성. Catppuccin 팔레트, 우측 상태 표시, Git/언어별 아이콘 등을 정의합니다.

## 레포 → 로컬 적용
```sh
cp dev/tooling/starship/starship.toml ~/.config/starship.toml
```
- 기존 설정이 있다면 `cp ~/.config/starship.toml ~/.config/starship.toml.backup.$(date +%Y%m%d%H%M)`으로 백업 후 덮어쓰세요.

## 로컬 → 레포 백업
```sh
cp ~/.config/starship.toml dev/tooling/starship/starship.toml
```

## 차이 비교
```sh
code --diff dev/tooling/starship/starship.toml ~/.config/starship.toml
# 또는
vim -d dev/tooling/starship/starship.toml ~/.config/starship.toml
```
