#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试各个模块功能
"""

import sys
import os
import pandas as pd

# 添加当前目录到路径
sys.path.append(os.path.dirname(__file__))

def test_chart_fetcher():
    """测试K线数据获取模块"""
    print("测试 chart_fetcher 模块...")
    try:
        from modules.chart_fetcher import fetch_ohlcv, get_current_price

        # 测试获取当前价格
        print("  获取BTC当前价格...")
        price = get_current_price("BTC")
        if price:
            print(f"  [成功] BTC当前价格: ${price:.2f}")
        else:
            print("  [失败] 无法获取BTC价格")
            return False

        # 测试获取OHLCV数据
        print("  获取BTC日线数据...")
        df = fetch_ohlcv("BTC", timeframe="day", limit=10)

        if not df.empty:
            print(f"  [成功] 获取到{len(df)}条日线数据")
            print(f"     最新数据: 时间={df.iloc[-1]['time']}, 收盘价=${df.iloc[-1]['close']:.2f}")
            return True
        else:
            print("  [失败] 无法获取K线数据")
            return False

    except Exception as e:
        print(f"  [失败] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_technical_analyzer():
    """测试技术指标分析模块"""
    print("\n测试 technical_analyzer 模块...")
    try:
        from modules.technical_analyzer import calculate_indicators, analyze_indicators

        # 创建测试数据
        print("  创建测试数据...")
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'time': dates,
            'open': [100 + i * 0.5 for i in range(100)],
            'high': [105 + i * 0.5 for i in range(100)],
            'low': [95 + i * 0.5 for i in range(100)],
            'close': [100 + i for i in range(100)],  # 上升趋势
            'volume': [1000 + i * 10 for i in range(100)]
        })

        # 计算技术指标
        print("  计算技术指标...")
        df_with_indicators = calculate_indicators(df)

        # 检查是否计算了指标
        required_columns = ['MA7', 'MA25', 'MA99', 'MACD', 'RSI']
        missing_columns = [col for col in required_columns if col not in df_with_indicators.columns]

        if missing_columns:
            print(f"  [警告]  缺少指标: {missing_columns}")
            print(f"     现有列: {list(df_with_indicators.columns)}")
        else:
            print(f"  [成功] 所有技术指标计算成功")
            print(f"     MA7最新值: {df_with_indicators.iloc[-1]['MA7']:.2f}")
            print(f"     RSI最新值: {df_with_indicators.iloc[-1]['RSI']:.2f}")

        # 分析技术指标
        print("  分析技术指标...")
        analysis = analyze_indicators(df_with_indicators)

        if analysis:
            print(f"  [成功] 技术分析成功")
            print(f"     技术评分: {analysis.get('overall_technical_score', 'N/A')}")
            print(f"     趋势分析: {analysis.get('trend_analysis', {}).get('primary', 'N/A')}")
            return True
        else:
            print("  [失败] 技术分析失败")
            return False

    except Exception as e:
        print(f"  [失败] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_trader_analysis():
    """测试交易员分析模块"""
    print("\n测试 trader_analysis 模块...")
    try:
        from modules.trader_analysis import analyze_asset

        # 注意：这个测试可能需要API调用，可能会失败
        print("  分析BTC资产...")

        # 由于可能需要API，我们只测试导入和基本功能
        from modules.trader_analysis import TraderAnalyzer
        analyzer = TraderAnalyzer()

        print(f"  [成功] 交易员分析器创建成功")
        print(f"     名称: {analyzer.analyzer_name}")
        print(f"     经验: {analyzer.experience_years}年")
        print(f"     胜率: {analyzer.win_rate}%")

        # 测试空分析（不调用API）
        print("  测试空分析生成...")
        empty_result = analyzer._empty_analysis()
        if empty_result:
            print(f"  [成功] 空分析生成成功")
            return True
        else:
            print("  [失败] 空分析生成失败")
            return False

    except Exception as e:
        print(f"  [失败] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_news_modules():
    """测试新闻相关模块"""
    print("\n测试新闻相关模块...")
    try:
        from modules.news_fetcher import fetch_news
        from modules.sentiment_analyzer import analyze_sentiment

        # 测试情感分析
        print("  测试情感分析...")
        test_text = "Bitcoin reaches new all-time high as institutional adoption grows."
        sentiment = analyze_sentiment(test_text)

        if sentiment:
            print(f"  [成功] 情感分析成功")
            print(f"     得分: {sentiment.get('score', 'N/A')}")
            print(f"     标签: {sentiment.get('chinese_label', 'N/A')}")

            # 测试新闻获取（可能返回空列表）
            print("  测试新闻获取...")
            news_list = fetch_news("BTC", asset_type="crypto", limit=2)
            print(f"     获取到{len(news_list)}条新闻")
            return True
        else:
            print("  [失败] 情感分析失败")
            return False

    except Exception as e:
        print(f"  [失败] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("交易分析系统模块测试")
    print("=" * 60)

    results = []

    # 测试各个模块
    results.append(("chart_fetcher", test_chart_fetcher()))
    results.append(("technical_analyzer", test_technical_analyzer()))
    results.append(("trader_analysis", test_trader_analysis()))
    results.append(("news_modules", test_news_modules()))

    # 打印测试结果
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)

    passed = 0
    total = len(results)

    for module_name, success in results:
        status = "[成功] 通过" if success else "[失败] 失败"
        print(f"{module_name:20} {status}")
        if success:
            passed += 1

    print(f"\n总计: {passed}/{total} 个测试通过 ({passed/total*100:.1f}%)")

    if passed == total:
        print("[庆祝] 所有模块测试通过！")
        return 0
    else:
        print("[警告]  部分模块测试失败，请检查错误信息")
        return 1

if __name__ == "__main__":
    sys.exit(main())