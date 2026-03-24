#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Flask API端点
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_endpoint(url, method="GET", data=None):
    """测试API端点"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print(f"  不支持的HTTP方法: {method}")
            return None

        print(f"  URL: {url}")
        print(f"  状态码: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  响应: {json.dumps(data, ensure_ascii=False)[:200]}...")
                return data
            except:
                print(f"  响应文本: {response.text[:200]}...")
                return response.text
        else:
            try:
                error_data = response.json()
                print(f"  错误: {error_data}")
            except:
                print(f"  错误响应: {response.text[:200]}...")
        return None

    except Exception as e:
        print(f"  请求失败: {e}")
        return None

def main():
    print("测试Flask API端点...")

    # 1. 健康检查
    print("\n1. 测试健康检查端点:")
    test_endpoint(f"{BASE_URL}/api/health")

    # 2. API状态
    print("\n2. 测试API状态端点:")
    test_endpoint(f"{BASE_URL}/api/status")

    # 3. 图表数据
    print("\n3. 测试图表数据端点:")
    chart_data = test_endpoint(f"{BASE_URL}/api/chart/BTC?timeframe=day&limit=10")

    # 4. 技术分析
    print("\n4. 测试技术分析端点:")
    test_endpoint(f"{BASE_URL}/api/technical/BTC?timeframe=day&limit=10")

    # 5. 价格信息
    print("\n5. 测试价格信息端点:")
    test_endpoint(f"{BASE_URL}/api/price/BTC")

    # 6. 新闻分析（POST请求）
    print("\n6. 测试新闻分析端点:")
    post_data = {"symbol": "BTC", "asset_type": "crypto"}
    test_endpoint(f"{BASE_URL}/analyze", method="POST", data=post_data)

    # 7. 交易员分析
    print("\n7. 测试交易员分析端点:")
    test_endpoint(f"{BASE_URL}/api/trader-analysis/BTC?asset_type=crypto")

    print("\n测试完成!")

if __name__ == "__main__":
    main()