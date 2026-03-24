# 股票 / 加密货币交易分析系统

一个基于 Flask 的交易分析仪表盘，聚合展示价格走势、技术指标、新闻情绪和 AI 交易观点。

## 当前状态

- 主要优化方向已完成：
  - 聚合分析接口，减少重复请求
  - 首页改版为轻玻璃 Apple 风格
  - 前端拆分为独立 CSS / JS
  - Plotly 改为按需加载
- 当前**优先支持加密货币分析**
- 股票入口界面仍保留，但由于 `ALPHA_VANTAGE_KEY` 未配置，股票分析目前不会正常返回完整结果

## 功能特性

- 聚合分析：一次请求返回新闻、价格、技术分析和 AI 综合结论
- 技术分析：MA、MACD、RSI、布林带、成交量等
- 消息面分析：新闻抓取 + TextBlob 情绪判断
- AI 交易员视角：综合评分、风险提示、仓位建议
- 新版前端：更清晰的信息层级、微交互、时间周期切换
- 短期缓存：减少重复 API 调用，改善响应速度

## 快速开始

### Windows

推荐直接运行：

```bat
start_fixed.bat
```

兼容入口：

```bat
start.bat
```

### Linux / macOS

```bash
chmod +x start.sh
./start.sh
```

### 手动启动

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

启动应用：

```bash
python app.py
```

浏览器访问：

```text
http://localhost:5000
```

## 主要接口

- `GET /`：主页面
- `POST /api/dashboard`：聚合分析主接口
- `POST /analyze`：新闻情绪分析
- `GET /api/chart/<symbol>`：图表与价格数据
- `GET /api/technical/<symbol>`：技术分析摘要
- `GET /api/trader-analysis/<symbol>`：AI 交易员分析
- `GET /api/price/<symbol>`：价格信息
- `GET /api/health`：健康检查
- `GET /api/status`：API 状态
- `GET /api/symbols`：热门代码列表

## 项目结构

```text
交易分析/
├── app.py
├── config.py
├── requirements.txt
├── start.bat
├── start_fixed.bat
├── start.sh
├── diagnose.bat
├── diagnose_fixed.bat
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── app.css
│   └── js/
│       └── app.js
├── modules/
│   ├── news_fetcher.py
│   ├── chart_fetcher.py
│   ├── sentiment_analyzer.py
│   ├── technical_analyzer.py
│   └── trader_analysis.py
└── utils/
    └── helpers.py
```

## 依赖说明

核心依赖见 `requirements.txt`，主要包括：

- Flask
- requests
- pandas
- numpy
- textblob
- plotly

## 配置说明

当前配置文件：

- [config.py](config.py)

已配置：

- `CRYPTOCOMPARE_API_KEY`

暂未配置：

- `ALPHA_VANTAGE_KEY`
- `NEWSAPI_KEY`

因此目前建议只使用：

- BTC
- ETH
- SOL
- BNB
- XRP
- DOGE
- ADA
- DOT

## 性能优化结果

本轮改造已处理的关键问题：

- 前端从并发 4 个请求改为 1 个主请求
- 时间周期切换仅刷新图表接口
- 避免 AI 分析重复抓取新闻和价格数据
- 为新闻、价格、K 线、涨跌幅增加内存 TTL 缓存
- 移除首页自动分析 BTC 的首屏阻塞行为
- 去掉 jQuery 依赖
- Plotly 改为延迟加载

## 注意事项

- 本项目分析结果仅供参考，不构成投资建议
- CryptoCompare 免费接口存在频率限制
- 当前股票分析未启用，不建议在现阶段使用股票入口

## 故障排查

### 1. 启动失败

检查：

- Python 版本是否 >= 3.8
- 虚拟环境依赖是否安装完成
- 5000 端口是否被占用

### 2. 页面打开但分析失败

检查：

- 网络是否正常
- API 密钥是否有效
- 控制台 / 终端是否有报错

### 3. 依赖缺失

如果看到类似：

```text
ModuleNotFoundError: No module named 'requests'
```

请先安装依赖：

```bash
pip install -r requirements.txt
```

## 免责声明

本系统提供的信息与分析仅供学习、研究和界面演示使用。任何投资决策应由用户独立判断并自行承担风险。
