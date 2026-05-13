# PowerShell 설정

## 목적

- PowerShell profile 설정을 도구별 패키지 구조 안에서 관리합니다.

## 주요 파일

- `config/Microsoft.PowerShell_profile.ps1`: PowerShell 사용자 profile 파일입니다.

## 적용 전 확인

- Windows PowerShell과 PowerShell Core의 profile 경로가 다를 수 있으므로 적용 전 대상 경로를 확인하세요.
- 기존 profile이 있다면 백업 후 적용하세요.

## 레포 → 로컬 적용

```powershell
Copy-Item -Path "packages\powershell\config\Microsoft.PowerShell_profile.ps1" -Destination $PROFILE
```

## 차이 비교

```powershell
code --diff "packages\powershell\config\Microsoft.PowerShell_profile.ps1" $PROFILE
```
