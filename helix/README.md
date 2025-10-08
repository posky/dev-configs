# Helix 설정

## 주요 파일
- `config.toml`: Helix 기본 옵션, 상태줄 구성, 테마 등을 정의합니다.
- `languages.toml`: 언어별 LSP/포맷터 설정을 커스터마이즈합니다.

## 레포 → 로컬 적용
```sh
mkdir -p ~/.config/helix
cp helix/config.toml ~/.config/helix/config.toml
cp helix/languages.toml ~/.config/helix/languages.toml
```
- 덮어쓰기 전에는 `cp -R ~/.config/helix ~/.config/helix.backup.$(date +%Y%m%d%H%M)`으로 백업하세요.

## 로컬 → 레포 백업
```sh
cp ~/.config/helix/config.toml helix/config.toml
cp ~/.config/helix/languages.toml helix/languages.toml
```

## 차이 비교
```sh
code --diff helix/config.toml ~/.config/helix/config.toml
code --diff helix/languages.toml ~/.config/helix/languages.toml
# 또는
vim -d helix/config.toml ~/.config/helix/config.toml
vim -d helix/languages.toml ~/.config/helix/languages.toml
```
