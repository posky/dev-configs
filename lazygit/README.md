# Lazygit 설정

## 목적
- Lazygit UI에서 Conventional Commits를 빠르게 작성하고, 자주 쓰는 유지보수 명령을 단축키로 노출합니다.
- macOS와 Linux 환경에서 설정 파일을 손쉽게 동기화합니다.

## 주요 파일
- `config.yml`: Lazygit 메인 설정 파일. `Ctrl+V`로 커밋 템플릿 프롬프트를 띄우고, `Ctrl+P`로 리모트 정리를 실행합니다.

## 동기화 방법
1. 레포 → 로컬 적용
   ```sh
   DEST="$(lazygit -cd)/config.yml"
   cp lazygit/config.yml "$DEST"
   ```
2. 로컬 → 레포 백업
   ```sh
   cp "$(lazygit -cd)/config.yml" lazygit/
   ```
3. 설정 비교
   ```sh
   LOCAL="$(lazygit -cd)/config.yml"
   code --diff lazygit/config.yml "$LOCAL"  # VS Code
   # 또는
   vim -d lazygit/config.yml "$LOCAL"
   ```

## 참고
- 커밋 템플릿 프롬프트는 `git/.gitmessage.txt` 구조와 동일하게 유지해야 UI가 일치합니다.
- 위 명령을 사용하려면 `lazygit` 명령어가 PATH에 있어야 합니다.
