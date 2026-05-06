import os
import json
import time
import subprocess
from pathlib import Path

# 配置
TASK_DIR = "./tasks"
RESULT_DIR = "./results"
os.makedirs(TASK_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

def get_pending_task():
    """获取待执行任务"""
    for f in os.listdir(TASK_DIR):
        path = os.path.join(TASK_DIR, f)
        if not f.endswith(".task"):
            continue
        with open(path, "r", encoding="utf-8") as r:
            task = json.load(r)
        if task.get("status") == "pending":
            return task, path
    return None, None

def run_qwen_code(prompt):
    """调用 qwen code 执行命令"""
    try:
        cmd = f'qwen -y -p "{prompt}"'
        res = subprocess.check_output(cmd, shell=True, text=True, encoding="utf-8", stderr=subprocess.STDOUT)
        return res
    except Exception as e:
        return str(e)

def write_result(task, result):
    """回写结果"""
    print(result)
    result_path = os.path.join(RESULT_DIR, f"{task['id']}.task")
    output = {
        "task_id": task["id"],
        "prompt": task["prompt"],
        "result": result,
        "status": "completed"
    }
    with open(result_path, "w", encoding="utf-8") as w:
        json.dump(output, w, ensure_ascii=False, indent=2)
    print(f"✅ 结果已回写: {result_path}")

def mark_task_done(task_path):
    """标记任务完成"""
    with open(task_path, "r", encoding="utf-8") as r:
        task = json.load(r)
    task["status"] = "completed"
    with open(task_path, "w", encoding="utf-8") as w:
        json.dump(task, w, ensure_ascii=False, indent=2)

def main():
    print("🚀 Qwen Code 自动任务执行机已启动（监听中...）")
    while True:
        task, path = get_pending_task()
        if not task:
            time.sleep(5)
            continue

        print(f"\n📦 发现新任务: {task['id']}")
        result = run_qwen_code(task["prompt"])
        write_result(task, result)
        mark_task_done(path)
        print("✅ 任务完成！等待下一个任务...")


'''
基于qwen code的无人值守测试功能

读取tasks目录下的文件
执行qwen -y -p "提示词"
将结果返回到results目录

'''
if __name__ == "__main__":
    main()