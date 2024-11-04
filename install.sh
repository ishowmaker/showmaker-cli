#!/bin/bash

set -e

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 检测系统和架构
OS="$(uname -s)"
ARCH="$(uname -m)"

# GitHub 仓库信息
REPO_OWNER="ishowmaker"
REPO_NAME="showmaker-cli"

echo -e "${GREEN}Installing ConnectDev CLI...${NC}"

# 获取最新版本
LATEST_VERSION=$(curl -s https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

# 根据系统选择下载文件
case "${OS}" in
    "Darwin")
        DOWNLOAD_FILE="connectdev-macos.tar.gz"
        ;;
    "Linux")
        DOWNLOAD_FILE="connectdev-linux.tar.gz"
        ;;
    *)
        echo -e "${RED}Unsupported operating system: ${OS}${NC}"
        exit 1
        ;;
esac

# 创建临时目录
TMP_DIR=$(mktemp -d)
cd "${TMP_DIR}"

# 下载文件
echo "Downloading ConnectDev CLI..."
DOWNLOAD_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/download/${LATEST_VERSION}/${DOWNLOAD_FILE}"
curl -LO "${DOWNLOAD_URL}"
curl -LO "${DOWNLOAD_URL}.sha256"

# 验证校验和
echo "Verifying download..."
if command -v sha256sum > /dev/null; then
    sha256sum -c "${DOWNLOAD_FILE}.sha256"
elif command -v shasum > /dev/null; then
    shasum -a 256 -c "${DOWNLOAD_FILE}.sha256"
else
    echo -e "${RED}Neither sha256sum nor shasum command found${NC}"
    exit 1
fi

# 安装
echo "Installing..."
tar xzf "${DOWNLOAD_FILE}"
sudo mkdir -p /usr/local/bin
sudo mv connectdev /usr/local/bin/
sudo chmod +x /usr/local/bin/connectdev

# 清理
cd - > /dev/null
rm -rf "${TMP_DIR}"

# 验证安装
if command -v connectdev > /dev/null; then
    echo -e "${GREEN}ConnectDev CLI has been installed successfully!${NC}"
    echo "Version: $(connectdev --version)"
    echo "Run 'connectdev --help' to get started."
else
    echo -e "${RED}Installation failed${NC}"
    exit 1
fi 