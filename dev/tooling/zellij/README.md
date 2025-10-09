# Zellij 설정

## 주요 파일
- `config.kdl`: Zellij 메인 설정 파일. 레이아웃, 키바인딩, UI 옵션 등을 정의합니다.
- `zellij`: 다중 세션이 있을 때 `sk`(skim)을 이용해 세션을 선택하는 zsh 래퍼 스크립트.

## 레포 → 로컬 적용
```sh
mkdir -p ~/.config/zellij
cp dev/tooling/zellij/config.kdl ~/.config/zellij/config.kdl
cp dev/tooling/zellij/zellij ~/.local/bin/zellij
chmod +x ~/.local/bin/zellij
```
- 기존 설정이 있다면 `cp ~/.config/zellij/config.kdl ~/.config/zellij/config.kdl.backup.$(date +%Y%m%d%H%M)`으로 백업하세요.
- 래퍼 스크립트를 사용하려면 PATH에 `~/.local/bin`이 포함되어 있고 `sk`가 설치되어 있어야 합니다.

## 로컬 → 레포 백업
```sh
cp ~/.config/zellij/config.kdl dev/tooling/zellij/config.kdl
cp ~/.local/bin/zellij dev/tooling/zellij/zellij
```

## 차이 비교
```sh
code --diff dev/tooling/zellij/config.kdl ~/.config/zellij/config.kdl
```

## 참고
- 공식 바이너리(`zellij attach`)와 혼동되지 않도록 래퍼 스크립트를 다른 이름(예: `zj`)으로 설치하는 것도 고려할 수 있습니다.
- 새 버전으로 업그레이드한 뒤에는 `zellij setup --check`로 설정이 최신 스키마와 호환되는지 확인하세요.
