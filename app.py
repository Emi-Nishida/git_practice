from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI
from datetime import datetime

# ローカル用に .env を読み込む
load_dotenv()

# Cloudとローカルの両対応（安全な書き方）
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# デバッグ用（Cloudログに出力される）
print("APIキーの中身:", api_key)

# OpenAIクライアントを初期化
client = OpenAI(api_key=api_key)

# 書かせたい内容のテイストを選択肢として表示する
content_kind_of = [
    "ユーモアを交えた文章",
    "中立的で客観的な文章",
    "分かりやすい、簡潔な文章",
    "親しみやすいトーンの文章",
    "専門用語をできるだけ使わない、一般読者向けの文章",
    "言葉の使い方にこだわり、正確な表現を心がけた文章",
    "シンプルかつわかりやすい文法を使った文章",
    "面白く、興味深い内容を伝える文章",
    "具体的でイメージしやすい表現を使った文章",
    "人間味のある、感情や思いを表現する文章",
    "引用や参考文献を適切に挿入した、信頼性の高い文章",
    "読み手の興味を引きつけるタイトルやサブタイトルを使った文章",
    "統計データや図表を用いたわかりやすい文章",
    "独自の見解や考え方を示した、論理的な文章",
    "問題提起から解決策までを網羅した、解説的な文章",
    "ニュース性の高い、旬なトピックを取り上げた文章",
    "エンターテイメント性のある、軽快な文章",
    "読者の関心に合わせた、専門的な内容を深く掘り下げた文章",
    "人物紹介やインタビューを取り入れた、読み物的な文章",
]

def run_gpt(content_text_to_gpt, content_kind_of_to_gpt, content_maxStr_to_gpt):
    request_to_gpt = content_text_to_gpt + " また、これを記事として読めるように、記事のタイトル、目次、内容の順番で出力してください。内容は"+ content_maxStr_to_gpt + "文字以内で出力してください。" + "また、文章は" + content_kind_of_to_gpt + "にしてください。"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": request_to_gpt},
        ],
    )

    output_content = response.choices[0].message.content.strip()
    return output_content

# 評価ボタンで記事を消えないようにする
if 'output_content_text' not in st.session_state:
    st.session_state.output_content_text = None

st.title('GPTに記事を書かせるアプリ')

tab1, tab2 = st.tabs(["新規作成", "履歴"])

# サイドバーに入力要素を配置
with st.sidebar:
    st.logo("https://streamlit.io/images/brand/streamlit-mark-color.png")
    st.header("設定")

    content_text_to_gpt = st.text_input("書かせる内容を入力してね！")
    content_kind_of_to_gpt = st.selectbox("文章の種類", options=content_kind_of)
    content_maxStr_to_gpt = str(st.slider('記事の最大文字数', 100, 1000, 300, step=100))

    with st.expander("詳細設定"):
        creativity = st.radio(
            "レベル",
            options=["低い", "普通", "**高**", ":rainbow[最高]"], 
            index=2,
            horizontal=False
        )
        theme_color = st.color_picker("テーマカラーを選んでね！", "#002CFF")
        publish_date = st.date_input(
            "公開予定日",
            value=datetime.now(),
            help="記事の公開予定日を設定"
        )

    generate_button = st.button('生成する')

# タブ1: 新規作成
with tab1:
    if generate_button and content_text_to_gpt:
        with st.spinner('記事を生成中...'):
            st.session_state.output_content_text = run_gpt(content_text_to_gpt, content_kind_of_to_gpt, content_maxStr_to_gpt)

    # 記事が生成されている場合に表示
    if st.session_state.output_content_text:
        # 記事本体を表示
        st.badge("New")
        st.markdown(st.session_state.output_content_text)
        
        # ダウンロードボタン
        st.download_button(
            label="📥 Download",
            data=st.session_state.output_content_text,
            file_name='generated_article.txt',
            mime='text/plain',
        )
        
        st.divider()
        
        # 記事の評価セクション
        st.subheader("⭐ 記事を評価して!")
        
        # 評価ボタンを追加
        with st.form("rating_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                readability = st.slider('読みやすさ', 1, 5, 3, key='readability')
            
            with col2:
                quality = st.slider('内容の質', 1, 5, 3, key='quality')
            
            with col3:
                creativity_score = st.slider('創造性', 1, 5, 3, key='creativity')
            
            # フォーム送信ボタン
            submitted = st.form_submit_button("確定しちゃうぞ!")
        
        # 評価が確定されたらメッセージ表示
        if submitted:
            st.info("📊 グラフ機能は現在開発中です。お楽しみに!")
    
    elif generate_button and not content_text_to_gpt:
        st.warning('書かせる内容を入力してね！')

# タブ2: 履歴
with tab2:
    st.info("履歴機能は年明けに向け開発中です。乞うご期待！")
