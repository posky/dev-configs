# VS Code 키바인딩

## 주요 파일
- `macos/keybindings.json`: macOS 환경의 사용자 키바인딩.
- `windows/keybindings.json`: Windows 환경의 사용자 키바인딩.

## 레포 → 로컬 적용
### macOS
```sh
DEST="$HOME/Library/Application Support/Code/User/keybindings.json"
cp vscode/macos/keybindings.json "$DEST"
```
- 덮어쓰기 전에는 `cp "$DEST" "$DEST".backup.$(date +%Y%m%d%H%M)`으로 백업하세요.

### Windows
PowerShell에서 실행:
```powershell
$dest = "$env:APPDATA\Code\User\keybindings.json"
Copy-Item -Path "vscode\windows\keybindings.json" -Destination $dest
```
- 기존 파일은 `Copy-Item $dest "$dest.bak-$(Get-Date -Format yyyyMMddHHmm)"`로 백업합니다.

## 로컬 → 레포 백업
```sh
cp "$HOME/Library/Application Support/Code/User/keybindings.json" vscode/macos/keybindings.json
```
PowerShell:
```powershell
Copy-Item "$env:APPDATA\Code\User\keybindings.json" "vscode\windows\keybindings.json"
```

## 차이 비교
```sh
code --diff vscode/macos/keybindings.json "$HOME/Library/Application Support/Code/User/keybindings.json"
# Windows
code --diff vscode\windows\keybindings.json "$env:APPDATA\Code\User\keybindings.json"
```

## 참고
- VS Code Insiders를 사용하는 경우 경로가 `Code - Insiders`로 달라질 수 있습니다.
- 설정 동기화(Sync) 기능을 사용한다면 중복 적용을 피하기 위해 Sync를 잠시 끄고 수동 복사 후 다시 켜는 것이 안전합니다.
