# pages/4_微分積分学.py
import streamlit as st
import json

# ---------- データ読み込み ----------
with open("data/calculus_problems.json", "r", encoding="utf-8") as f:
    problems = json.load(f)

# ---------- カテゴリー分類 ----------
category_names = {
    "multiple_integral": "重積分（累次・置換）",
    "area_volume": "面積、体積、曲面積",
    "extrema": "極値を求める問題",
    "constrained_extrema": "条件付きの極値を求める問題"
}

categories = list(category_names.keys())
selected_category_key = st.selectbox("テーマを選択：", categories, format_func=lambda k: category_names[k])

# ---------- 該当カテゴリの問題リスト ----------
filtered = [p for p in problems if isinstance(p, dict) and p.get("category") == selected_category_key]

if not filtered:
    st.warning("このカテゴリにはまだ問題が登録されていません。")
    st.stop()

sorted_problems = sorted(
    filtered,
    key=lambda p: (p.get("priority", 0), -p["id"]),
    reverse=True
)
names = [f"{p['id']}: {p['title']} " + "★" * p.get("priority", 0) for p in sorted_problems]
sel = st.selectbox("問題を選択：", names, index=0)
sel_id = int(sel.split(":")[0])
q = next(p for p in filtered if p["id"] == sel_id)

# ---------- 出題 ----------
st.title("📘 微分積分学 演習問題")
star_str = " " + "★" * q.get("priority", 0) if q.get("priority", 0) > 0 else ""
st.markdown(f"### ❓ {q['title']}{star_str}")
st.latex(q["latex_expr"])

# ---------- 解答・解説 ----------
with st.expander("💡 解答 / 解説"):
    st.markdown("#### ✅ 結論")
    st.latex(q["answer_expr"])

    st.markdown("#### 🧠 導出ステップ")
    for step in q["steps_jp"]:
        st.markdown(step["explain"], unsafe_allow_html=False)
        st.latex(step["latex"])

    st.markdown("#### 📌 ポイント")
    for pt in q["points"]:
        st.markdown(f"- {pt}")