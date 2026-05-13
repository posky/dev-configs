# Dev Configs

개인 개발 환경 설정을 도구별 패키지 구조로 관리하는 저장소입니다.

## Structure

```text
packages/<tool>/
  README.md
  config/
  themes/
  examples/
  scripts/
  docs/
```

## Package Rules

- 설정의 기본 소유 단위는 도메인이 아니라 도구/런타임/설정 소유자입니다.
- 각 패키지의 `README.md`는 주요 파일, 적용 방법, 백업/비교 방법을 설명합니다.
- 특정 도구 전용 스크립트는 해당 패키지의 `scripts/`에 둡니다.
- 여러 도구에 걸친 공용 스크립트는 `packages/shared-scripts/`에 둡니다.
- 여러 도구에서 참고 가능한 테마 문서는 `packages/shared-themes/`에 둡니다.
- `.DS_Store` 같은 로컬 산출물은 설정 패키지로 취급하지 않습니다.

## Current Packages

- `packages/neovim/`, `packages/vscode/`, `packages/windsurf/`, `packages/zed/`
- `packages/ghostty/`, `packages/kitty/`, `packages/wezterm/`, `packages/tmux/`, `packages/zellij/`, `packages/starship/`, `packages/zsh/`, `packages/powershell/`
- `packages/bat/`, `packages/git/`, `packages/hammerspoon/`, `packages/lazygit/`, `packages/prettier/`
- `packages/python/`, `packages/rust/`, `packages/toml/`
- `packages/shared-scripts/`, `packages/shared-themes/`

기존 최상위 디렉터리(`editor/`, `terminal/`, `tooling/`, `languages/`)는 `.DS_Store` 삭제 제외 방침 때문에 일시적으로 남아 있을 수 있습니다.

## Change Safety

- 기존 로컬 설정을 덮어쓰기 전에 각 패키지 README의 백업 안내를 확인하세요.
- 구조 이동이나 경로 변경 후에는 README의 `cp`, `ln -sf`, `code --diff`, `vim -d` 예시가 실제 파일 위치와 일치하는지 확인하세요.
- 자동 설치 도구는 아직 도입하지 않았으며, 현재는 수동 적용 절차를 기준으로 관리합니다.
