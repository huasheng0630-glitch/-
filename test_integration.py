#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试：测试所有模块协同工作
"""

import sys
import os
sys.path.append('.')

from modules.chart_fetcher import fetch_ohlcv, get_current_price, get_price_change
from modules.news_fetcher import fetch_news
from modules.sentiment_analyzer import analyze_news, get_sentiment_summary
from modules.technical_analyzer import calculate_indicators, analyze_indicators
from modules.trader_analysis import analyze_asset

def test_chart():
    print("=== 测试图表数据获取 ===")
    try:
        df = fetch_ohlcv("BTC", "day", limit=5)
        print(f"  OHLCV数据: {len(df)} 条记录")
        if not df.empty:
            print(f"    列: {list(df.columns)}")
            print(f"    最后一条: {df.iloc[-1]['time']}, 收盘价: ${df.iloc[-1]['close']}")

        price = get_current_price("BTC")
        print(f"  当前价格: ${price}")

        change = get_price_change("BTC", "24h")
        print(f"  24小时价格变化: {change}")
        return True
    except Exception as e:
        print(f"  图表测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_news():
    print("\n=== 测试新闻获取 ===")
    try:
        news_list = fetch_news("BTC", asset_type="crypto", limit=5)
        print(f"  获取到 {len(news_list)} 条新闻")
        if news_list:
            for i, news in enumerate(news_list[:2]):
                print(f"    新闻{i+1}: {news.get('title', '无标题')[:50]}...")
        return news_list
    except Exception as e:
        print(f"  新闻测试失败: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_sentiment(news_list):
    print("\n=== 测试情感分析 ===")
    if not news_list:
        print("  无新闻数据，跳过情感分析")
        return None, None

    try:
        analyzed_news, overall_result = analyze_news(news_list)
        print(f"  情感分析完成")
        print(f"    总体得分: {overall_result['overall_score']}")
        print(f"    总体标签: {overall_result['overall_chinese_label']}")
        print(f"    正面: {overall_result['positive_count']}, 负面: {overall_result['negative_count']}, 中性: {overall_result['neutral_count']}")

        summary = get_sentiment_summary("BTC", overall_result, len(analyzed_news))
        print(f"    摘要: {summary[:100]}...")

        return analyzed_news, overall_result
    except Exception as e:
        print(f"  情感分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def test_technical():
    print("\n=== 测试技术分析 ===")
    try:
        df = fetch_ohlcv("BTC", "day", limit=30)
        if df.empty:
            print("  无K线数据，跳过技术分析")
            return None

        df_with_indicators = calculate_indicators(df)
        print(f"  技术指标计算完成")
        print(f"    新增列: {[col for col in df_with_indicators.columns if col not in df.columns]}")

        technical_analysis = analyze_indicators(df_with_indicators)
        print(f"  技术分析完成")
        print(f"    趋势: {technical_analysis.get('trend', '未知')}")
        print(f"    信号: {technical_analysis.get('signal', '未知')}")

        return technical_analysis
    except Exception as e:
        print(f"  技术分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_trader_analysis():
    print("\n=== 测试交易员分析 ===")
    try:
        analysis = analyze_asset("BTC", "crypto")
        print(f"  交易员分析完成")
        print(f"    状态: {analysis.get('status', '未知')}")
        print(f"    分析时间: {analysis.get('analysis_time', '未知')}")

        # 检查关键部分
        if 'market_overview' in analysis:
            print(f"    市场概况: {analysis['market_overview'].get('summary', '无')[:80]}...")

        if 'recommendation' in analysis:
            print(f"    建议: {analysis['recommendation'].get('action', '未知')}")

        return analysis
    except Exception as e:
        print(f"  交易员分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("开始集成测试...")

    # 测试各个模块
    chart_ok = test_chart()

    news_list = test_news()

    if news_list:
        analyzed_news, overall_result = test_sentiment(news_list)

    technical_analysis = test_technical()

    trader_analysis = test_trader_analysis()

    print("\n=== 测试总结 ===")
    print(f"图表数据: {'通过' if chart_ok else '失败'}")
    print(f"新闻获取: {'通过' if news_list else '失败'}")
    print(f"技术分析: {'通过' if technical_analysis else '失败'}")
    print(f"交易员分析: {'通过' if trader_analysis else '失败'}")

    if chart_ok and news_list and technical_analysis and trader_analysis:
        print("\n✅ 所有模块测试通过！")
    else:
        print("\n⚠️ 部分模块测试失败，需要检查。")

if __name__ == "__main__":
    main()