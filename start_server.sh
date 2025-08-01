#!/bin/bash

# 输出彩色文本的函数
print_green() {
    echo -e "\033[0;32m$1\033[0m"
}

print_blue() {
    echo -e "\033[0;34m$1\033[0m"
}

print_yellow() {
    echo -e "\033[0;33m$1\033[0m"
}

# 显示欢迎信息
print_blue "====================================="
print_blue "   Flask 消息管理系统 - 服务器启动   "
print_blue "====================================="
echo ""

# 检查是否存在虚拟环境
if [ -d "venv" ]; then
    print_green "检测到虚拟环境，正在激活..."
    source venv/bin/activate || source venv/Scripts/activate
else
    print_yellow "未检测到虚拟环境，将在全局环境中运行..."
fi

# 安装必要的依赖
print_green "正在检查并安装必要的依赖..."
pip install flask

# 检查数据库文件是否存在
if [ ! -f "messages.db" ]; then
    print_yellow "数据库文件不存在，将在应用启动时自动创建..."
fi

# 启动Flask应用
print_green "正在启动Flask应用服务器..."
echo ""
python app.py

# 如果应用意外退出，保持终端窗口打开
read -p "按任意键退出..."
