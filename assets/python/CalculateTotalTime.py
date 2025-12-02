import json
import sys
from pathlib import Path

def CalculateTotalTime(mumu_json_path):
    """转换MuMu录制文件为更易读取的结构化JSON文件"""
    
    with open(mumu_json_path, 'r', encoding='utf-8') as f:
        mumu_data = json.load(f)
    
    actions = mumu_data['actions']
    
    i = 0
    TotalTiming = 0 # 用于将无意义"release"的timing累加到下一个有效操作上
    
    # 遍历转换
    while i < len(actions):
        action = actions[i]
        TotalTiming = TotalTiming + action['timing']
        i += 1
    print(f"✅ 总时间: {TotalTiming/1000} s")

# ==================== 使用示例 ====================

if __name__ == "__main__":
        
    input_file = "D:/GameModsRelated/BrownDust2Mod/MFABD2_forked/assets/python/Test.mmor"
    
    if not Path(input_file).exists():
        print(f"❌ 文件不存在: {input_file}")
        sys.exit(1)
    
    CalculateTotalTime(input_file)