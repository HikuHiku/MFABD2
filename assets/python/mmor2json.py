import json
import sys
from pathlib import Path

def convert_mumu_to_Result(mumu_json_path, output_path=None):
    """转换MuMu录制文件为更易读取的结构化JSON文件"""
    
    with open(mumu_json_path, 'r', encoding='utf-8') as f:
        mumu_data = json.load(f)
    
    actions = mumu_data['actions']
    
    # 过滤开头的release块
    start_idx = 1
    while start_idx < len(actions) and actions[start_idx]['data'] == 'release':
        start_idx += 1
    
    if start_idx > len(actions):
        print("❌ 无可转换的操作块")
        return
    
    filtered_actions = actions[start_idx:len(actions)]
    Result = {"taskes": []}
    i = 0
    PressingList = [] # 记录当前按下的手指ID列表
    AddTiming = 0 # 用于将无意义"release"的timing累加到下一个有效操作上
    
    # 遍历转换
    while i < len(filtered_actions):
        action = filtered_actions[i]
        data = action['data'].replace('press_rel:', '')
        timing = action['timing'] + AddTiming# timing在mumu录制结果中指的是所在action与上一个action之间的时间间隔，即pre_delay
        AddTiming = AddTiming + action['timing']
        contact = int(action['extra1'])
        
        if data == "release":
            # 判断是否是有效的TouchUp            
            if contact in PressingList:
                # 上一个块是press_rel → TouchUp
                Result["taskes"].append({
                    "action": "TouchUp",
                    "x": 0,
                    "y": 0,
                    "contact": contact,
                    "timing_ns": timing * 1_000_000,
                })
                PressingList.remove(contact)
        else:
            # 坐标换算（MuMu坐标系 → 操作坐标系）
            MuMuYX = data.strip('()').split(',')
            y = round(720 - 1280 * float(MuMuYX[0]))
            x = round(720 * float(MuMuYX[1]))
            # 判断是TouchDown还是TouchMove
            if contact in PressingList:
                # 当前已按下这个手指ID → TouchMove
                action_type = "TouchMove"
            else:
                # 目前没按下这个手指ID → TouchDown
                PressingList.append(contact)
                action_type = "TouchDown"
            Result["taskes"].append({
                "action": action_type,
                "x": x,
                "y": y,
                "contact": contact,
                "timing_ns": timing * 1_000_000,
            })
        i += 1
    
    # 保存
    if output_path is None:
        output_path = mumu_json_path.replace('.mmor', '.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(Result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 转换完成: {mumu_json_path} → {output_path}")
    print(f"生成操作数: {len(Result["taskes"])}")

# ==================== 使用示例 ====================

if __name__ == "__main__":
        
    input_file = "D:/GameModsRelated/BrownDust2Mod/MFABD2_forked/assets/python/Records/Main01_Town.mmor"
    
    if not Path(input_file).exists():
        print(f"❌ 文件不存在: {input_file}")
        sys.exit(1)
    
    convert_mumu_to_Result(input_file)