# pages/1_フーリエ変換.py
import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt

# ---------- 共通描画関数 ----------
def _plot_basic(x, y, ylim=None):
    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=2)
    ax.set_xlim(-4, 4)
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$f(t)$")
    ax.grid(True)
    st.pyplot(fig)

# ---------- 各種描画関数 ----------
def plot_exp():
    x = np.linspace(-4, 4, 1000)
    _plot_basic(x, np.exp(-np.abs(x)))

def plot_rect():
    x = np.linspace(-4, 4, 1000)
    _plot_basic(x, np.where(np.abs(x) <= 1, 1, 0), ylim=(-0.2, 1.2))

def plot_tri():
    x = np.linspace(-4, 4, 1000)
    _plot_basic(x, np.clip(1 - np.abs(x), 0, 1), ylim=(-0.2, 1.2))

def plot_exp_pos():
    x = np.linspace(-4, 4, 1000)
    _plot_basic(x, np.exp(-x) * (x >= 0), ylim=(-0.2, 1.2))

def plot_delta():
    fig, ax = plt.subplots()
    ax.axvline(0, ymax=0.8, linewidth=2)
    ax.annotate(r"$\delta(t)$", xy=(0, 0.8), xytext=(0.1, 0.8))
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 1)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$f(t)$")
    ax.grid(True)
    st.pyplot(fig)

def plot_cos():
    x = np.linspace(-4, 4, 1000)
    _plot_basic(x, np.cos(2 * np.pi * x))

def plot_gauss():
    x = np.linspace(-4, 4, 1000)
    _plot_basic(x, np.exp(-np.pi * x**2))

def plot_step():
    x = np.linspace(-4, 4, 1000)
    _plot_basic(x, (x >= 0).astype(float), ylim=(-0.2, 1.2))

def plot_sgn():
    x = np.linspace(-4, 4, 1000)
    y = np.sign(x)
    y[y == 0] = 0
    _plot_basic(x, y, ylim=(-1.2, 1.2))

def plot_const():
    _plot_basic(np.linspace(-4, 4, 500), np.ones(500), ylim=(-0.2, 1.2))

def plot_ramp():
    x = np.linspace(-4, 4, 500)
    _plot_basic(x, np.clip(x, 0, None), ylim=(-0.5, 4))

def plot_sinc():
    x = np.linspace(-4, 4, 1000)
    _plot_basic(x, np.sinc(x), ylim=(-0.3, 1.1))

def plot_sq_per():
    x = np.linspace(-4*np.pi, 4*np.pi, 2000)
    _plot_basic(x, np.sign(np.sin(x)), ylim=(-1.2, 1.2))

def plot_saw():
    x = np.linspace(-2*np.pi, 2*np.pi, 2000)
    _plot_basic(x, (x % (2*np.pi)) - np.pi, ylim=(-3.5, 3.5))

def plot_rect_shift():
    x = np.linspace(-4, 4, 1000)
    _plot_basic(x, np.where(np.abs(x - 1) <= 1, 1, 0), ylim=(-0.2, 1.2))

plot_functions = {
    "exp": plot_exp,
    "rect": plot_rect,
    "tri": plot_tri,
    "exp_pos": plot_exp_pos,
    "delta": plot_delta,
    "cos": plot_cos,
    "gauss": plot_gauss,
    "step": plot_step,
    "sgn": plot_sgn,
    "const": plot_const,
    "ramp": plot_ramp,
    "sinc": plot_sinc,
    "sq_per": plot_sq_per,
    "saw": plot_saw,
    "rect_shift": plot_rect_shift,
}

# ---------- データ読み込み ----------
with open("data/fourier_problems.json", "r", encoding="utf-8") as f:
    problems = json.load(f)

# ---------- 優先順選択モード ----------
st.title("📘 フーリエ変換 演習問題")

sorted_problems = sorted(
    problems,
    key=lambda p: (p.get("priority", 0), -p["id"]),
    reverse=True
)
names = [f"{p['id']}: {p['title']} " + "★" * p.get("priority", 0) for p in sorted_problems]
sel = st.selectbox("問題を選択：", names, index=0)
sel_id = int(sel.split(":")[0])
q = next(p for p in problems if p["id"] == sel_id)

# ---------- 出題表示 ----------
star_str = " " + "★" * q.get("priority", 0) if q.get("priority", 0) > 0 else ""
st.markdown(f"### ❓ {q['title']}{star_str}")
st.latex(q["latex_expr"])

ptype = q.get("plot_type")
if ptype in plot_functions:
    plot_functions[ptype]()
else:
    st.warning(f"グラフ関数が未定義 (plot_type = {ptype})")

# ---------- 解答表示 ----------
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
