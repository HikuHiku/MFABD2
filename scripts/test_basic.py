#!/usr/bin/env python3
"""
最简单的测试脚本 - 验证核心逻辑
"""

import subprocess
import sys

def run_simple_git_command():
    """运行简单的git命令测试"""
    try:
        # 获取当前标签列表
        result = subprocess.run(
            ["git", "tag", "-l", "v*"],
            capture_output=True, 
            text=True,
            check=True
        )
        
        tags = result.stdout.strip().split('\n')
        print("找到的标签:", tags)
        
        # 简单的版本排序逻辑
        formal_versions = [tag for tag in tags if '-beta' not in tag and '-ci' not in tag]
        print("正式版标签:", formal_versions)
        
        return True
        
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == "__main__":
    print("开始基础验证...")
    success = run_simple_git_command()
    if success:
        print("✅ 基础验证通过!")
    else:
        print("❌ 基础验证失败!")
        sys.exit(1)