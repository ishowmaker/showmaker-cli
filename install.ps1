# 检查是否以管理员权限运行
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "Please run this script as Administrator"
    exit 1
}

# 设置 TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# 仓库信息
$RepoOwner = "ishowmaker"
$RepoName = "showmaker-cli"

Write-Host "Installing ConnectDev CLI..." -ForegroundColor Green

# 获取最新版本
$LatestRelease = Invoke-RestMethod -Uri "https://api.github.com/repos/$RepoOwner/$RepoName/releases/latest"
$Version = $LatestRelease.tag_name

# 下载地址
$DownloadFile = "connectdev-windows.exe.zip"
$DownloadUrl = "https://github.com/$RepoOwner/$RepoName/releases/download/$Version/$DownloadFile"

# 创建临时目录
$TempDir = New-Item -ItemType Directory -Path "$env:TEMP\connectdev-install" -Force
$OutFile = Join-Path $TempDir $DownloadFile

# 下载文件
Write-Host "Downloading ConnectDev CLI..."
Invoke-WebRequest -Uri $DownloadUrl -OutFile $OutFile

# 解压文件
Write-Host "Extracting..."
Expand-Archive -Path $OutFile -DestinationPath $TempDir -Force

# 安装目录
$InstallDir = "$env:ProgramFiles\ConnectDev"
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null

# 移动文件
Move-Item -Path "$TempDir\connectdev.exe" -Destination "$InstallDir\connectdev.exe" -Force

# 添加到 PATH
$EnvPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)
if ($EnvPath -notlike "*$InstallDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$EnvPath;$InstallDir", [EnvironmentVariableTarget]::Machine)
}

# 清理
Remove-Item -Path $TempDir -Recurse -Force

# 验证安装
try {
    $Version = & "$InstallDir\connectdev.exe" --version
    Write-Host "ConnectDev CLI has been installed successfully!" -ForegroundColor Green
    Write-Host "Version: $Version"
    Write-Host "Run 'connectdev --help' to get started."
} catch {
    Write-Error "Installation failed: $_"
    exit 1
} 