# bat 설정

## 목적
- `bat` 명령행 뷰어에서 Catppuccin Mocha 테마와 기본 옵션을 일관되게 사용합니다.
- 개인화된 테마를 빠르게 재적용하거나 백업할 수 있도록 저장합니다.

## 주요 파일
- `config`: `bat` 실행 시 적용할 기본 옵션(테마 지정 등)을 포함합니다.
- `themes/Catppuccin Mocha.tmTheme`: Catppuccin 프로젝트에서 제공하는 다크 테마 원본 파일입니다.

## 동기화 방법
- 명령은 `bat/` 디렉터리에서 실행한다고 가정합니다.
1. 로컬에 테마를 배치합니다.
   ```sh
   mkdir -p ~/.config/bat/themes
   cp "$(pwd)/themes/Catppuccin Mocha.tmTheme" ~/.config/bat/themes/
   ```
2. 캐시를 재생성합니다.
   ```sh
   bat cache --build
   ```
3. 기본 설정을 적용합니다.
   ```sh
   ln -sf "$(pwd)/config" ~/.config/bat/config
   ```

## 참고
- 테마를 업데이트했다면 2단계를 다시 수행해 캐시를 갱신하세요.
- 별도 자동화 스크립트는 없으니 수동으로 동기화를 반복합니다.
