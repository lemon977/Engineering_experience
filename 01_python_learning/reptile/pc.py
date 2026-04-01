#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度爬虫 - 渐进学习版 (Step by Step)
====================================

学习目标：
1. 先理解最基本的请求+解析流程
2. 再学习添加异常处理
3. 然后学习数据存储
4. 最后学习简单优化

当前阶段：第1阶段 - 最基础版本
"""

import requests
from bs4 import BeautifulSoup
import time


# ========== 第1步：最简单的爬取 ==========

def simple_crawl():
    """
    最基础版本：请求网页 + 打印标题
    """
    # 1. 目标网址
    url = "https://www.baidu.com"
    
    # 2. 告诉服务器"我是浏览器"（不加这个可能被拒绝）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 3. 发送请求（就像你在浏览器输入网址）
    print("正在请求百度首页...")
    response = requests.get(url, headers=headers, timeout=10)
    
    # 4. 检查是否成功（200表示成功）
    if response.status_code == 200:
        print(f"✅ 请求成功！状态码：{response.status_code}")
        
        # 5. 设置编码（防止中文乱码）
        response.encoding = 'utf-8'
        
        # 6. 用BeautifulSoup解析HTML（就像浏览器渲染页面）
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 7. 提取标题（<title>标签里的内容）
        title = soup.title.string if soup.title else "没有标题"
        print(f"📄 网页标题：{title}")
        
        # 8. 提取所有链接（<a>标签）
        links = soup.find_all('a', href=True)
        print(f"🔗 找到 {len(links)} 个链接")
        
        # 打印前3个链接看看
        for i, link in enumerate(links[:3]):
            print(f"  链接{i+1}：{link.get('href')} -> {link.get_text(strip=True)[:20]}")
    
    else:
        print(f"❌ 请求失败，状态码：{response.status_code}")


# ========== 第2步：添加异常处理（让程序更稳定） ==========

def safe_crawl():
    """
    改进版：添加try-except，防止程序崩溃
    """
    url = "https://www.baidu.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        # 添加延时，不要请求太快（礼貌爬取）
        print("等待2秒...")
        time.sleep(2)
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 如果状态码不是200，会抛出异常
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取信息
        result = {
            'url': url,
            'title': soup.title.string if soup.title else '无标题',
            'links_count': len(soup.find_all('a', href=True))
        }
        
        print("✅ 爬取成功！")
        print(f"结果：{result}")
        return result
        
    except requests.exceptions.Timeout:
        print("❌ 错误：请求超时（网络太慢或对方无响应）")
    except requests.exceptions.ConnectionError:
        print("❌ 错误：连接失败（检查网络或URL是否正确）")
    except requests.exceptions.HTTPError as e:
        print(f"❌ 错误：HTTP错误 {e.response.status_code}")
    except Exception as e:
        print(f"❌ 未知错误：{str(e)}")
    
    return None  # 出错时返回None


# ========== 第3步：保存数据到文件 ==========

import json

def crawl_and_save():
    """
    进阶版：把爬取的数据保存到JSON文件
    """
    # 先爬取
    data = safe_crawl()
    
    if data:
        # 添加时间戳
        data['crawl_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存到文件（JSON格式，方便后续使用）
        filename = "baidu_data.json"
        with open(filename, 'w', encoding='utf-8') as f:
            # ensure_ascii=False 保证中文正常显示
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 数据已保存到：{filename}")


# ========== 第4步：函数封装，方便复用 ==========

def crawl_page(url, delay=2):
    """
    通用爬取函数：可以爬任何网页
    
    参数：
        url: 要爬的网址
        delay: 请求前等待几秒（默认2秒）
    
    返回：
        dict: 包含标题、链接数等信息
    """
    print(f"\n🚀 开始爬取：{url}")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        # 礼貌等待
        time.sleep(delay)
        
        # 请求
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # 解析
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取数据
        result = {
            'url': url,
            'title': soup.title.string.strip() if soup.title else '无标题',
            'status_code': response.status_code,
            'html_length': len(response.text),  # HTML代码长度
            'links': []
        }
        
        # 提取前5个链接（过滤掉JavaScript链接）
        for link in soup.find_all('a', href=True)[:5]:
            href = link['href']
            # 只保留http链接（跳过javascript:;等）
            if href.startswith('http'):
                result['links'].append({
                    'text': link.get_text(strip=True)[:30],  # 只取前30字
                    'url': href[:80]  # 只取前80字符
                })
        
        print(f"✅ 成功：{result['title']}")
        return result
        
    except Exception as e:
        print(f"❌ 失败：{str(e)}")
        return None


def batch_crawl():
    """
    批量爬取示例：一次爬多个页面
    """
    # 要爬的网址列表
    urls = [
        "https://www.baidu.com",
        "https://news.baidu.com",  # 百度新闻
        "https://map.baidu.com",   # 百度地图
    ]
    
    all_results = []
    
    for url in urls:
        result = crawl_page(url, delay=3)  # 每页等3秒
        if result:
            all_results.append(result)
    
    # 批量保存
    with open("batch_results.json", 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 总计爬取 {len(all_results)} 个页面，数据已保存")


# ========== 主程序入口 ==========

if __name__ == "__main__":
    print("=" * 50)
    print("百度爬虫 - 渐进学习版")
    print("=" * 50)
    
    # 选择要运行的模式（取消注释你想试的）
    
    # 模式1：最基础（推荐先运行这个）
    simple_crawl()
    
    # 模式2：带异常处理
    # safe_crawl()
    
    # 模式3：保存到文件
    #crawl_and_save()
    
    # 模式4：通用函数（推荐掌握这个）
    #crawl_page("https://www.baidu.com")
    
    # 模式5：批量爬取（注意：不要一次爬太多！）
    # batch_crawl()
    
    print("\n" + "=" * 50)
    print("运行完成！查看上面的输出结果")
    print("=" * 50)