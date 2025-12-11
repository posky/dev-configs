# Hammerspoon 설정

## 목적
- macOS에서 사용하는 Hammerspoon 자동화 설정과 키 리매핑 스크립트를 버전 관리합니다.
- `foundation_remapping` 모듈을 포함해 입력기 전환 및 Escape 키 보정을 일관되게 유지합니다.

## 주요 파일
- `.hammerspoon/init.lua`: Spoons 로드, 키 리매핑 등록, Escape 입력 시 영문 레이아웃 강제 전환을 담당합니다.
- `.hammerspoon/foundation_remapping.lua`: `hidutil` 기반 키 매핑 헬퍼 라이브러리입니다.

## 동기화 방법
### 레포 → 로컬 적용
1. 기존 설정을 백업합니다.
   ```sh
   cp -r ~/.hammerspoon ~/.hammerspoon.backup.$(date +%Y%m%d%H%M)
   ```
2. 레포 루트에서 다음을 실행합니다.
   ```sh
   rm -rf ~/.hammerspoon
   cp -r "$(pwd)/hammerspoon/.hammerspoon" ~/.hammerspoon
   ```
3. Hammerspoon을 재시작하거나 메뉴에서 `Reload Config`를 선택합니다.

### 로컬 → 레포 백업
```sh
rm -rf hammerspoon/.hammerspoon
cp -R ~/.hammerspoon hammerspoon/
```

## 참고
- `foundation_remapping.lua`는 외부 프로젝트에서 가져왔으므로 업데이트 시 upstream 변화를 확인하고, 변경 내역을 README에 기록하세요.
