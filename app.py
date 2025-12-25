import streamlit as st
import jieba
from collections import Counter
import re

# 设置页面标题和布局
st.set_page_config(page_title="文本分析工具", page_icon="📝", layout="wide")

# 标题和说明
st.title("📝 文本分析Web应用")
st.markdown("---")

# 文本输入区域
text = st.text_area("请输入需要分析的文本内容", height=200)

# 当用户输入文本后执行分析
if text:
    # 1. 基础统计：字符数、字数（中文）、单词数（英文）
    # 去除空格和换行的字符数
    char_count = len(re.sub(r'\s', '', text))
    # 中文分词后的词数
    words = jieba.lcut(text)
    word_count = len(words)
    # 英文单词数（简单匹配）
    en_words = re.findall(r'[a-zA-Z]+', text)
    en_word_count = len(en_words)

    # 分栏显示基础统计
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("纯字符数（不含空格换行）", char_count)
    with col2:
        st.metric("中文分词数量", word_count)
    with col3:
        st.metric("英文单词数量", en_word_count)

    st.markdown("---")

    # 2. 高频关键词提取（排除停用词）
    st.subheader("高频关键词TOP10")
    # 简单停用词列表（可扩展）
    stop_words = {'的', '了', '是', '我', '你', '他', '她', '它', '们', '在', '有', '就', '不', '和', '也', '这', '那', '啊', '呀', '哦', '嗯', '哈', '吧', '吗', '呢', '！', '？', '。', '，', '、', '：', '；', '“', '”', '‘', '’', '（', '）', '【', '】', '…', '—', ' ', '\n', '\t'}
    # 过滤停用词
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    # 统计词频
    word_freq = Counter(filtered_words)
    top10_words = word_freq.most_common(10)

    # 显示关键词
    for word, count in top10_words:
        st.write(f"**{word}**：{count}次")

    st.markdown("---")

    # 3. 简单情感倾向（基于关键词匹配，仅作演示）
    st.subheader("情感倾向分析（简易版）")
    positive_words = {'好', '棒', '优秀', '开心', '快乐', '幸福', '满意', '喜欢', '精彩', '完美'}
    negative_words = {'坏', '差', '糟糕', '难过', '伤心', '生气', '不满', '讨厌', '无聊', '失望'}

    positive_count = sum([1 for word in words if word in positive_words])
    negative_count = sum([1 for word in words if word in negative_words])

    if positive_count > negative_count:
        st.success("情感倾向：积极 😊")
    elif negative_count > positive_count:
        st.error("情感倾向：消极 😞")
    else:
        st.info("情感倾向：中性 😐")
else:
    st.info("请输入文本内容以进行分析~")
