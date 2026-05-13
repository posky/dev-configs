# Shared Scripts

## 목적

- 특정 도구 하나의 소유로 보기 어려운 공용 유지보수 스크립트를 관리합니다.

## 주요 파일

- `scripts/update`: macOS 개발 환경의 여러 도구 업데이트를 순차 실행하는 공용 유지보수 스크립트입니다.

## 소유권 기준

- 특정 도구의 설정 또는 실행 방식과 강하게 결합된 스크립트는 해당 도구 패키지의 `scripts/`에 둡니다.
- 여러 도구나 저장소 전체 유지보수에 쓰이는 스크립트만 이 패키지에 둡니다.

## 적용 전 확인

- 각 스크립트는 실행 전 shebang, 실행 권한, PATH 전제, 상대 경로 의존성을 확인해야 합니다.

## 적용 예시

```sh
cp packages/shared-scripts/scripts/update ~/.local/bin/update
chmod +x ~/.local/bin/update
```
