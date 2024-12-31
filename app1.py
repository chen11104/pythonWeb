import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
import plotly.express as px
import pandas as pd

def main_plotly():
    st.title("URL 文章词频分析 (Plotly)")

    # 侧边栏图表选择
    chart_type = st.sidebar.selectbox(
        "选择图表类型",
        ["柱状图", "折线图", "饼图", "散点图", "雷达图"]
    )

    url = st.text_input('请输入文章URL:', '')

    if st.button('抓取并分析'):
        if url:
            # 抓取网页内容
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()

            # 分词
            words = jieba.lcut(text)

            # 统计词频
            word_counts = Counter(words)

            # 过滤低频词
            filtered_word_counts = {word: count for word, count in word_counts.items() if count > 1}

            # 展示前20个高频词汇
            top_words = dict(word_counts.most_common(20))
            st.write("Top 20 高频词汇:")
            st.write(top_words)

            # 创建选定类型的图表
            df = pd.DataFrame(list(filtered_word_counts.items()), columns=['Word', 'Count'])

            if chart_type == "柱状图":
                fig = px.bar(df, x='Word', y='Count', title="词频柱状图")
            elif chart_type == "折线图":
                fig = px.line(df, x='Word', y='Count', title="词频折线图")
            elif chart_type == "饼图":
                fig = px.pie(df, names='Word', values='Count', title="词频饼图")
            elif chart_type == "散点图":
                fig = px.scatter(df, x='Word', y='Count', title="词频散点图")
            elif chart_type == "雷达图":
                fig = px.line_polar(df, r='Count', theta='Word', line_close=True, title="词频雷达图")

            st.plotly_chart(fig)

# 启动Plotly主函数
if __name__ == "__main__":
    main_plotly()