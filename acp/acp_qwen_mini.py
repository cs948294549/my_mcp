#!/usr/bin/env python3
"""
ACP Client Minimal Example - 最小化的实现

这个示例展示了 ACP 协议的核心原理：
1. 通过 npx 启动 Qwen Code，并传递 --acp 参数
2. 使用 stdio（标准输入/输出）进行通信
3. 发送 NDJSON（每行一个 JSON 对象）格式的消息
4. 接收流式返回的响应
"""

import subprocess
import json


def main():
    # 1. 启动 Qwen Code 进程
    # ACP agent 必须通过 --acp 参数启动
    print("Starting Qwen Code with ACP protocol...\n")

    proc = subprocess.Popen(
        ["qwen.cmd", "--acp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,  # 文本模式
        bufsize=1   # 行缓冲
    )

    def send_rpc(method, params):
        """发送 JSON-RPC 请求"""
        msg = json.dumps({
            "jsonrpc": "2.0",
            "id": send_rpc.counter,
            "method": method,
            "params": params
        }) + "\n"
        send_rpc.counter += 1

        proc.stdin.write(msg)
        proc.stdin.flush()

        # 打印发送的内容（仅用于调试）
        print(f"[SEND] {msg.strip()}\n")

    send_rpc.counter = 1

    try:
        # 2. 初始化连接
        print("=" * 60)
        print("Step 1: Initialize connection")
        print("=" * 60)

        send_rpc("initialize", {
            "protocolVersion": "2024-09-11",
            "clientInfo": {"name": "minimal-client", "version": "1.0.0"},
            "capabilities": {}
        })

        # 等待片刻让 agent 准备就绪
        import time
        time.sleep(1)

        # 3. 创建会话
        print("\n" + "=" * 60)
        print("Step 2: Create session")
        print("=" * 60)

        send_rpc("newSession", {
            "cwd": ".",
            "mcpServers": {}
        })

        time.sleep(1)

        # 4. 发送消息
        print("\n" + "=" * 60)
        print("Step 3: Send message and stream response")
        print("=" * 60)

        prompt = "List all files in the current directory."

        send_rpc("sendMessage", {
            "sessionId": "session-1",  # 简单模式下可以用任意 ID
            "message": {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        })

        print(f"\nYour message: {prompt}\n")
        print("-" * 60)
        print("Qwen Code response:\n")

        # 5. 流式读取响应
        for line in proc.stdout:
            # 移除终端颜色代码等控制字符
            clean_line = line.replace('\x1b', '').replace('\x1b[', '')
            print(clean_line, end="", flush=True)

            # 如果收到空行或检测到完成信号，可以停止
            if not line.strip():
                break

        print("\n" + "-" * 60)
        print("\nDone!")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    finally:
        # 6. 清理：终止子进程
        print("\nCleaning up...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except:
            proc.kill()
        print("Done.")


if __name__ == "__main__":
    main()
