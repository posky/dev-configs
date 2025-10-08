# Python 개발 환경

## 주요 파일
- `ruff.toml`: Ruff 린터/포매터 공통 설정.
- `logging/`: 예제 로깅 설정(`logging.yaml`)과 사용 방법 샘플(`example.py`).
- `settings.json`: VS Code에서 Python 파일 저장 시 Ruff/Black을 자동 실행하도록 하는 워크스페이스 설정.
- `tasks.json`: VS Code 작업 예시(예: jupytext 변환).

## 레포 → 프로젝트/로컬 적용
1. Ruff/Black 설정을 프로젝트 루트에 복사합니다.
   ```sh
   cp python/ruff.toml /path/to/project/ruff.toml
   ```
2. VS Code 워크스페이스에서 Python용 설정을 가져오려면 `.vscode` 폴더에 파일을 배치합니다.
   ```sh
   mkdir -p /path/to/project/.vscode
   cp python/settings.json /path/to/project/.vscode/settings.json
   cp python/tasks.json /path/to/project/.vscode/tasks.json
   ```
3. 로깅 예제는 참고용이므로 필요 시 프로젝트에 맞게 복사합니다.
   ```sh
   cp -R python/logging /path/to/project/tools/logging
   ```

## 프로젝트 → 레포 백업
```sh
cp /path/to/project/ruff.toml python/ruff.toml
cp /path/to/project/.vscode/settings.json python/settings.json
cp /path/to/project/.vscode/tasks.json python/tasks.json
# 로깅 설정을 수정했다면
cp -R /path/to/project/tools/logging python/
```

## 차이 비교
```sh
code --diff python/ruff.toml /path/to/project/ruff.toml
code --diff python/settings.json /path/to/project/.vscode/settings.json
```

## 참고
- `ruff.toml`은 Python 3.12 대상과 광범위한 플러그인 룰을 활성화합니다. 프로젝트 요구에 따라 `select` 목록을 조정하세요.
- VS Code 자동 정리(Black, Ruff)는 `settings.json`에 정의된 확장 프로그램이 설치되어 있을 때 정상 동작합니다.
