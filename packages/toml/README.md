# TOML 개발 환경

## 주요 파일

- `taplo.toml`: Taplo formatter 설정입니다.

## 참고

- Taplo: https://taplo.tamasfe.dev/
- SchemaStore: https://www.schemastore.org/json/

## 레포 → 프로젝트 적용

```sh
cp packages/toml/taplo.toml /path/to/project/taplo.toml
```

## 차이 비교

```sh
code --diff packages/toml/taplo.toml /path/to/project/taplo.toml
```
