#!/bin/bash

set -e

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 仓库信息
REPO_OWNER="ishowmaker"
REPO_NAME="showmaker-cli"

# 检测系统和架构
OS="$(uname -s)"
ARCH="$(uname -m)"

echo -e "${GREEN}Detecting system: ${OS} (${ARCH})${NC}"

# 根据系统和架构选择下载文件
case "${OS}" in
    "Darwin")
        # macOS 统一使用 arm64 版本
        DOWNLOAD_FILE="connectdev-macos-arm64.tar.gz"
        ;;
    "Linux")
        if [ "${ARCH}" = "x86_64" ]; then
            DOWNLOAD_FILE="connectdev-linux-x86_64.tar.gz"
        else
            echo -e "${RED}Unsupported architecture: ${ARCH}${NC}"
            exit 1
        fi
        ;;
    *)
        echo -e "${RED}Unsupported operating system: ${OS}${NC}"
        exit 1
        ;;
esac

# 获取最新版本
echo "Fetching latest version..."
LATEST_VERSION=$(curl -s https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "${LATEST_VERSION}" ]; then
    echo -e "${RED}Failed to get latest version${NC}"
    exit 1
fi

# 创建临时目录
TMP_DIR=$(mktemp -d)
cd "${TMP_DIR}" || exit 1

# 下载文件
echo -e "${GREEN}Downloading version ${LATEST_VERSION}...${NC}"
DOWNLOAD_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/download/${LATEST_VERSION}/${DOWNLOAD_FILE}"

if ! curl -LO "${DOWNLOAD_URL}"; then
    echo -e "${RED}Download failed${NC}"
    exit 1
fi

if ! curl -LO "${DOWNLOAD_URL}.sha256"; then
    echo -e "${RED}Checksum download failed${NC}"
    exit 1
fi

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
cd - > /dev/null || exit 1
rm -rf "${TMP_DIR}"

# 验证安装
if command -v connectdev > /dev/null; then
    echo -e "${GREEN}ConnectDev CLI has been installed successfully!${NC}"
    VERSION_OUTPUT=$(connectdev --version)
    echo "Version: ${VERSION_OUTPUT}"
    echo "Run 'connectdev --help' to get started."
else
    echo -e "${RED}Installation failed${NC}"
    exit 1
fi 