# Zsh 설정

## 목적

- Zsh shell 설정과 관련 유지보수 스크립트를 도구별 패키지 구조 안에서 관리합니다.

## 주요 파일

- `config/.zshrc`: Zsh 사용자 설정 파일입니다.
- `scripts/upgrade.sh`: Zsh 관련 업데이트 또는 유지보수 스크립트입니다.

## 적용 전 확인

- 기존 `~/.zshrc`가 있다면 백업 후 적용하세요.
- `upgrade.sh`는 실행 전 shebang, 실행 권한, 상대 경로 의존성을 확인해야 합니다.

## 레포 → 로컬 적용

```sh
cp packages/zsh/config/.zshrc ~/.zshrc
```

## 차이 비교

```sh
code --diff packages/zsh/config/.zshrc ~/.zshrc
```
