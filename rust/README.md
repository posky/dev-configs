# Rust 개발 환경

## 주요 파일
- `rustfmt.toml`: 프로젝트 전역 포맷터 설정. edition 2024, `imports_granularity = "Crate"` 등 고급 포맷 옵션을 활성화합니다.
- `Makefile.toml`: `cargo-make`용 태스크 정의(빌드, 클린, 클리피, 벤치 등).
- `log4rs.yaml`: log4rs 로깅 설정 예제 (회전 파일 포함).

## 레포 → 프로젝트 적용
```sh
cp rust/rustfmt.toml /path/to/project/rustfmt.toml
cp rust/Makefile.toml /path/to/project/Makefile.toml
mkdir -p /path/to/project/config
cp rust/log4rs.yaml /path/to/project/config/log4rs.yaml
```
- `cargo-make`를 사용할 경우 프로젝트 루트에 `Makefile.toml`이 존재해야 합니다.

## 프로젝트 → 레포 백업
```sh
cp /path/to/project/rustfmt.toml rust/rustfmt.toml
cp /path/to/project/Makefile.toml rust/Makefile.toml
cp /path/to/project/config/log4rs.yaml rust/log4rs.yaml
```

## 차이 비교
```sh
code --diff rust/rustfmt.toml /path/to/project/rustfmt.toml
code --diff rust/Makefile.toml /path/to/project/Makefile.toml
```

## 참고
- `rustfmt.toml`은 실험적 옵션을 포함하므로 사용하는 toolchain에서 `unstable_features = true`가 허용되는지 확인하세요.
- `Makefile.toml`은 `cargo install cargo-make` 후 `cargo make build`와 같은 명령으로 실행합니다.
