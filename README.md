# Tg 消息合并助手

**实例:** [@M2MGBot](https://t.me/M2MGBot)

## 环境变量

将 `.env.example` 文件重命名为 `.env`

| 名称        | 描述                              | 默认值 |
|-------------|-----------------------------------|--------|
| `API_ID`    | 登录 https://my.telegram.org 获取 |        |
| `API_HASH`  | 登录 https://my.telegram.org 获取 |        |
| `BOT_TOKEN` | 在 https://t.me/BotFather 获取    |        |
| `BOT_PROXY` | Bot 代理, 海外服务器不用填        |        |

## 开始部署

#### Docker (推荐):

**在项目根目录运行:**

```shell
sudo sh start.sh # 构建并运行 Bot
# 其他命令:
sudo sh start.sh -h # 查看帮助
sudo sh start.sh stop  # 停止 Bot
sudo sh start.sh restart # 重启 Bot
```

#### 源码运行:

**在项目根目录运行:**

```shell
uv sync
uv run bot.py 
```

## 使用

私聊 Bot 发送 `/start` 即可开始, 发送 `开始` 后发送要合并的媒体文件, 完成后发送 `结束` 即可
