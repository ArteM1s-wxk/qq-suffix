# qq-suffix

QQ 频道自动后缀工具：在 QQ 客户端聊天时，按回车发送消息前自动在末尾追加一段可配置的后缀。

## 功能

- **自动追加后缀**：在 QQ 客户端窗口按回车发送时，自动在消息末尾补上后缀
- **后缀另起一行**（可选）：勾选后后缀换行单独成行
- **可视化窗口**：修改后缀内容、启动/停止开关
- **F8 全局热键**：无需切回窗口即可快速启停
- **配置持久化**：后缀与换行开关保存在 exe 旁边的 `config.json`

## 下载与使用

1. 到 [Releases](../../releases) 页面下载 `qq-suffix.zip`
2. 解压到任意目录
3. 双击 `qq-suffix.exe` 运行

> 首次运行若安全软件提示「全局键盘钩子」，请选择允许，否则工具无法监听回车。

## 从源码运行

需要 Python 3.11 与 [uv](https://docs.astral.sh/uv/)。

```bash
uv sync
uv run python -m qq_suffix
```

## 打包为 exe

```bash
uv run pyinstaller --onedir --windowed --name qq-suffix --paths src run.py
```

产物在 `dist/qq-suffix/`，整个文件夹一起分发。

## 说明

- 仅对 QQ 客户端（`QQ.exe`）窗口生效，其他软件不受影响。
- 后缀默认「音音」，可在窗口中修改。
- 因 QQ 的频道面板与普通聊天同属 `QQ.exe` 进程，工具对 QQ 客户端所有窗口均生效。
