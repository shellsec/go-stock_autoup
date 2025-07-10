#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自动更新脚本 - 用于自动更新go-stock应用程序
功能：
1. 访问GitHub发布页面检查最新版本
2. 下载最新的安装程序
3. 终止当前运行的go-stock进程
4. 运行新的安装程序
"""

import os
import sys
import re
import time
import subprocess
import requests
from bs4 import BeautifulSoup
import logging

# 配置日志 - 使用UTF-8编码
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("update_log.txt", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置
GITHUB_RELEASES_URL = "https://github.com/ArvinLovegood/go-stock/releases"
INSTALLER_PATTERN = r"go-stock-amd64-installer\.exe"
PROCESS_NAME = "go-stock.exe"
DOWNLOAD_DIR = os.path.dirname(os.path.abspath(__file__))

# 确保下载目录存在
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
    logger.info(f"创建下载目录: {DOWNLOAD_DIR}")


def check_latest_version():
    """
    检查GitHub上的最新版本
    返回: 版本号
    """
    try:
        logger.info(f"正在检查最新版本: {GITHUB_RELEASES_URL}")
        
        # 添加User-Agent头，模拟浏览器请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(GITHUB_RELEASES_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 保存HTML内容用于调试
        with open("github_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        logger.info("已保存GitHub页面内容到github_page.html用于调试")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尝试多种选择器来查找最新版本
        # 方法1: 查找release-header
        latest_release = soup.find('div', class_='release-header')
        
        # 方法2: 查找release标签
        if not latest_release:
            logger.info("未找到release-header，尝试其他选择器")
            latest_release = soup.select_one('.release')
        
        # 方法3: 查找包含版本信息的任何元素
        if not latest_release:
            logger.info("未找到.release，尝试查找任何版本标签")
            latest_release = soup.select_one('[data-view-component="true"].Link--primary')
        
        if not latest_release:
            # 记录页面结构以便调试
            logger.error("无法找到版本信息，页面结构可能已更改")
            logger.error(f"页面标题: {soup.title.string if soup.title else 'No title'}")
            logger.error(f"页面包含的主要元素: {[tag.name for tag in soup.find_all(limit=10)]}")
            raise Exception("无法找到最新版本信息")
        
        # 尝试多种方式获取版本号
        version_tag = None
        if hasattr(latest_release, 'find'):
            version_tag = latest_release.find('a', class_='Link--primary')
        
        if not version_tag:
            version_tag = soup.select_one('a[data-view-component="true"].Link--primary')
        
        if not version_tag:
            # 尝试查找任何看起来像版本号的文本
            for tag in soup.find_all('a'):
                if tag.text and re.search(r'v?\d+\.\d+\.\d+', tag.text):
                    version_tag = tag
                    break
        
        if not version_tag:
            logger.error("无法找到版本标签")
            raise Exception("无法找到版本标签")
        
        version = version_tag.text.strip()
        # 确保版本号以v开头
        if not version.startswith('v'):
            version = 'v' + version
            
        logger.info(f"找到最新版本: {version}")
        
        return version
    
    except Exception as e:
        logger.error(f"检查版本时出错: {str(e)}")
        # 记录更详细的错误信息
        import traceback
        logger.error(f"详细错误: {traceback.format_exc()}")
        raise


def download_installer(version, max_retries=3):
    """
    下载安装程序，带有重试机制
    参数:
        version: 版本号
        max_retries: 最大重试次数
    返回:
        下载的文件路径
    """
    # 根据版本号拼接下载链接
    download_url = f"https://gh-proxy.com/https://github.com/ArvinLovegood/go-stock/releases/download/{version}/go-stock-amd64-installer.exe"
    logger.info(f"拼接下载链接: {download_url}")
    
    local_filename = os.path.join(DOWNLOAD_DIR, "go-stock-amd64-installer.exe")
    logger.info(f"开始下载安装程序到: {local_filename}")
    
    # 添加User-Agent头，模拟浏览器请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(
                download_url, 
                stream=True, 
                timeout=60, 
                headers=headers
            )
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        # 打印下载进度
                        if total_size > 0:
                            percent = int(100 * downloaded / total_size)
                            sys.stdout.write(f"\r下载进度: {percent}% ({downloaded}/{total_size} 字节)")
                            sys.stdout.flush()
            
            # 验证下载的文件
            if os.path.exists(local_filename) and os.path.getsize(local_filename) > 0:
                if total_size > 0 and os.path.getsize(local_filename) != total_size:
                    logger.warning(f"下载的文件大小({os.path.getsize(local_filename)})与预期大小({total_size})不匹配")
                else:
                    logger.info(f"\n下载完成: {local_filename}")
                    return local_filename
            else:
                logger.error("下载的文件不存在或为空")
                if retries < max_retries - 1:
                    retries += 1
                    logger.info(f"重试下载 ({retries}/{max_retries})...")
                    continue
                else:
                    raise Exception("下载失败：文件不存在或为空")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"下载请求出错: {str(e)}")
            if retries < max_retries - 1:
                wait_time = 2 ** retries  # 指数退避
                logger.info(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                retries += 1
                logger.info(f"重试下载 ({retries}/{max_retries})...")
            else:
                logger.error("达到最大重试次数，下载失败")
                raise
        
        except Exception as e:
            logger.error(f"下载安装程序时出错: {str(e)}")
            import traceback
            logger.error(f"详细错误: {traceback.format_exc()}")
            raise
    
    raise Exception(f"下载失败，已尝试 {max_retries} 次")


def kill_process():
    """
    终止go-stock进程
    """
    try:
        logger.info(f"尝试终止进程: {PROCESS_NAME}")
        
        # 在Windows上使用taskkill命令
        if sys.platform == 'win32':
            try:
                subprocess.run(['taskkill', '/F', '/IM', PROCESS_NAME], 
                              check=True, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
                logger.info(f"成功终止进程: {PROCESS_NAME}")
            except subprocess.CalledProcessError as e:
                if e.returncode == 128:  # 进程未找到
                    logger.info(f"进程未运行: {PROCESS_NAME}")
                else:
                    logger.warning(f"终止进程时出现警告: {e}")
        else:
            logger.warning("不支持的操作系统，无法终止进程")
    
    except Exception as e:
        logger.error(f"终止进程时出错: {str(e)}")
        raise


def run_installer(installer_path):
    """
    运行安装程序
    参数:
        installer_path: 安装程序路径
    """
    try:
        logger.info(f"开始运行安装程序: {installer_path}")
        
        # 确保文件存在
        if not os.path.exists(installer_path):
            raise FileNotFoundError(f"安装程序不存在: {installer_path}")
        
        # 检查文件大小
        file_size = os.path.getsize(installer_path)
        if file_size < 1000000:  # 假设安装程序至少有1MB
            logger.warning(f"安装程序文件大小异常: {file_size} 字节")
        
        # 尝试多种方法运行安装程序
        methods_tried = 0
        max_methods = 3
        
        # 方法1: 使用subprocess.Popen直接运行
        try:
            logger.info("尝试方法1: 使用subprocess.Popen直接运行")
            process = subprocess.Popen([installer_path], shell=True)
            logger.info("安装程序已启动 (方法1)")
            return
        except Exception as e1:
            methods_tried += 1
            logger.warning(f"方法1失败: {str(e1)}")
            
            if methods_tried < max_methods:
                # 方法2: 使用os.startfile (仅Windows)
                try:
                    if sys.platform == 'win32':
                        logger.info("尝试方法2: 使用os.startfile")
                        os.startfile(installer_path)
                        logger.info("安装程序已启动 (方法2)")
                        return
                except Exception as e2:
                    methods_tried += 1
                    logger.warning(f"方法2失败: {str(e2)}")
            
            if methods_tried < max_methods:
                # 方法3: 使用PowerShell以管理员权限运行
                try:
                    logger.info("尝试方法3: 使用PowerShell以管理员权限运行")
                    cmd = f'powershell -Command "Start-Process \'{installer_path}\' -Verb RunAs"'
                    subprocess.run(cmd, shell=True, check=True)
                    logger.info("安装程序已启动 (方法3)")
                    return
                except Exception as e3:
                    methods_tried += 1
                    logger.warning(f"方法3失败: {str(e3)}")
            
            # 如果所有方法都失败
            if methods_tried >= max_methods:
                raise Exception(f"尝试了{max_methods}种方法，但都无法启动安装程序")
    
    except Exception as e:
        logger.error(f"运行安装程序时出错: {str(e)}")
        import traceback
        logger.error(f"详细错误: {traceback.format_exc()}")
        raise


def main():
    """
    主函数
    """
    try:
        logger.info("=== 开始自动更新过程 ===")
        
        # 检查网络连接
        try:
            logger.info("检查网络连接...")
            requests.get("https://github.com", timeout=10)
            logger.info("网络连接正常")
        except requests.exceptions.RequestException as e:
            logger.error(f"网络连接错误: {str(e)}")
            logger.error("请检查您的网络连接并重试")
            return 1
        
        try:
            # 检查最新版本
            logger.info("正在检查最新版本...")
            version = check_latest_version()
            logger.info(f"准备下载版本 {version}")
        except Exception as e:
            logger.error(f"检查版本失败: {str(e)}")
            return 1
        
        try:
            # 下载安装程序
            logger.info("开始下载安装程序...")
            installer_path = download_installer(version)
            logger.info(f"安装程序下载成功: {installer_path}")
        except Exception as e:
            logger.error(f"下载安装程序失败: {str(e)}")
            return 1
        
        try:
            # 终止当前进程
            logger.info("正在终止当前运行的进程...")
            kill_process()
            
            # 等待进程完全终止
            logger.info("等待进程完全终止...")
            time.sleep(2)
        except Exception as e:
            logger.error(f"终止进程失败: {str(e)}")
            # 继续执行，因为即使终止进程失败，我们仍然可以尝试运行安装程序
        
        try:
            # 运行安装程序
            logger.info("正在运行安装程序...")
            run_installer(installer_path)
            logger.info("安装程序已启动")
        except Exception as e:
            logger.error(f"运行安装程序失败: {str(e)}")
            return 1
        
        logger.info("=== 自动更新过程完成 ===")
    
    except Exception as e:
        logger.error(f"自动更新过程失败: {str(e)}")
        import traceback
        logger.error(f"详细错误: {traceback.format_exc()}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())