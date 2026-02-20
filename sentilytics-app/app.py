
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Sentilytics - Real-Time Sentiment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(45deg, #FF4B4B, #FF914D);
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .splash-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 80vh;
        text-align: center;
        animation: fadeIn 2s;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .university-title {
        font-size: 3em;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 0.2em;
        text-shadow: 2px 2px 4px #000000;
    }
    .dept-title {
        font-size: 2em;
        color: #CCCCCC;
        margin-bottom: 2em;
    }
    .developer-name {
        font-size: 1.5em;
        font-weight: bold;
        color: #FF4B4B;
        position: absolute;
        top: 20px;
        left: 20px;
    }
    .developer-role {
        font-size: 0.8em;
        color: #AAAAAA;
    }
    .ai-intro {
        margin-top: 50px;
        font-style: italic;
        color: #888888;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

# Theme CSS Injection
def inject_theme_css(theme):
    if theme == "Light":
        st.markdown("""
        <style>
            .stApp {
                background-color: #f8fafc;
                color: #1e293b;
            }
            .sidebar .sidebar-content {
                background-image: linear-gradient(#ffffff, #ffffff);
                color: #1e293b;
            }
            .metric-card {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #e2e8f0;
            }
            h1, h2, h3, p, span, label {
                color: #1e293b !important;
            }
            .stMarkdown div p {
                color: #64748b !important;
            }
            .university-title {
                color: #1e293b !important;
            }
            .dept-title {
                color: #64748b !important;
            }
            .ai-intro p {
                color: #64748b !important;
            }
        </style>
        """, unsafe_allow_html=True)

# Initialize session state for splash screen
if 'show_splash' not in st.session_state:
    st.session_state.show_splash = True

def main():
    if st.session_state.show_splash:
        show_splash_screen()
    else:
        show_dashboard()

def show_splash_screen():
    # University Branding
    st.markdown('<div class="splash-container">', unsafe_allow_html=True)

    # Developer Name on Top Right
    col1, col2 = st.columns([4, 1])
    with col2:
        st.markdown("""
        <div style="text-align: right;">
            <div style="font-size: 1.2em; font-weight: bold; color: #FF4B4B;">Saira Alvi</div>
            <div style="font-size: 0.9em; color: #AAAAAA;">Web Developer</div>
        </div>
        """, unsafe_allow_html=True)

    # Main Center Content
    st.markdown("""
    <div style="margin-top: 100px;">
        <div class="university-title">University of Layyah</div>
        <div class="dept-title">Department of Computer Science</div>
    </div>
    """, unsafe_allow_html=True)

    # Proceed Button
    _, col_center, _ = st.columns([2, 2, 2])
    with col_center:
        if st.button("Enter Dashboard 🚀"):
            st.session_state.show_splash = False
            st.rerun()

    # AI Generated Intro at bottom
    st.markdown("""
    <div class="ai-intro">
        <p>Sentilytics represents the convergence of advanced data engineering and emotional intelligence. 
        Developed within the Department of Computer Science, this platform leverages state-of-the-art 
        natural language processing to decode the human sentiment behind the digital noise.</p>
    </div>
    </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    # Sidebar
    with st.sidebar:
        st.title("Sentilytics 🧠")
        st.markdown("---")
        theme = st.selectbox("Theme Mode", ["Dark", "Light"], index=0)
        inject_theme_css(theme)
        st.markdown("---")
        st.subheader("Configuration")
        keyword = st.text_input("Track Keyword", value="Tesla")
        st.selectbox("Data Source", ["Twitter (X)", "Reddit", "News API"])
        st.slider("Refresh Rate (s)", 5, 60, 10)
        st.markdown("---")
        st.info("System Status: Online 🟢")

    # Main Dashboard Header
    col_title, col_dev = st.columns([3, 1])
    with col_title:
        st.title(f"Real-Time Sentiment Analysis: {keyword}")
        st.markdown(f"Tracking live social sentiment for **#{keyword}**")
    with col_dev:
        st.markdown(f"""
        <div style="text-align: right; margin-top: 20px;">
            <div style="font-size: 1.2em; font-weight: bold; color: #FF4B4B;">Saira Alvi</div>
            <div style="font-size: 0.9em; color: #AAAAAA;">Web Developer</div>
        </div>
        """, unsafe_allow_html=True)

    # Mock Data Generation
    sentiment_counts = pd.DataFrame({
        'Sentiment': ['Positive', 'Neutral', 'Negative'],
        'Count': [450, 300, 150]
    })
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Posts", "1,245", "+12%")
    col2.metric("Positive Sentiment", "45%", "+5%")
    col3.metric("Negative Sentiment", "15%", "-2%")
    col4.metric("Engagement Score", "8.4/10", "+0.3")

    # Charts Row 1
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Sentiment Distribution")
        fig_pie = px.pie(sentiment_counts, values='Count', names='Sentiment', 
                         color='Sentiment',
                         color_discrete_map={'Positive':'#00CC96', 'Neutral':'#636EFA', 'Negative':'#EF553B'},
                         hole=0.4)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_chart2:
        st.subheader("Sentiment Trend (Last 24h)")
        # Mock time series data
        dates = pd.date_range(start='now', periods=24, freq='H')
        trend_data = pd.DataFrame({
            'Time': dates,
            'Positive': np.random.randint(20, 50, 24),
            'Negative': np.random.randint(5, 20, 24)
        })
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=trend_data['Time'], y=trend_data['Positive'], mode='lines', name='Positive', line=dict(color='#00CC96')))
        fig_line.add_trace(go.Scatter(x=trend_data['Time'], y=trend_data['Negative'], mode='lines', name='Negative', line=dict(color='#EF553B')))
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_line, use_container_width=True)

    # Charts Row 2
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.subheader("Keyword Frequency (Word Cloud Alternative)")
        keywords = pd.DataFrame({
            'Word': ['Innovation', 'Price', 'Battery', 'CEO', 'Stock', 'Launch'],
            'Frequency': [80, 65, 50, 45, 40, 30]
        })
        fig_bar = px.bar(keywords, x='Word', y='Frequency', color='Frequency', color_continuous_scale='Viridis')
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart4:
        st.subheader("Activity Log")
        log_data = [
            "🔴 Alert: Negative sentiment spike detected at 14:00.",
            "🟢 Data Batch #452 processed successfully.",
            "🟡 Spam filter removed 45 bot accounts.",
            "🟢 New positive trend identified in 'Battery' topic.",
            "⚪ System health check passed."
        ]
        st.markdown("""
        <div style="background-color: #262730; padding: 10px; border-radius: 5px; height: 300px; overflow-y: scroll;">
        """, unsafe_allow_html=True)
        for log in log_data:
            st.markdown(f"- {log}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888888;">
        Sentilytics © 2026 | Department of Computer Science, University of Layyah
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
