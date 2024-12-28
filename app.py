import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
from pyecharts.charts import WordCloud, Bar, Line, Pie, Scatter, Radar, Map
from pyecharts import options as opts

# Streamlit界面设置
st.title("URL 文章词频分析")

# 侧边栏图表选择
chart_type = st.sidebar.selectbox(
    "选择图表类型",
    ["词云", "柱状图", "折线图", "饼图", "散点图", "雷达图", "地图"]
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

        # 根据选择创建不同类型的图表
        def create_chart(chart_type):
            if chart_type == "词云":
                chart = WordCloud()
                chart.add("", list(filtered_word_counts.items()), word_size_range=[20, 100])
            elif chart_type == "柱状图":
                chart = Bar()
                items = list(filtered_word_counts.items())
                chart.add_xaxis([item[0] for item in items])
                chart.add_yaxis("", [item[1] for item in items])
            elif chart_type == "折线图":
                chart = Line()
                items = list(filtered_word_counts.items())
                chart.add_xaxis([item[0] for item in items])
                chart.add_yaxis("", [item[1] for item in items])
            elif chart_type == "饼图":
                chart = Pie()
                chart.add("", list(filtered_word_counts.items()))
            elif chart_type == "散点图":
                chart = Scatter()
                items = list(filtered_word_counts.items())
                chart.add_xaxis([item[0] for item in items])
                chart.add_yaxis("", [item[1] for item in items])
            elif chart_type == "雷达图":
                chart = Radar()
                schema = [{"name": item[0], "max": max(filtered_word_counts.values())} for item in filtered_word_counts.items()]
                chart.add_schema(schema)
                chart.add("", [[value for value in filtered_word_counts.values()]])
            elif chart_type == "地图":
                chart = Map()
                chart.add("", list(filtered_word_counts.items()), "china")

            return chart

        # 创建选定类型的图表
        selected_chart = create_chart(chart_type)

        # 直接嵌入图表HTML
        st.components.v1.html(selected_chart.render_embed(), width=800, height=600)