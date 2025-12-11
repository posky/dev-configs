# Windsurf 설정

## 주요 파일
- `settings.json`: Windsurf(User) 설정. 에디터 테마, 확장 동작 등을 정의합니다.

## 레포 → 로컬 적용 (macOS)
```sh
DEST="$HOME/Library/Application Support/Windsurf/User/settings.json"
mkdir -p "$(dirname "$DEST")"
cp windsurf/settings.json "$DEST"
```
- 기존 파일이 있다면 `cp "$DEST" "$DEST".backup.$(date +%Y%m%d%H%M)`으로 백업 후 덮어쓰세요.

## 로컬 → 레포 백업
```sh
cp "$HOME/Library/Application Support/Windsurf/User/settings.json" windsurf/settings.json
```

## 차이 비교
```sh
code --diff windsurf/settings.json "$HOME/Library/Application Support/Windsurf/User/settings.json"
```

## 참고
- Windsurf는 VS Code 기반이므로 설정 구조가 유사합니다. Sync 기능을 사용 중이라면 수동 복사 전에 동기화를 일시 정지하세요.
