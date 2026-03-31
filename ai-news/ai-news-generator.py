#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻自动生成器
Daily AI News Generator for 上海第二工业大学AI素养平台
更新频率：每日一次
更新时间：每天早上9点
"""

import json
import os
from datetime import datetime
from typing import List, Dict
from mcp_matrix_batch_web_search import batch_web_search
from mcp_matrix_extract_content_from_websites import extract_content_from_websites

# 项目路径配置
PROJECT_PATH = "/workspace/ai-news/"
OUTPUT_HTML = os.path.join(PROJECT_PATH, "ai-news.html")
ARCHIVE_PATH = os.path.join(PROJECT_PATH, "archive/")

# 新闻数量配置
NEWS_COUNT = 8

# 搜索关键词配置
SEARCH_QUERIES = [
    {"query": "AI 人工智能 新闻 今日", "num_results": 10},
    {"query": "artificial intelligence news today", "num_results": 10},
    {"query": "ChatGPT GPT 大模型 发布 2026", "num_results": 8},
    {"query": "AI 创业 融资 政策 2026", "num_results": 8},
]

# 分类标签映射
CATEGORY_COLORS = {
    "AI模型": "category-model",
    "AI产业": "category-industry",
    "AI政策": "category-policy",
    "AI安全": "category-security",
    "AI活动": "category-event",
    "AI产品": "category-product"
}

def get_news_data() -> List[Dict]:
    """获取当日AI新闻数据"""
    print("正在搜索今日AI新闻...")

    results = batch_web_search(
        queries=SEARCH_QUERIES,
        display_text="搜索AI新闻"
    )

    news_items = []
    for result in results:
        if result.get('success') and result.get('formatted_content'):
            for item in result['formatted_content']:
                if len(news_items) >= NEWS_COUNT * 2:  # 预取更多以便筛选
                    break

                news_item = {
                    'title': item.get('title', ''),
                    'source': item.get('source', '未知来源'),
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'summary': item.get('snippet', '')[:200],
                    'url': item.get('link', '#'),
                    'category': categorize_news(item.get('title', '') + ' ' + item.get('snippet', ''))
                }

                # 去重检查
                if news_item['title'] and not is_duplicate(news_item, news_items):
                    news_items.append(news_item)

    # 只保留前NEWS_COUNT条
    return news_items[:NEWS_COUNT]

def categorize_news(text: str) -> str:
    """根据内容分类新闻"""
    text_lower = text.lower()

    if any(kw in text_lower for kw in ['模型', 'gpt', 'chatgpt', 'claude', 'gemini', 'llama', 'model', 'deepseek', '通通', 'kimi']):
        return "AI模型"
    elif any(kw in text_lower for kw in ['人形机器人', '量产', '万台', '宇树', 'figure', 'robot']):
        return "AI产业"
    elif any(kw in text_lower for kw in ['政策', '监管', '法规', '标准', '欧盟', '美国', '中国', 'policy', 'regulation']):
        return "AI政策"
    elif any(kw in text_lower for kw in ['安全', '伦理', '隐私', 'deepfake', '伪造', 'security', 'safety']):
        return "AI安全"
    elif any(kw in text_lower for kw in ['中关村', '论坛', '会议', '展会', 'MWC', 'conference']):
        return "AI活动"
    else:
        return "AI产品"

def is_duplicate(item: Dict, existing: List[Dict]) -> bool:
    """检查是否重复"""
    for e in existing:
        if item['title'][:30] == e['title'][:30]:
            return True
    return False

def generate_html(news_items: List[Dict]) -> str:
    """生成HTML代码"""
    today = datetime.now().strftime('%Y年%m月%d日')

    html = f'''<!-- AI新鲜事 - 自动生成于 {today} -->
<section id="ai-news" class="section">
    <div class="container">
        <h2 class="section-title">AI新鲜事</h2>

        <div class="news-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">

            <!-- 行业新闻 -->
            <div class="news-column">
                <h3 style="font-size: 20px; margin-bottom: 20px; color: #0066cc;">行业新闻</h3>
                <div class="news-list">
'''

    # 添加行业新闻
    industry_news = [n for n in news_items if n['category'] in ['AI模型', 'AI产业', 'AI产品']]
    for i, news in enumerate(industry_news[:4]):
        html += f'''                    <div class="news-item">
                        <span class="news-date">{news['date']}</span>
                        <a href="{news['url']}" class="news-link" target="_blank" title="{news['title']}">{news['title']}</a>
                    </div>
'''

    html += '''                </div>
                <a href="#" class="card-btn" style="margin-top: 15px;">浏览更多</a>
            </div>

            <!-- 政策与法规 -->
            <div class="news-column">
                <h3 style="font-size: 20px; margin-bottom: 20px; color: #ff6600;">政策与法规速递</h3>
                <div class="news-list">
'''

    # 添加政策新闻
    policy_news = [n for n in news_items if n['category'] in ['AI政策', 'AI安全']]
    for news in policy_news[:4]:
        html += f'''                    <div class="news-item">
                        <span class="news-date">{news['date']}</span>
                        <a href="{news['url']}" class="news-link" target="_blank" title="{news['title']}">{news['title']}</a>
                    </div>
'''

    html += '''                </div>
                <a href="#" class="card-btn" style="margin-top: 15px;">了解更多</a>
            </div>

        </div>

        <p style="text-align: center; margin-top: 30px; color: #999; font-size: 12px;">
            📅 每日 {datetime.now().strftime('%H:%M')} 自动更新 · 数据来源：全网AI新闻聚合
        </p>
    </div>
</section>
'''

    return html

def save_news(html: str):
    """保存新闻HTML"""
    # 确保目录存在
    os.makedirs(PROJECT_PATH, exist_ok=True)
    os.makedirs(ARCHIVE_PATH, exist_ok=True)

    # 保存今日新闻
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    # 存档
    archive_file = os.path.join(ARCHIVE_PATH, f"ai-news-{datetime.now().strftime('%Y%m%d')}.html")
    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 新闻已生成：{OUTPUT_HTML}")
    print(f"✅ 存档已保存：{archive_file}")

def main():
    """主函数"""
    print("=" * 50)
    print("🤖 AI新闻自动生成器启动")
    print(f"📅 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 目标数量：{NEWS_COUNT} 条新闻")
    print("=" * 50)

    # 获取新闻数据
    news_items = get_news_data()

    if news_items:
        # 生成HTML
        html = generate_html(news_items)

        # 保存
        save_news(html)

        print(f"\n✅ 成功生成 {len(news_items)} 条新闻！")
        print(f"📄 输出文件：{OUTPUT_HTML}")
    else:
        print("\n❌ 未能获取新闻数据，请检查网络连接。")

if __name__ == "__main__":
    main()
