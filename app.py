import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Writing Tool",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ 設定")
    api_key = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Google AI Studio から取得したAPIキーを入力してください",
    )
    model_name = st.selectbox(
        "モデル",
        ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        help="速度重視: Flash / 高品質: Pro",
    )
    if api_key:
        genai.configure(api_key=api_key)
        st.success("APIキー設定済み ✓")
    else:
        st.warning("APIキーを入力してください")

    st.divider()
    st.caption("✍️ AI Writing Tool")
    st.caption("Powered by Google Gemini")


# --- Helper ---
def generate(prompt: str) -> str:
    if not api_key:
        st.error("サイドバーにAPIキーを設定してください")
        return ""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        return ""


def result_area(content: str, filename: str, mime: str = "text/plain"):
    st.divider()
    st.markdown(content)
    st.download_button("📥 ダウンロード", content, file_name=filename, mime=mime)


# --- Main ---
st.title("✍️ AI Writing Tool")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 ブログ記事",
    "📧 メール返信",
    "📋 文章要約",
    "📱 SNS投稿",
    "🔍 文章校正",
    "💡 タイトル生成",
])


# ── Tab 1: Blog Writer ────────────────────────────────────────────────────────
with tab1:
    st.header("📝 ブログ記事執筆")
    st.caption("テーマを入力するだけで完成度の高いブログ記事を生成します")

    col1, col2 = st.columns([2, 1])
    with col1:
        blog_topic = st.text_area(
            "記事のテーマ・キーワード",
            placeholder="例: Pythonで始める機械学習入門",
            height=80,
        )
        blog_outline = st.text_area(
            "含めたい内容・ポイント（任意）",
            placeholder="例: 環境構築、基本的なライブラリ、サンプルコード",
            height=80,
        )
    with col2:
        blog_style = st.selectbox(
            "文体", ["わかりやすく・親しみやすい", "専門的・詳細", "カジュアル・フランク", "フォーマル"]
        )
        blog_audience = st.selectbox(
            "対象読者", ["初心者向け", "中級者向け", "上級者向け", "一般向け"]
        )
        blog_length = st.selectbox(
            "記事の長さ", ["短め（500字程度）", "標準（1000〜1500字）", "長め（2000字以上）"]
        )
        blog_lang = st.selectbox("言語", ["日本語", "English"], key="blog_lang")

    if st.button("記事を生成", type="primary", key="blog_btn"):
        if not blog_topic:
            st.warning("テーマを入力してください")
        else:
            length_map = {
                "短め（500字程度）": "約500文字",
                "標準（1000〜1500字）": "約1000〜1500文字",
                "長め（2000字以上）": "2000文字以上",
            }
            lang_note = "日本語で書いてください。" if blog_lang == "日本語" else "Please write in English."
            prompt = f"""あなたはプロのブログライターです。以下の条件でブログ記事を執筆してください。

テーマ: {blog_topic}
{"含めたい内容: " + blog_outline if blog_outline else ""}
文体: {blog_style}
対象読者: {blog_audience}
文字数: {length_map[blog_length]}
{lang_note}

記事には適切な見出し（H2, H3）を含め、読みやすい構成にしてください。Markdown形式で出力してください。"""
            with st.spinner("記事を生成中..."):
                result = generate(prompt)
            if result:
                result_area(result, "blog_article.md", "text/markdown")


# ── Tab 2: Email Reply ────────────────────────────────────────────────────────
with tab2:
    st.header("📧 メール返信文生成")
    st.caption("受信したメールを貼り付けると、適切な返信文を生成します")

    original_email = st.text_area(
        "元のメール本文",
        placeholder="受信したメールの内容をここに貼り付けてください...",
        height=200,
    )
    col1, col2 = st.columns(2)
    with col1:
        reply_intent = st.text_area(
            "返信の意図・ポイント",
            placeholder="例: 承諾する、来週水曜に打ち合わせを設定したい",
            height=100,
        )
        reply_tone = st.selectbox(
            "文体", ["丁寧・ビジネス", "フレンドリー", "簡潔・シンプル", "フォーマル"]
        )
    with col2:
        sender_name = st.text_input("送信者名（任意）", placeholder="例: 山田太郎")
        my_name = st.text_input("自分の名前（任意）", placeholder="例: 鈴木花子")
        reply_lang = st.selectbox("言語", ["日本語", "English"], key="reply_lang")

    if st.button("返信文を生成", type="primary", key="email_btn"):
        if not original_email:
            st.warning("元のメール本文を入力してください")
        else:
            lang_note = "日本語で書いてください。" if reply_lang == "日本語" else "Please write in English."
            prompt = f"""あなたはプロのビジネスライターです。以下のメールへの返信文を作成してください。

【受信メール】
{original_email}

{"【送信者名】" + sender_name if sender_name else ""}
{"【自分の名前】" + my_name if my_name else ""}
【返信の意図・ポイント】{reply_intent or "適切に返信する"}
【文体】{reply_tone}
{lang_note}

件名と本文を含めて返信メールを作成してください。"""
            with st.spinner("返信文を生成中..."):
                result = generate(prompt)
            if result:
                st.divider()
                st.text_area("生成された返信文", result, height=300)
                st.download_button("📥 ダウンロード", result, file_name="email_reply.txt")


# ── Tab 3: Summarizer ─────────────────────────────────────────────────────────
with tab3:
    st.header("📋 文章要約")
    st.caption("長い文章を簡潔にまとめます")

    text_to_summarize = st.text_area(
        "要約したい文章",
        placeholder="ここに要約したい文章を貼り付けてください...",
        height=250,
    )
    col1, col2 = st.columns(2)
    with col1:
        summary_format = st.selectbox(
            "要約形式", ["箇条書き", "段落（文章）", "一文要約", "見出し付き要約"]
        )
        summary_length = st.selectbox(
            "詳細度", ["簡潔（重要点のみ）", "標準", "詳細"]
        )
    with col2:
        summary_focus = st.text_input(
            "重視するポイント（任意）",
            placeholder="例: 数値データ、結論、アクションアイテム",
        )
        summary_lang = st.selectbox(
            "出力言語", ["元の言語のまま", "日本語", "English"]
        )

    if st.button("要約を生成", type="primary", key="summary_btn"):
        if not text_to_summarize:
            st.warning("要約したい文章を入力してください")
        else:
            format_map = {
                "箇条書き": "箇条書き（・）形式",
                "段落（文章）": "自然な文章の段落形式",
                "一文要約": "一文で簡潔に",
                "見出し付き要約": "見出し（##）付きの構造化形式",
            }
            length_map = {
                "簡潔（重要点のみ）": "最も重要な点のみ（3〜5点）",
                "標準": "主要なポイントをバランスよく",
                "詳細": "重要な詳細も含めて網羅的に",
            }
            lang_map = {
                "元の言語のまま": "入力テキストと同じ言語で出力してください。",
                "日本語": "日本語で出力してください。",
                "English": "Please output in English.",
            }
            prompt = f"""以下の文章を要約してください。

【文章】
{text_to_summarize}

【要約形式】{format_map[summary_format]}
【詳細度】{length_map[summary_length]}
{"【重視するポイント】" + summary_focus if summary_focus else ""}
{lang_map[summary_lang]}"""
            with st.spinner("要約中..."):
                result = generate(prompt)
            if result:
                result_area(result, "summary.txt")


# ── Tab 4: SNS Posts ──────────────────────────────────────────────────────────
with tab4:
    st.header("📱 SNS投稿文生成")
    st.caption("各プラットフォームに最適化した投稿文を3パターン生成します")

    col1, col2 = st.columns([2, 1])
    with col1:
        sns_topic = st.text_area(
            "投稿したい内容・テーマ",
            placeholder="例: 新しいカフェに行った感想、新製品のPR、技術記事のシェア",
            height=120,
        )
    with col2:
        platform = st.selectbox(
            "プラットフォーム", ["X (Twitter)", "Instagram", "LinkedIn", "Facebook", "note"]
        )
        sns_tone = st.selectbox(
            "トーン", ["カジュアル・親しみやすい", "フォーマル・プロフェッショナル", "ユーモア・面白い", "感情的・共感"]
        )
        include_hashtags = st.checkbox("ハッシュタグを含める", value=True)
        sns_lang = st.selectbox("言語", ["日本語", "English"], key="sns_lang")

    if st.button("投稿文を生成", type="primary", key="sns_btn"):
        if not sns_topic:
            st.warning("投稿したい内容を入力してください")
        else:
            platform_notes = {
                "X (Twitter)": "日本語140文字以内に収めてください。",
                "Instagram": "絵文字を効果的に使い、改行を活用してください。",
                "LinkedIn": "プロフェッショナルな文体で、インサイトを提供する内容にしてください。",
                "Facebook": "読みやすい長さで、エンゲージメントを促す内容にしてください。",
                "note": "読者を引き込むリード文を作成してください。",
            }
            lang_note = "日本語で書いてください。" if sns_lang == "日本語" else "Please write in English."
            hashtag_note = "適切なハッシュタグを3〜5個含めてください。" if include_hashtags else "ハッシュタグは不要です。"
            prompt = f"""あなたはSNSマーケティングの専門家です。以下の条件でSNS投稿文を3パターン生成してください。

内容・テーマ: {sns_topic}
プラットフォーム: {platform}
トーン: {sns_tone}
ハッシュタグ: {hashtag_note}
{lang_note}

プラットフォーム固有のルール: {platform_notes[platform]}

各パターンに番号と簡単なコンセプト説明を付けてください。"""
            with st.spinner("投稿文を生成中..."):
                result = generate(prompt)
            if result:
                result_area(result, "sns_posts.txt")


# ── Tab 5: Proofreading ───────────────────────────────────────────────────────
with tab5:
    st.header("🔍 文章校正・改善")
    st.caption("文章の誤りを修正し、より読みやすい文章に改善します")

    text_to_proofread = st.text_area(
        "校正したい文章",
        placeholder="ここに校正したい文章を入力してください...",
        height=200,
    )
    col1, col2 = st.columns(2)
    with col1:
        proofread_focus = st.multiselect(
            "校正の観点",
            ["誤字脱字・文法", "文章の流れ・読みやすさ", "表現の明確さ", "敬語・丁寧語", "簡潔さ"],
            default=["誤字脱字・文法", "文章の流れ・読みやすさ"],
        )
    with col2:
        output_style = st.radio(
            "出力スタイル", ["修正後の文章のみ", "修正箇所の説明付き"]
        )
        proofread_lang = st.selectbox("言語", ["日本語", "English"], key="proofread_lang")

    if st.button("校正する", type="primary", key="proofread_btn"):
        if not text_to_proofread:
            st.warning("校正したい文章を入力してください")
        else:
            focus_str = "、".join(proofread_focus) if proofread_focus else "総合的な校正"
            lang_note = "日本語で出力してください。" if proofread_lang == "日本語" else "Please output in English."
            if output_style == "修正後の文章のみ":
                prompt = f"""以下の文章を校正・改善してください。

【校正の観点】{focus_str}

【元の文章】
{text_to_proofread}

修正後の文章のみを出力してください。{lang_note}"""
            else:
                prompt = f"""以下の文章を校正・改善してください。

【校正の観点】{focus_str}

【元の文章】
{text_to_proofread}

以下の形式で出力してください：
## 修正箇所と理由
（箇条書きで各修正点を説明）

## 修正後の文章
（改善した文章全文）

{lang_note}"""
            with st.spinner("校正中..."):
                result = generate(prompt)
            if result:
                result_area(result, "proofread_result.txt")


# ── Tab 6: Title Generator ────────────────────────────────────────────────────
with tab6:
    st.header("💡 タイトル・見出し生成")
    st.caption("記事やコンテンツに最適なタイトルを複数パターン生成します")

    col1, col2 = st.columns([2, 1])
    with col1:
        title_content = st.text_area(
            "記事の内容・概要",
            placeholder="例: Pythonを使った機械学習の入門記事。scikit-learnで分類問題を解く方法を解説する初心者向けの記事。",
            height=130,
        )
    with col2:
        title_style = st.selectbox(
            "スタイル",
            ["SEO重視・検索されやすい", "クリック率重視・興味を引く", "シンプル・わかりやすい", "専門的・権威ある"],
        )
        title_count = st.slider("生成するタイトル数", 3, 10, 5)
        content_type = st.selectbox(
            "コンテンツの種類", ["ブログ記事", "SNS投稿", "メールの件名", "動画タイトル", "プレゼン"]
        )
        title_lang = st.selectbox("言語", ["日本語", "English"], key="title_lang")

    if st.button("タイトルを生成", type="primary", key="title_btn"):
        if not title_content:
            st.warning("記事の内容・概要を入力してください")
        else:
            lang_note = "日本語で生成してください。" if title_lang == "日本語" else "Please generate in English."
            prompt = f"""あなたはコピーライティングの専門家です。以下の内容に最適なタイトルを{title_count}個生成してください。

【内容・概要】{title_content}
【スタイル】{title_style}
【コンテンツの種類】{content_type}
{lang_note}

番号付きリストで出力し、各タイトルに一言コメント（なぜ効果的か）を添えてください。"""
            with st.spinner("タイトルを生成中..."):
                result = generate(prompt)
            if result:
                result_area(result, "titles.txt")
