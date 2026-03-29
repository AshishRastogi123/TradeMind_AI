import streamlit as st
import asyncio
import math
from multi_agent_system import MultiAgentSystem
from utils import Recommendation

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI for Indian Investor - TradeMind AI",
    page_icon="🇮🇳📈",
    layout="wide",
)

# ---------------- STYLES ----------------
st.markdown("""
<style>
.metric-card {background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 1rem 0;}
.strong-buy {border-left: 6px solid #10B981;}
.buy {border-left: 6px solid #059669;}
.hold {border-left: 6px solid #F59E0B;}
.sell {border-left: 6px solid #EF4444;}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
def sidebar():
    st.sidebar.header("🔧 Configuration")
    groq_key = st.sidebar.text_input("GROQ API Key", type="password")
    portfolio = st.sidebar.text_area(
        "Portfolio (comma separated NSE symbols)",
        placeholder="RELIANCE.NS, TCS.NS"
    )
    analyze_btn = st.sidebar.button("🚀 Run Multi-Agent Analysis")
    hindi_toggle = st.sidebar.toggle("हिंदी व्याख्या (Hindi Explanation)", value=False)

    return groq_key, portfolio, analyze_btn, hindi_toggle


# ---------------- SAFE PRICE ----------------
def safe_price(val):
    try:
        if val is None:
            return None
        val = float(val)
        if math.isnan(val):
            return None
        return val
    except:
        return None


# ---------------- DISPLAY CARD ----------------
def display_rec_card(rec: Recommendation, hindi: bool):
    action_class = f"metric-card {'strong-buy' if 'STRONG' in rec.action else rec.action.lower().replace(' ', '-')}"
    color_emoji = "🟢" if 'BUY' in rec.action else "🟡" if rec.action == 'HOLD' else "🔴"

    with st.container():
        col1, col2, col3 = st.columns([1.5, 2, 3])

        # ACTION
        with col1:
            st.markdown(
                f'<div class="{action_class}"><h2>{color_emoji} {rec.action}</h2></div>',
                unsafe_allow_html=True
            )

        # CONFIDENCE
        with col2:
            st.metric("Confidence", f"{rec.confidence}%")
            st.progress(rec.confidence / 100)

        # PRICE
        with col3:
            entry = safe_price(rec.entry)
            target = safe_price(rec.target)
            stop_loss = safe_price(rec.stop_loss)

            st.markdown("### 💰 Price Levels")
            st.markdown(f"**Entry:** ₹{entry:.0f}" if entry is not None else "**Entry:** N/A")
            st.markdown(f"**Target:** ₹{target:.0f}" if target is not None else "**Target:** N/A")
            st.markdown(f"**Stop Loss:** ₹{stop_loss:.0f}" if stop_loss is not None else "**Stop Loss:** N/A")

        # REASONS
        with st.expander("Reasons"):
            if rec.reason:
                for r in rec.reason:
                    st.markdown(f"• {r}")
            else:
                st.write("No reasoning available")

        # HINDI
        if hindi:
            st.markdown("### हिंदी में")
            st.info("AI explanation coming soon...")


# ---------------- HEADER ----------------
st.title("🇮🇳 TradeMind AI")
st.subheader("Multi-Agent Stock Decision Engine")

# ---------------- INPUT ----------------
groq_key, portfolio_str, analyze, hindi = sidebar()

# ---------------- RUN ANALYSIS ----------------
if analyze and groq_key:
    with st.spinner("Running AI agents..."):
        system = MultiAgentSystem(groq_key)

        recs = asyncio.run(system.analyze())
        print("FINAL RECS:", recs)

        st.session_state.recs = recs if recs else []
        st.session_state.json = system.format_recs_json(recs) if recs else "[]"

    st.success("✅ Analysis Complete")
    st.rerun()


# ---------------- DISPLAY ----------------
if st.session_state.get("recs") is not None:
    recs = st.session_state.recs

    if len(recs) == 0:
        st.warning("⚠️ No trading opportunities found")
    else:
        st.markdown("## 🎯 Actionable Recommendations")

        num_cols = min(3, len(recs))
        cols = st.columns(num_cols)

        for i, rec in enumerate(recs):
            with cols[i % num_cols]:
                display_rec_card(rec, hindi)

        st.download_button(
            "📥 Download JSON",
            st.session_state.json,
            "recommendations.json"
        )

else:
    st.info("👆 Enter GROQ key and click Run Analysis")