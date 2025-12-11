# Git 설정

## 목적
- 컨벤션을 맞춘 커밋 메시지 템플릿과 기본 Git 옵션을 일관되게 관리합니다.
- 개인 환경에서 사용하는 글로벌 설정을 백업할 수 있는 진입점을 제공합니다.

## 주요 파일
- `.gitconfig`: 기본 브랜치, diff 알고리즘, fetch 옵션 등 전역 권장 설정을 담고 있습니다.
- `.gitmessage.txt`: Conventional Commits 형식에 맞춘 메시지 템플릿입니다.

## 적용 방법 (레포 → 로컬)
1. 템플릿과 설정 파일을 홈 디렉터리로 배치합니다.
   ```sh
   cp git/.gitconfig ~/.gitconfig           # 기존 설정과 병합이 필요하면 적절히 조정
   cp git/.gitmessage.txt ~/.gitmessage.txt
   ```
2. Git 전역 설정에 템플릿을 등록합니다.
   ```sh
   git config --global commit.template ~/.gitmessage.txt
   ```
3. 다른 레포에서도 동일한 설정을 공유하려면 `includeIf` 규칙을 활용해도 좋습니다.

## 백업 방법 (로컬 → 레포)
```sh
cp ~/.gitmessage.txt git/
```
필요하다면 `.gitconfig`도 동일한 방식으로 복사한 뒤 변경분을 검토하세요.

## 참고
- `.gitconfig`는 바로 덮어쓰지 말고 기존 환경과 비교(diff) 후 필요한 항목만 병합하는 것을 권장합니다.

## FAQ

### 여러 환경에서 `.gitconfig`를 나누고 싶어요.
1. 공통 설정을 `~/.gitconfig`에 두고, 머신별 파일을 예를 들어 `~/.gitconfig-macos`, `~/.gitconfig-work`처럼 분리합니다.
2. `~/.gitconfig` 하단에 `includeIf` 규칙을 추가합니다.
   ```ini
   [includeIf "gitdir:~/work/"]
       path = .gitconfig-work
   [includeIf "hasconfig:remote.origin.url:github.com/company/"]
       path = .gitconfig-company
   ```
   - 특정 디렉터리나 원격 주소에 따라 다른 설정이 자동으로 병합됩니다.
3. 새 규칙을 추가한 뒤 `git config --global --edit`로 문법 오류가 없는지 확인하세요.

### Windows PowerShell에서 커밋 템플릿을 설정하려면?
PowerShell을 관리자 권한 없이 실행해도 됩니다.
```powershell
git config --global commit.template "$env:USERPROFILE\\.gitmessage.txt"
```
- 파일을 복사할 때는 `Copy-Item git\\.gitmessage.txt "$env:USERPROFILE\\.gitmessage.txt"`를 사용합니다.
- WSL 환경과 공유하려면 `C:\Users\<name>\.gitconfig`와 `~/.gitconfig`가 서로 충돌하지 않도록 includeIf 규칙을 활용하세요.
