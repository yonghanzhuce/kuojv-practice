import streamlit as st
from openai import OpenAI
import time, re


apikey = "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"
apikey = apikey.replace('\u200b', '')
client = OpenAI(api_key=apikey)

# Streamlit 页面布局
st.title('扩句练习系统')

# 初始化存储句子和扩句案例的变量
if 'sentences' not in st.session_state:
    st.session_state['sentences'] = []
if 'sentences_generate_complete' not in st.session_state:
    st.session_state['sentences_generate_complete'] = False
if 'expanded_sentences' not in st.session_state:
    st.session_state['expanded_sentences'] = []
if 'expanded_sentences_not_generated' not in st.session_state:
    st.session_state['expanded_sentences_not_generated'] = True
if 'expanded_sentences_generate_complete' not in st.session_state:
    st.session_state['expanded_sentences_generate_complete'] = False

# 用户点击“生成练习”按钮后的逻辑
if st.button('生成练习'):
    # 使用 OpenAI API 生成五个简短的句子
    prompt = "请提供两个简短的句子，用于扩句练习。"

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )
    # 解析生成的句子
    print(chat_completion)
    print(chat_completion.choices[0].message.content)
    sentences = chat_completion.choices[0].message.content.strip().split('\n')

    # sentences = [resp['text'].strip() for resp in response['choices']]
    sentences = [sentence for sentence in sentences if sentence]
    sentences = [re.sub(r'^\d+\.\s*', '', sentence) for sentence in sentences]
    st.session_state['sentences'] = sentences
    st.session_state['sentences_generate_complete'] = True


# 显示简短句子和输入框用于用户输入他们的扩句答案
for i, sentence in enumerate(st.session_state['sentences'], 1):
    user_input = st.session_state.get(f"user_exp_{i}", "")  # 获取用户输入的答案
    st.text_input(f"句子 {i}", value=sentence, disabled=True, key=f"sent_{i}")
    st.text_area(f"你的扩句答案", key=f"user_exp_{i}", value=user_input)

if st.session_state['sentences_generate_complete'] and st.session_state['expanded_sentences_not_generated']:
    st.session_state['expanded_sentences_not_generated'] = False
    print(st.session_state['sentences'])
    for i, sentence in enumerate(st.session_state['sentences'], 1):
        print("Start Next")
        time.sleep(20)
        # 生成扩句案例
        prompt = f"请帮我扩展以下句子，并赋予它更多情感色彩：\n{sentence}\n"
        print("promot:", prompt)
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            
        )
        print("response:", response)
        expanded_sentence = response.choices[0].message.content.strip()
        st.session_state['expanded_sentences'].append(expanded_sentence)
    print("Process Complete")
    st.session_state['expanded_sentences_generate_complete'] = True

# 用户点击“显示答案”按钮后的逻辑
if st.session_state['expanded_sentences_generate_complete']:
    if st.button('显示答案'):

        for i, sentence in enumerate(st.session_state['sentences'], 1):
            st.text_input(f"句子 {i}", value=sentence, disabled=True)
            user_input = st.session_state.get(f"user_exp_{i}", "")  # 获取用户输入的答案
            # 你可以在这里添加逻辑来处理或显示用户的输入
            st.text_area(f"你的扩句答案", value=user_input)

            expanded_sentence = st.session_state['expanded_sentences'][i - 1]
            st.text_area(f"扩句案例", value=expanded_sentence, height=150, disabled=True)
