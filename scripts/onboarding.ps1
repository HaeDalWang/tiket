#!/usr/bin/env pwsh
#
# onboarding.ps1 — Windows 온보딩. macOS / Linux 는 onboarding.sh 를 쓴다.
#
# 셸 프로필을 건드리지 않는다. 자격증명은 ~/.config/saltware/*.conf 에 저장하고
# 저장소 스크립트가 그 파일을 직접 읽는다. onboarding.sh 와 같은 경로 규약을 쓰므로
# 같은 사람이 두 OS 를 오가도 설정 위치가 같다.
#
# 사용:
#   pwsh -File scripts/onboarding.ps1           대화형
#   pwsh -File scripts/onboarding.ps1 -Check    확인만 (입력 없음)

param([switch]$Check)

$ErrorActionPreference = "Continue"

# STEPS-PARITY-START
$StepNames = @(
  "required-tools"
  "push-guard"
  "zendesk-credentials"
  "workspace-validation"
)
# STEPS-PARITY-END

$Root = Split-Path (Split-Path $MyInvocation.MyCommand.Path -Parent) -Parent
$UserHome = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
$ConfDir = Join-Path $UserHome ".config/saltware"
$ZendeskConf = Join-Path $ConfDir "zendesk.conf"

$script:FailCount = 0
function Write-Ok   { param([string]$m) Write-Host "  OK    $m" -ForegroundColor Green }
function Write-Bad  { param([string]$m) Write-Host "  FAIL  $m" -ForegroundColor Red; $script:FailCount++ }
function Write-Skip { param([string]$m) Write-Host "  건너뜀 $m" -ForegroundColor Yellow }
function Write-Step { param([string]$n, [string]$m) Write-Host "`n[$n] $m" }

# ── 1. required-tools ────────────────────────────────────────────────────────
Write-Step "1/4" "필수 도구"
foreach ($bin in @("git", "python3", "curl", "jq")) {
    $found = Get-Command $bin -ErrorAction SilentlyContinue
    # Windows 에서 python3 가 없고 python 만 있는 경우가 흔하다.
    if (-not $found -and $bin -eq "python3") {
        $found = Get-Command "python" -ErrorAction SilentlyContinue
        if ($found) { Write-Ok "python (python3 대신)"; continue }
    }
    if ($found) { Write-Ok $bin }
    else        { Write-Bad "$bin 없음 — winget install $bin 또는 scoop install $bin" }
}

# ── 2. push-guard ────────────────────────────────────────────────────────────
Write-Step "2/4" "push guard"
$currentHooks = (git -C $Root config --get core.hooksPath 2>$null)
if ($currentHooks -eq ".githooks") {
    Write-Ok "core.hooksPath = .githooks"
} elseif ($Check) {
    Write-Bad "core.hooksPath 미설정 — 해결: git config core.hooksPath .githooks"
} else {
    git -C $Root config core.hooksPath .githooks 2>$null
    if ($LASTEXITCODE -eq 0) { Write-Ok "core.hooksPath 를 .githooks 로 설정했다" }
    else                     { Write-Bad "core.hooksPath 설정 실패" }
}
if (Test-Path (Join-Path $Root ".githooks/pre-push")) {
    Write-Ok "pre-push hook 존재"
} else {
    Write-Bad "pre-push hook 이 없다"
}

# ── 3. zendesk-credentials ───────────────────────────────────────────────────
Write-Step "3/4" "Zendesk 자격증명"
function Test-ConfKey {
    param([string]$Key)
    if (-not (Test-Path $ZendeskConf)) { return $false }
    return [bool](Get-Content $ZendeskConf | Where-Object { $_ -match "^$Key=" })
}

if ((Test-ConfKey "ZENDESK_SUBDOMAIN") -and (Test-ConfKey "ZENDESK_EMAIL") -and (Test-ConfKey "ZENDESK_API_TOKEN")) {
    Write-Ok "설정됨: ~/.config/saltware/zendesk.conf (값은 출력하지 않는다)"
} elseif ($Check) {
    Write-Bad "미설정 — 해결: pwsh -File scripts/onboarding.ps1"
} else {
    Write-Host ""
    Write-Host "  Zendesk 토큰을 등록한다. 티켓을 번호로 가져오려면 필요하다."
    Write-Host "  토큰 발급: Zendesk 관리센터 → 앱 및 통합 → API → Zendesk API → 토큰 추가"
    Write-Host ""

    # 빈 입력은 건너뛰기가 아니다. 건너뛰려면 skip 을 직접 입력해야 한다 —
    # 필수 단계에 쉬운 탈출구를 두면 대부분 그걸 누르고, 나중에 안 된다고 되돌아온다.
    function Read-Required {
        param([string]$Label)
        for ($i = 0; $i -lt 3; $i++) {
            $v = Read-Host "  $Label"
            if ($v -eq "skip") { return $null }
            if (-not [string]::IsNullOrWhiteSpace($v)) { return $v }
            Write-Host "    값이 필요하다. 지금 등록할 수 없으면 skip 을 입력한다."
        }
        return $null
    }

    $zdSub = Read-Required "Zendesk 서브도메인 (예: saltware)"
    if (-not $zdSub) {
        Write-Skip "토큰 등록을 건너뛰었다. 티켓 조회는 아직 안 된다."
        Write-Skip "나중에 다시 실행: pwsh -File scripts/onboarding.ps1"
    } else {
        # 'Zendesk 로그인 이메일'로 적는다. 이 저장소에서 '에이전트'는 AI 도구를 뜻하므로
        # Zendesk 쪽 agent(상담원)와 겹쳐 읽는 사람이 자기 이메일인지 헷갈린다.
        $zdEmail = Read-Required "Zendesk 로그인 이메일 (본인 계정)"
        if (-not $zdEmail) {
            Write-Skip "토큰 등록을 건너뛰었다. 나중에 다시 실행: pwsh -File scripts/onboarding.ps1"
        } else {
            $zdTokenSecure = Read-Host "  API 토큰 (화면에 안 보인다)" -AsSecureString
            $zdToken = [System.Net.NetworkCredential]::new("", $zdTokenSecure).Password

            if ([string]::IsNullOrWhiteSpace($zdToken)) {
                Write-Bad "토큰이 비었다. 저장하지 않았다. 다시 실행: pwsh -File scripts/onboarding.ps1"
            } else {
                $zdHost = if ($zdSub -like "*.zendesk.com") { $zdSub } else { "$zdSub.zendesk.com" }
                Write-Host "  확인 중: https://$zdHost ..."
                $pair = "$zdEmail/token:$zdToken"
                $basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
                $code = 0
                try {
                    $resp = Invoke-WebRequest -Uri "https://$zdHost/api/v2/users/me.json" `
                        -Headers @{ Authorization = "Basic $basic" } `
                        -TimeoutSec 20 -UseBasicParsing -ErrorAction Stop
                    $code = $resp.StatusCode
                } catch {
                    if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode }
                }

                if ($code -eq 200) {
                    $who = "?"
                    try { $u = ($resp.Content | ConvertFrom-Json).user; $who = "$($u.name) ($($u.role))" } catch {}
                    New-Item -ItemType Directory -Force -Path $ConfDir | Out-Null
                    $lines = @(
                        "# tiket Zendesk credentials. 이 파일 내용을 채팅·이슈·PR 에 붙여넣지 않는다."
                        "# 다시 설정하려면: pwsh -File scripts/onboarding.ps1"
                        "ZENDESK_SUBDOMAIN=$zdSub"
                        "ZENDESK_EMAIL=$zdEmail"
                        "ZENDESK_API_TOKEN=$zdToken"
                    )
                    Set-Content -Path $ZendeskConf -Value $lines -Encoding UTF8
                    # NTFS 에는 chmod 가 없다. 상속을 끊고 현재 사용자만 남긴다.
                    try {
                        $acl = Get-Acl $ZendeskConf
                        $acl.SetAccessRuleProtection($true, $false)
                        $acl.Access | ForEach-Object { $acl.RemoveAccessRule($_) | Out-Null }
                        $rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
                            "$env:USERDOMAIN\$env:USERNAME", "FullControl", "Allow")
                        $acl.SetAccessRule($rule)
                        Set-Acl -Path $ZendeskConf -AclObject $acl
                    } catch {
                        Write-Skip "파일 권한을 좁히지 못했다. 사용자만 읽도록 직접 확인한다: $ZendeskConf"
                    }
                    Write-Ok "인증 성공 ($who) — ~/.config/saltware/zendesk.conf 에 저장"
                } elseif ($code -eq 401 -or $code -eq 403) {
                    Write-Bad "인증 거부 (HTTP $code). 이메일 또는 토큰이 맞지 않는다. 저장하지 않았다."
                } else {
                    Write-Bad "Zendesk 응답 HTTP $code. 서브도메인과 네트워크를 확인한다. 저장하지 않았다."
                }
            }
        }
    }
}

# ── 4. workspace-validation ──────────────────────────────────────────────────
Write-Step "4/4" "저장소 검증"
$py = (Get-Command python3 -ErrorAction SilentlyContinue) ?? (Get-Command python -ErrorAction SilentlyContinue)
if ($py) {
    Push-Location $Root
    $out = & $py.Source scripts/validate_workspace.py 2>&1
    $rc = $LASTEXITCODE
    Pop-Location
    if ($rc -eq 0) { Write-Ok ($out | Select-Object -First 1) }
    else           { Write-Bad (($out | Select-Object -First 3) -join " / ") }
} else {
    Write-Bad "python 이 없어 검증을 건너뛰었다"
}

# ── 결과 ─────────────────────────────────────────────────────────────────────
Write-Host ""
if ($script:FailCount -eq 0) {
    Write-Host "온보딩 완료. 다음: ONBOARDING.md 의 `"연습해보기`"" -ForegroundColor Green
    exit 0
}
Write-Host "$($script:FailCount)개 항목이 남았다. 위 FAIL 줄의 해결 방법을 따른 뒤 다시 실행한다." -ForegroundColor Red
exit 1
