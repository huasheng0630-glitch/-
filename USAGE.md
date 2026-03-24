# 使用说明

## 推荐启动方式

### Windows

优先使用：

```bat
start_fixed.bat
```

也可以使用：

```bat
start.bat
```

### Linux / macOS

```bash
chmod +x start.sh
./start.sh
```

## 手动启动

进入项目目录后执行：

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

启动：

```bash
python app.py
```

打开浏览器访问：

```text
http://localhost:5000
```

## 当前建议使用方式

当前版本已经完成第三轮收口，建议这样使用：

1. 进入首页
2. 优先输入加密货币代码，如 `BTC`、`ETH`、`SOL`
3. 点击“开始分析”
4. 首次分析会走聚合接口，返回：
   - 当前价格
   - 技术分析
   - 新闻情绪
   - AI 交易员综合结论
5. 切换 `1D / 1H / 1M` 时，只会刷新图表相关数据

## 当前支持说明

### 推荐使用

- 加密货币分析：已可用

### 暂不建议使用

- 股票分析：界面入口保留，但当前未配置 `ALPHA_VANTAGE_KEY`，所以暂不支持完整股票分析流程

## 常见问题

### 1. 启动时报依赖缺失

例如：

```text
ModuleNotFoundError: No module named 'requests'
```

处理方式：

```bash
pip install -r requirements.txt
```

### 2. 页面可以打开，但点击分析失败

请检查：

- 网络连接是否正常
- `config.py` 中的加密货币 API 是否可用
- 终端控制台是否有报错输出

### 3. 端口 5000 被占用

处理方式：

- 关闭占用 5000 端口的程序
- 然后重新执行启动脚本

### 4. Windows 双击脚本闪退

请直接在命令行中运行：

```cmd
cd "e:\毕业论文\交易分析"
"venv\Scripts\python.exe" app.py
```

这样可以直接看到错误信息。

## 诊断方式

Windows 下可以运行：

```bat
diagnose_fixed.bat
```

它会帮助你检查：

- Python 是否存在
- venv 是否存在
- 依赖是否安装
- Flask / requests / textblob 是否可导入
- 应用是否可被快速拉起

## 本次改造后的变化

与旧版本相比，现在的使用体验有这些变化：

- 首页不再自动发起 BTC 分析
- 前端不再并发打 4 个接口
- 图表库改为按需加载
- 页面结构更清晰，视觉层次更统一
- 结果页支持更轻的局部刷新

## 建议测试代码

推荐先用这些代码做体验：

- `BTC`
- `ETH`
- `SOL`
- `BNB`

## 备注

分析结果仅供参考，不构成投资建议。
