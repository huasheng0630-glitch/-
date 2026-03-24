# API配置
CRYPTOCOMPARE_API_KEY = "67b391a691168da7f871515ae19ef9831a38822c1192ddba69efd457c737ef2f"
NEWSAPI_KEY = ""  # 如果需要添加NewsAPI，请在此处填写
ALPHA_VANTAGE_KEY = ""  # 如果需要添加Alpha Vantage，请在此处填写

# 应用配置
DEBUG = True
SECRET_KEY = "your-secret-key-change-this-in-production"

# API端点
CRYPTOCOMPARE_NEWS_URL = "https://min-api.cryptocompare.com/data/v2/news/"
CRYPTOCOMPARE_PRICE_URL = "https://min-api.cryptocompare.com/data/price"
CRYPTOCOMPARE_HISTO_URL = "https://min-api.cryptocompare.com/data/v2/histoday"
CRYPTOCOMPARE_HISTO_HOUR_URL = "https://min-api.cryptocompare.com/data/v2/histohour"

# 其他配置
MAX_NEWS_ITEMS = 20  # 最大新闻数量
TIME_WINDOW_HOURS = 24  # 获取最近多少小时内的新闻

# 技术指标配置
MA_PERIODS = [7, 25, 99]  # 移动平均线周期
MACD_FAST = 12  # MACD快线周期
MACD_SLOW = 26  # MACD慢线周期
MACD_SIGNAL = 9  # MACD信号线周期
RSI_PERIOD = 14  # RSI周期
CHART_DATA_POINTS = 100  # 图表数据点数量
CHART_TIMEFRAME = "day"  # 图表时间框架: day, hour, minute