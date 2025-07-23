# go-stock 自动更新工具

这是一个自动更新工具，用于自动检查并更新 go-stock 应用程序。

## 功能
- 无需加速科学
- 自动检查 GitHub 上的最新版本
- 下载最新的安装程序
- 终止当前运行的 go-stock 进程
- 运行新的安装程序

## 使用方法

### 快速开始

1. 双击运行 `run_update.bat` 文件
2. 脚本将自动检查依赖项、下载最新版本并安装

### 手动运行

如果您已经安装了 Python 和所需的依赖项，也可以直接运行 Python 脚本：

```
python auto_update.py
```

## 系统要求

- Windows 操作系统
- Python 3.6 或更高版本
- 网络连接以访问 GitHub

## 文件说明

- `auto_update.py` - 主要的更新脚本
- `requirements.txt` - Python 依赖项列表
- `run_update.bat` - 批处理文件，用于安装依赖并运行脚本
- `update_log.txt` - 更新过程的日志文件（运行脚本后生成）

## 日志

更新过程的详细日志将保存在 `update_log.txt` 文件中，可用于排查问题。


2025-07-23 10:15:29,945 - INFO - === 开始自动更新过程 ===
2025-07-23 10:15:29,946 - INFO - 检查网络连接...
2025-07-23 10:15:30,430 - INFO - 网络连接正常
2025-07-23 10:15:30,431 - INFO - 正在检查最新版本...
2025-07-23 10:15:30,431 - INFO - 正在检查最新版本: https://bgithub.xyz/ArvinLovegood/go-stock/releases
2025-07-23 10:15:31,775 - INFO - 已保存GitHub页面内容到github_page.html用于调试
2025-07-23 10:15:31,983 - INFO - 未找到release-header，尝试其他选择器
2025-07-23 10:15:32,019 - INFO - 未找到.release，尝试查找任何版本标签
2025-07-23 10:15:32,044 - INFO - 找到最新版本: v2025.7.22.2-dev
2025-07-23 10:15:32,045 - INFO - 准备下载版本 v2025.7.22.2-dev
2025-07-23 10:15:32,045 - INFO - 开始下载安装程序...
2025-07-23 10:15:32,045 - INFO - 拼接下载链接: https://gh-proxy.com/https://github.com/ArvinLovegood/go-stock/releases/download/v2025.7.22.2-dev/go-stock-amd64-installer.exe
2025-07-23 10:15:32,046 - INFO - 开始下载安装程序到: E:\发布GITHUB\已经发布\go-stock_autoup\go-stock-amd64-installer.exe
2025-07-23 10:15:37,142 - INFO - 
下载完成: E:\发布GITHUB\已经发布\go-stock_autoup\go-stock-amd64-installer.exe
2025-07-23 10:15:37,144 - INFO - 安装程序下载成功: E:\发布GITHUB\已经发布\go-stock_autoup\go-stock-amd64-installer.exe
2025-07-23 10:15:37,144 - INFO - 正在终止当前运行的进程...
2025-07-23 10:15:37,144 - INFO - 尝试终止进程: go-stock.exe
2025-07-23 10:15:37,600 - INFO - 进程未运行: go-stock.exe
2025-07-23 10:15:37,601 - INFO - 等待进程完全终止...
2025-07-23 10:15:39,603 - INFO - 正在运行安装程序...
2025-07-23 10:15:39,603 - INFO - 开始运行安装程序: E:\发布GITHUB\已经发布\go-stock_autoup\go-stock-amd64-installer.exe
2025-07-23 10:15:39,604 - INFO - 尝试方法1: 使用subprocess.Popen直接运行
2025-07-23 10:15:39,615 - INFO - 安装程序已启动 (方法1)
2025-07-23 10:15:39,617 - INFO - 安装程序已启动
2025-07-23 10:15:39,617 - INFO - === 自动更新过程完成 ===


## 注意事项

- 脚本运行时会终止当前运行的 go-stock.exe 进程
- 需要管理员权限才能正确安装新版本
- 确保您的防火墙允许脚本访问 GitHub