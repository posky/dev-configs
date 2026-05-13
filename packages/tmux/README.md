# tmux 설정

## 목적

- tmux 터미널 멀티플렉서 설정을 도구별 패키지 구조 안에서 관리합니다.

## 주요 파일

- `config/.tmux.conf`: 홈 디렉터리의 `~/.tmux.conf`에 대응하는 tmux 설정 파일입니다.

## 적용 전 확인

- 기존 `~/.tmux.conf`가 있다면 백업 후 적용하세요.
- 실제 적용 명령은 구조 이동 완료 후 최종 경로 기준으로 검증합니다.

## 레포 → 로컬 적용

```sh
cp packages/tmux/config/.tmux.conf ~/.tmux.conf
```

## 차이 비교

```sh
code --diff packages/tmux/config/.tmux.conf ~/.tmux.conf
```
