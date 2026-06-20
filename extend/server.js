const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const WebSocket = require('ws');
const path = require('path');

const ACP_WS_URL = 'ws://127.0.0.1:4500/acp';
const ACP_TOKEN = 'sk-qwen-123456-secret-token';
const PORT = 3000;
const WORKSPACE = '/Users/chensong';

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "*" }
});

app.use(express.static(path.join(__dirname, 'public')));

let acpWs = null;
let acpConnected = false;
let sessionId = null;
let requestId = 1;

function connectACP() {
  if (acpWs) acpWs.close();

  const headers = {
    Authorization: `Bearer ${ACP_TOKEN}`
  };
  acpWs = new WebSocket(ACP_WS_URL, { headers });

  acpWs.on('open', () => {
    acpConnected = true;
    console.log('✅ ACP WebSocket 已连接');
    sessionId = null;
    requestId = 1;
    const initMsg = JSON.stringify({
      jsonrpc: '2.0',
      id: 0,
      method: 'initialize',
      params: {
        protocolVersion: 1,
        clientCapabilities: {
          fs: {
            readTextFile: true,
            writeTextFile: true
          },
          terminal: true
        },
        clientInfo: {
          name: 'qwen-acp-terminal',
          version: '1.0.0'
        }
      }
    });
    acpWs.send(initMsg);
  });

  acpWs.on('message', (raw) => {
    try {
      const data = JSON.parse(raw);
      console.log('ACP消息:', JSON.stringify(data));

      if (data.jsonrpc === '2.0') {
        if (data.id !== undefined) {
          if (data.result) {
            if (data.id === 0) {
              const newSessionReq = JSON.stringify({
                jsonrpc: '2.0',
                id: requestId++,
                method: 'session/new',
                params: {
                  cwd: WORKSPACE
                }
              });
              acpWs.send(newSessionReq);
            } else {
              sessionId = data.result.sessionId;
              io.emit('acp_output', { type: 'result', payload: data.result });
            }
          } else if (data.error) {
            io.emit('acp_output', { type: 'error', payload: { message: data.error.message, code: data.error.code } });
          }
        } else if (data.method === 'session/update') {
          const update = data.params.update;
          if (update.kind === 'AgentMessageChunk') {
            io.emit('acp_output', { type: 'chat_chunk', payload: { content: update.content } });
          } else if (update.kind === 'TurnEnd') {
            io.emit('acp_output', { type: 'chat_done', payload: {} });
          } else if (update.kind === 'ToolCall') {
            io.emit('acp_output', { type: 'tool_call', payload: { tool: update, toolId: update.callId } });
          } else if (update.kind === 'ToolCallUpdate') {
            io.emit('acp_output', { type: 'tool_update', payload: update });
          } else {
            io.emit('acp_output', { type: 'session_update', payload: update });
          }
        } else if (data.method === 'request_permission') {
          io.emit('acp_output', { type: 'permission_request', payload: data.params });
        } else {
          io.emit('acp_output', { type: data.method || 'unknown', payload: data.params || data });
        }
      } else {
        io.emit('acp_output', data);
      }
    } catch (e) {
      io.emit('acp_output_raw', raw.toString());
    }
  });

  acpWs.on('close', () => {
    acpConnected = false;
    sessionId = null;
    console.log('❌ ACP 断开，3秒重连');
    setTimeout(connectACP, 3000);
  });

  acpWs.on('error', (err) => {
    console.error('ACP error:', err.message);
  });
}

io.on('connection', (socket) => {
  console.log('前端终端接入');

  socket.on('user_input', (query) => {
    if (!acpConnected || !acpWs) {
      socket.emit('print', '❌ ACP服务未连接，请稍后重试\n');
      return;
    }
    if (!sessionId) {
      socket.emit('print', '❌ 会话未初始化，请等待...\n');
      return;
    }
    const promptReq = JSON.stringify({
      jsonrpc: '2.0',
      id: requestId++,
      method: 'session/prompt',
      params: {
        sessionId: sessionId,
        prompt: [{ type: 'text', text: query }]
      }
    });
    acpWs.send(promptReq);
  });

  socket.on('tool_confirm', (data) => {
    if (!acpWs || !sessionId) return;
    acpWs.send(JSON.stringify({
      jsonrpc: '2.0',
      id: requestId++,
      method: 'session/tool_result',
      params: {
        sessionId: sessionId,
        callId: data.toolId,
        result: data.allow ? { success: true } : { success: false, error: 'User denied' }
      }
    }));
  });

  socket.on('disconnect', () => {
    console.log('前端终端断开');
  });
});

connectACP();

server.listen(PORT, () => {
  console.log(`终端页面运行: http://127.0.0.1:${PORT}`);
  console.log(`对接ACP: ${ACP_WS_URL}`);
});
