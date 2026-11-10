param([string]$AndroidSdk)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$utf8 = New-Object System.Text.UTF8Encoding($false)

function New-LocalSecret {
    $bytes = New-Object byte[] 32
    $generator = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $generator.GetBytes($bytes) } finally { $generator.Dispose() }
    return ([BitConverter]::ToString($bytes)).Replace('-', '').ToLowerInvariant()
}

$envPath = Join-Path $projectRoot '.env'
if (-not (Test-Path -LiteralPath $envPath)) {
    $content = [IO.File]::ReadAllText((Join-Path $projectRoot '.env.example'))
    $content = $content.Replace('change-local-db-password', (New-LocalSecret))
    $content = $content.Replace('replace-with-a-random-local-secret', (New-LocalSecret))
    [IO.File]::WriteAllText($envPath, $content, $utf8)
    Write-Host '已生成根目录 .env，包含随机本地密码。'
} else { Write-Host '保留已有 .env。' }

$webEnv = Join-Path $projectRoot 'frontend/.env.local'
if (-not (Test-Path -LiteralPath $webEnv)) {
    Copy-Item -LiteralPath (Join-Path $projectRoot 'frontend/.env.example') -Destination $webEnv
    Write-Host '已生成 Web 本地配置。'
}

if (-not $AndroidSdk) {
    $candidates = @($env:ANDROID_HOME, $env:ANDROID_SDK_ROOT, (Join-Path $env:LOCALAPPDATA 'Android/Sdk'))
    $AndroidSdk = $candidates | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
}
$androidProperties = Join-Path $projectRoot 'android/local.properties'
if (-not (Test-Path -LiteralPath $androidProperties)) {
    if ($AndroidSdk -and (Test-Path -LiteralPath $AndroidSdk)) {
        $sdkPath = $AndroidSdk.Replace('\', '/')
        [IO.File]::WriteAllText($androidProperties, "sdk.dir=$sdkPath`nAPI_BASE_URL=http://10.0.2.2:8000/api/v1/`n", $utf8)
        Write-Host '已生成 Android SDK 与模拟器 API 配置。'
    } else {
        Write-Host '未找到 Android SDK；安装后用 -AndroidSdk 指定实际路径重新执行。'
    }
} else { Write-Host '保留已有 Android 本机配置。' }

Write-Host '本机配置不提交 Git；本脚本不会安装依赖或启动服务。'
