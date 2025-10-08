# Prettier 설정

## 주요 파일
- `.prettierrc.json`: 프로젝트 전역에서 재사용할 Prettier 포맷팅 규칙을 정의합니다.

## 사용 방법
- 새로운 프로젝트를 생성할 때 레포의 설정을 루트에 복사하거나 심볼릭 링크를 만듭니다.
```sh
cp prettier/.prettierrc.json /path/to/project/.prettierrc.json
# 또는
ln -sf $(pwd)/prettier/.prettierrc.json /path/to/project/.prettierrc.json
```
- 전역 설정으로 사용하려면 macOS/Linux 기준 `~/.prettierrc` 또는 `~/.config/prettier/.prettierrc` 위치에 배치합니다.
```sh
cp prettier/.prettierrc.json ~/.prettierrc
```

## 로컬 → 레포 백업
```sh
cp /path/to/project/.prettierrc.json prettier/.prettierrc.json
```

## 차이 비교
```sh
code --diff prettier/.prettierrc.json /path/to/project/.prettierrc.json
```
