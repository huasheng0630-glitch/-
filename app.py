#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票/加密货币新闻情感分析系统
主应用文件（优化版）
"""

import logging
import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from config import CRYPTOCOMPARE_API_KEY
from modules.news_fetcher import fetch_news
from modules.sentiment_analyzer import analyze_news, get_sentiment_summary
from modules.chart_fetcher import fetch_ohlcv, get_current_price, get_price_change
from modules.technical_analyzer import calculate_indicators, analyze_indicators
from modules.trader_analysis import TraderAnalyzer
from utils.helpers import validate_symbol, format_datetime, get_api_status

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s %(name)s: %(message)s')
for noisy_logger_name in ('werkzeug', __name__, 'modules.news_fetcher', 'modules.chart_fetcher', 'modules.trader_analysis'):
    logging.getLogger(noisy_logger_name).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_pyfile('config.py')
trader_analyzer = TraderAnalyzer()


def _normalize_request_input(source):
    symbol = source.get('symbol', '').strip().upper()
    asset_type = source.get('asset_type', 'crypto')
    timeframe = source.get('timeframe', 'hour')
    limit = int(source.get('limit', 100))
    return symbol, asset_type, timeframe, limit


def _build_news_payload(symbol: str, asset_type: str, limit: int = 10):
    news_list = fetch_news(symbol, asset_type=asset_type, limit=limit)
    analyzed_news, overall_result = analyze_news(news_list)
    summary = get_sentiment_summary(symbol, overall_result, len(analyzed_news))
    key_news = trader_analyzer._extract_key_news(analyzed_news)

    formatted_news = []
    for news in analyzed_news:
        formatted = news.copy()
        if 'published_time' in formatted and isinstance(formatted['published_time'], datetime):
            formatted['published_time'] = format_datetime(formatted['published_time'])
        formatted_news.append(formatted)

    snapshot = trader_analyzer.build_news_snapshot(formatted_news, overall_result, summary, key_news)
    return {
        'symbol': symbol,
        'asset_type': asset_type,
        'news_count': len(formatted_news),
        'news_list': formatted_news,
        'sentiment_analysis': overall_result,
        'summary': summary,
        'key_news': key_news,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'api_status': get_api_status(),
        'snapshot': snapshot
    }


def _build_price_payload(symbol: str, asset_type: str, timeframe: str = 'hour', limit: int = 100):
    df = fetch_ohlcv(symbol, timeframe=timeframe, limit=limit, asset_type=asset_type)
    if df.empty:
        raise ValueError(f"未找到{symbol}的K线数据")

    df_with_indicators = calculate_indicators(df)
    chart_data = df_with_indicators.to_dict('records')
    for item in chart_data:
        for key, value in item.items():
            if isinstance(value, float) and (value != value):
                item[key] = None

    technical_analysis = analyze_indicators(df_with_indicators)
    current_price = get_current_price(symbol)
    price_change_24h = get_price_change(symbol, '24h')
    price_change_7d = get_price_change(symbol, '7d')

    snapshot = trader_analyzer.build_price_snapshot(
        chart_data,
        technical_analysis,
        current_price,
        price_change_24h,
        price_change_7d,
    )

    return {
        'symbol': symbol,
        'asset_type': asset_type,
        'timeframe': timeframe,
        'current_price': current_price,
        'price_change_24h': price_change_24h,
        'price_change_7d': price_change_7d,
        'chart_data': chart_data,
        'technical_analysis': technical_analysis,
        'data_points': len(chart_data),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'snapshot': snapshot
    }


@app.route('/')
def index():
    return render_template('index.html', api_status=get_api_status())


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        symbol, asset_type, _, _ = _normalize_request_input(request.form)

        if not symbol:
            return jsonify({"error": "请输入股票/加密货币代码"}), 400
        if not validate_symbol(symbol):
            return jsonify({"error": "无效的代码格式，请使用字母和数字组合"}), 400
        if asset_type == "crypto" and not CRYPTOCOMPARE_API_KEY:
            return jsonify({
                "error": "加密货币分析需要配置CryptoCompare API密钥",
                "symbol": symbol,
                "asset_type": asset_type
            }), 503

        payload = _build_news_payload(symbol, asset_type, limit=10)
        if payload['news_count'] == 0:
            return jsonify({
                "error": f"未找到{symbol}的相关新闻",
                "symbol": symbol,
                "asset_type": asset_type,
                "suggestion": "请尝试其他代码或稍后重试"
            }), 404

        payload.pop('snapshot', None)
        return jsonify(payload)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("分析过程中出错")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/dashboard', methods=['POST'])
def dashboard_analyze():
    try:
        symbol, asset_type, timeframe, limit = _normalize_request_input(request.form or request.json or {})

        if not symbol:
            return jsonify({"error": "请输入股票/加密货币代码"}), 400
        if not validate_symbol(symbol):
            return jsonify({"error": "无效的代码格式，请使用字母和数字组合"}), 400
        if asset_type == "crypto" and not CRYPTOCOMPARE_API_KEY:
            return jsonify({"error": "加密货币分析需要配置CryptoCompare API密钥"}), 503

        news_payload = _build_news_payload(symbol, asset_type, limit=10)
        price_payload = _build_price_payload(symbol, asset_type, timeframe=timeframe, limit=limit)
        trader_analysis = trader_analyzer.analyze_asset(
            symbol,
            asset_type,
            news_data=news_payload['snapshot'],
            price_data=price_payload['snapshot'],
        )

        news_payload.pop('snapshot', None)
        price_payload.pop('snapshot', None)

        return jsonify({
            'symbol': symbol,
            'asset_type': asset_type,
            'timeframe': timeframe,
            'news': news_payload,
            'price': price_payload,
            'trader_analysis': trader_analysis,
            'api_status': get_api_status(),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("仪表板分析失败")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "股票/加密货币新闻情感分析系统",
        "api_status": get_api_status(),
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/status')
def api_status():
    return jsonify(get_api_status())


@app.route('/api/symbols')
def popular_symbols():
    popular = {
        "crypto": [
            {"symbol": "BTC", "name": "比特币"},
            {"symbol": "ETH", "name": "以太坊"},
            {"symbol": "XRP", "name": "瑞波币"},
            {"symbol": "LTC", "name": "莱特币"},
            {"symbol": "BCH", "name": "比特币现金"},
            {"symbol": "ADA", "name": "卡尔达诺"},
            {"symbol": "DOT", "name": "波卡"},
            {"symbol": "LINK", "name": "Chainlink"},
            {"symbol": "BNB", "name": "币安币"},
            {"symbol": "DOGE", "name": "狗狗币"}
        ],
        "stock": [
            {"symbol": "AAPL", "name": "苹果公司"},
            {"symbol": "GOOGL", "name": "谷歌"},
            {"symbol": "MSFT", "name": "微软"},
            {"symbol": "AMZN", "name": "亚马逊"},
            {"symbol": "TSLA", "name": "特斯拉"},
            {"symbol": "NVDA", "name": "英伟达"},
            {"symbol": "META", "name": "Meta"},
            {"symbol": "NFLX", "name": "奈飞"}
        ]
    }
    return jsonify(popular)


@app.route('/api/chart/<symbol>')
def get_chart_data(symbol):
    try:
        if not validate_symbol(symbol):
            return jsonify({"error": "无效的代码格式"}), 400

        timeframe = request.args.get('timeframe', 'day')
        limit = int(request.args.get('limit', 100))
        asset_type = request.args.get('asset_type', 'crypto')
        payload = _build_price_payload(symbol, asset_type, timeframe=timeframe, limit=limit)
        payload.pop('snapshot', None)
        return jsonify(payload)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("获取图表数据失败")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/technical/<symbol>')
def get_technical_analysis(symbol):
    try:
        if not validate_symbol(symbol):
            return jsonify({"error": "无效的代码格式"}), 400

        timeframe = request.args.get('timeframe', 'day')
        limit = int(request.args.get('limit', 100))
        asset_type = request.args.get('asset_type', 'crypto')
        payload = _build_price_payload(symbol, asset_type, timeframe=timeframe, limit=limit)
        return jsonify({
            "symbol": symbol,
            "timeframe": timeframe,
            "technical_analysis": payload['technical_analysis'],
            "data_points": payload['data_points'],
            "timestamp": payload['timestamp']
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("技术分析失败")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/trader-analysis/<symbol>')
def get_trader_analysis(symbol):
    try:
        if not validate_symbol(symbol):
            return jsonify({"error": "无效的代码格式"}), 400

        asset_type = request.args.get('asset_type', 'crypto')
        news_payload = _build_news_payload(symbol, asset_type, limit=10)
        price_payload = _build_price_payload(symbol, asset_type, timeframe='day', limit=30)
        analysis = trader_analyzer.analyze_asset(
            symbol,
            asset_type,
            news_data=news_payload['snapshot'],
            price_data=price_payload['snapshot'],
        )

        return jsonify({
            "symbol": symbol,
            "asset_type": asset_type,
            "analysis": analysis,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("交易员分析失败")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/price/<symbol>')
def get_price_info(symbol):
    try:
        if not validate_symbol(symbol):
            return jsonify({"error": "无效的代码格式"}), 400

        current_price = get_current_price(symbol)
        if current_price is None:
            return jsonify({"error": f"无法获取{symbol}的价格"}), 404

        return jsonify({
            "symbol": symbol,
            "current_price": current_price,
            "price_change_24h": get_price_change(symbol, '24h'),
            "price_change_7d": get_price_change(symbol, '7d'),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("获取价格信息失败")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', True), host='0.0.0.0', port=5000)
