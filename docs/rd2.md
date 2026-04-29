# claude code对接微信
```text
https://github.com/formulahendry/wechat-acp

安装微信acp
npx wechat-acp --agent claude

然后在微信端使用Clawbot发送消息
就能直接对接到本地的claude code上处理消息了
```

# ilink相关接口
```text
iLink 的主要 API 如下：
GET /ilink/bot/get_bot_qrcode
功能：获取登录二维码
参数：bot_type
GET /ilink/bot/get_qrcode_status
功能：轮询二维码状态
参数：qrcode
POST /ilink/bot/getupdates
功能：长轮询拉取消息
参数：get_updates_buf
POST /ilink/bot/sendmessage
功能：发送 / 回复消息
参数：msg，需 context_token
POST /ilink/bot/getuploadurl
功能：获取媒体上传 URL
参数：filekey / media_type / md5
POST /ilink/bot/getconfig
功能：获取机器人配置（含 typing_ticket）
POST /ilink/bot/sendtyping
功能：发送 “正在输入” 提示
参数：typing_ticket 等
```