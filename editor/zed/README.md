# Zed 에디터 설정

## 주요 파일
- `settings.json`: 전반적인 에디터 동작 및 테마 설정.
- `keymap.json`: 커스텀 키바인딩.
- `tasks.json`: 자주 사용하는 작업 정의 예시.

macOS 기준 설정 경로는 `~/Library/Application Support/Zed/User/` 입니다. Linux는 `~/.config/zed/User/`을 사용합니다.

## 레포 → 로컬 적용 (macOS)
```sh
DEST="$HOME/Library/Application Support/Zed/User"
mkdir -p "$DEST"
cp zed/settings.json "$DEST/settings.json"
cp zed/keymap.json "$DEST/keymap.json"
cp zed/tasks.json "$DEST/tasks.json"
```
- 기존 파일은 `cp` 명령으로 백업(`*.backup.$(date +%Y%m%d%H%M)`)한 뒤 덮어쓰세요.

## 로컬 → 레포 백업
```sh
cp "$HOME/Library/Application Support/Zed/User/settings.json" zed/settings.json
cp "$HOME/Library/Application Support/Zed/User/keymap.json" zed/keymap.json
cp "$HOME/Library/Application Support/Zed/User/tasks.json" zed/tasks.json
```

## 차이 비교
```sh
code --diff zed/settings.json "$HOME/Library/Application Support/Zed/User/settings.json"
code --diff zed/keymap.json "$HOME/Library/Application Support/Zed/User/keymap.json"
```

## 참고
- Linux 사용자는 위 경로에서 `Library/Application Support/Zed/User` 대신 `~/.config/zed/User`를 사용하면 됩니다.
- `tasks.json`은 선택 사항이므로 필요에 따라 제외하거나 프로젝트별 파일로 복사하세요.
