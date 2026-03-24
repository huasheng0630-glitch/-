#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试chart_fetcher模块
"""

import sys
import os
sys.path.append('.')

from modules.chart_fetcher import ChartFetcher, fetch_ohlcv, get_current_price
from config import CRYPTOCOMPARE_API_KEY

def test_chart_fetcher():
    print("测试ChartFetcher模块...")
    print(f"API KEY配置: {'已配置' if CRYPTOCOMPARE_API_KEY else '未配置'}")

    try:
        # 创建fetcher实例
        fetcher = ChartFetcher()
        print("ChartFetcher实例创建成功")

        # 测试获取当前价格
        print("\n1. 测试获取当前价格...")
        price = fetcher.get_current_price("BTC")
        if price:
            print(f"  BTC当前价格: ${price}")
        else:
            print("  获取当前价格失败")

        # 测试获取OHLCV数据
        print("\n2. 测试获取OHLCV数据...")
        df = fetcher.fetch_ohlcv("BTC", "day", limit=10)
        if not df.empty:
            print(f"  获取到{len(df)}条K线数据")
            print(f"  列: {list(df.columns)}")
            if len(df) > 0:
                latest = df.iloc[-1]
                print(f"  最新数据: 时间={latest['time']}, 收盘价=${latest['close']}")
        else:
            print("  获取K线数据失败")

        # 测试便捷函数
        print("\n3. 测试便捷函数...")
        price2 = get_current_price("ETH")
        if price2:
            print(f"  ETH当前价格: ${price2}")

        df2 = fetch_ohlcv("ETH", "day", limit=5)
        if not df2.empty:
            print(f"  ETH K线数据: {len(df2)}条")

        print("\n测试完成!")

    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chart_fetcher()