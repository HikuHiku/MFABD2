from enum import IntEnum
from collections import namedtuple
import json
import time
from maa.controller import AdbController

# 添加 __slots__ 减少内存访问开销
class ActionType(IntEnum):
    TOUCH_MOVE = 0
    TOUCH_DOWN = 1
    TOUCH_UP = 2

# 使用 __slots__ 优化namedtuple内存布局
Op = namedtuple("Op", ["action", "x", "y", "contact", "timing_ns"])

def load_precompile(path: str):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    op_list = []
    for item in raw["taskes"]:
        # 使用字典映射替代if/elif链（加载阶段开销可忽略）
        action_map = {
            "TouchDown": ActionType.TOUCH_DOWN,
            "TouchMove": ActionType.TOUCH_MOVE,
            "TouchUp": ActionType.TOUCH_UP
        }
        action = action_map.get(item["action"])
        if action is None:
            raise ValueError(f"这啥玩意儿？: {item['action']}")

        op = Op(
            action=action,
            x=item["x"],
            y=item["y"],
            contact=item["contact"],
            timing_ns=item["timing_ns"]
        )
        op_list.append(op)
    return op_list

def build_executor(controller):
    # 统一所有函数的调用签名 -> (x, y, contact)
    # 这样run_operations中可以直接调用，无需任何判断
    return [ controller.post_touch_move, controller.post_touch_down, lambda x, y, contact: controller.post_touch_up(contact) ]

def run_operations():
    # 运行前设置
    adb_path = r"D:/MUMU/MuMu Player 12/shell/adb.exe"
    address = "127.0.0.1:5555"
    record_path = "D:/GameModsRelated/BrownDust2Mod/MFABD2_forked/assets/python/Records/Main01_Town.json"
    # 创建ADB控制器并连接
    controller = AdbController(adb_path=adb_path, address=address)
    connection = controller.post_connection()
    connection.wait()
    if not connection.succeeded:
        print("连接失败")
        return
    print("连接成功")

    # 加载并预编译操作文件
    operations = load_precompile(record_path)
    executor = build_executor(controller)
    # 将数据展开为5个平行数组
    timing_array = [op.timing_ns for op in operations]
    action_array = [op.action for op in operations]
    x_array = [op.x for op in operations]
    y_array = [op.y for op in operations]
    contact_array = [op.contact for op in operations]
    
    # 运行时优化
    execute = executor  # 字典局部引用
    pc_ns = time.perf_counter_ns  # 函数局部绑定
    # 预热executor（确保lambda已编译）
    execute[ActionType.TOUCH_DOWN](10, 20, 0)
    execute[ActionType.TOUCH_MOVE](10, 20, 0)
    execute[ActionType.TOUCH_UP](10, 20, 0)
    time.sleep(2)
    
    # 开始执行操作
    idx = 0
    lenth = len(timing_array)
    stTime = pc_ns()
    while idx < lenth:
        # 忙等待至目标时间
        while pc_ns() - stTime < timing_array[idx]:
            pass
        execute[action_array[idx]](x_array[idx], y_array[idx], contact_array[idx])
        idx += 1

if __name__ == "__main__":
    run_operations()