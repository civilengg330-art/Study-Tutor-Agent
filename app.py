import streamlit as st

from agent import ask_tutor
from memory import add_memory, load_memory


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Study Tutor AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* ==============================
       MAIN BACKGROUND
       ============================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 170, 255, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 80%,
                rgba(110, 70, 255, 0.10),
                transparent 30%
            ),
            #070b17;
        color: #f4f7ff;
    }


    /* ==============================
       REMOVE STREAMLIT TOP BAR
       ============================== */

    header {
        background: transparent !important;
    }


    /* ==============================
       SIDEBAR
       ============================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                rgba(10, 18, 38, 0.98),
                rgba(5, 10, 24, 0.98)
            );

        border-right: 1px solid rgba(80, 180, 255, 0.15);
    }


    /* ==============================
       SIDEBAR BRAND
       ============================== */

    .brand {
        padding: 10px 5px 25px 5px;
    }

    .brand-title {
        font-size: 25px;
        font-weight: 800;

        background: linear-gradient(
            90deg,
            #00c6ff,
            #5b8cff,
            #a66cff
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brand-subtitle {
        color: #8d9bb8;
        font-size: 13px;
        margin-top: 4px;
    }


    /* ==============================
       SIDEBAR ITEMS
       ============================== */

    .side-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.06);

        border-radius: 14px;

        padding: 14px;

        margin-bottom: 12px;
    }

    .side-label {
        color: #8795b2;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .side-value {
        color: #eef4ff;
        font-size: 15px;
        font-weight: 600;

        margin-top: 5px;
    }


    /* ==============================
       MAIN HERO
       ============================== */

    .hero {
        padding: 35px 20px 20px 20px;
    }

    .hero-badge {
        display: inline-block;

        padding: 6px 12px;

        border-radius: 30px;

        background: rgba(0, 190, 255, 0.08);

        border: 1px solid rgba(0, 200, 255, 0.25);

        color: #55d8ff;

        font-size: 12px;

        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 44px;
        line-height: 1.1;

        font-weight: 800;

        background: linear-gradient(
            90deg,
            #ffffff,
            #8fdfff,
            #7c8cff
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin: 0;
    }

    .hero-text {
        color: #8f9db8;

        font-size: 16px;

        margin-top: 12px;

        max-width: 700px;
    }


    /* ==============================
       QUICK ACTION CARDS
       ============================== */

    .quick-title {
        color: #aab6cf;
        font-size: 13px;

        margin-top: 25px;
        margin-bottom: 10px;
    }

    .quick-card {
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.055),
                rgba(255,255,255,0.02)
            );

        border: 1px solid rgba(120, 180, 255, 0.12);

        border-radius: 16px;

        padding: 16px;

        height: 100px;

        transition: 0.2s;
    }

    .quick-card:hover {
        border-color: rgba(0, 200, 255, 0.4);
        transform: translateY(-2px);
    }

    .quick-icon {
        font-size: 24px;
    }

    .quick-name {
        color: #edf4ff;

        font-weight: 700;

        margin-top: 8px;
    }

    .quick-description {
        color: #7f8da8;

        font-size: 11px;
    }


    /* ==============================
       CHAT MESSAGE
       ============================== */

    div[data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.025);

        border: 1px solid rgba(255,255,255,0.05);

        border-radius: 16px;

        padding: 12px;

        margin-bottom: 10px;
    }


    /* ==============================
       CHAT INPUT
       ============================== */

    div[data-testid="stChatInput"] {
        border-radius: 18px;
    }

    div[data-testid="stChatInput"] textarea {
        background: rgba(10, 18, 38, 0.9);

        color: white;

        border: 1px solid rgba(80, 190, 255, 0.25);

        border-radius: 16px;
    }


    /* ==============================
       BUTTONS
       ============================== */

    .stButton > button {
        border-radius: 12px;

        border: 1px solid rgba(80, 190, 255, 0.25);

        background: rgba(20, 40, 75, 0.65);

        color: #dcecff;

        font-weight: 600;

        transition: 0.2s;
    }

    .stButton > button:hover {
        border-color: #00c8ff;

        background: rgba(0, 150, 255, 0.15);

        color: white;
    }


    /* ==============================
       STATUS
       ============================== */

    .status {
        display: flex;
        align-items: center;

        gap: 7px;

        color: #91a0ba;

        font-size: 12px;
    }

    .status-dot {
        width: 8px;
        height: 8px;

        background: #00e5a8;

        border-radius: 50%;

        box-shadow: 0 0 10px #00e5a8;
    }


    /* ==============================
       FOOTER
       ============================== */

    .footer {
        text-align: center;

        color: #596782;

        font-size: 11px;

        padding: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div class="brand">

            <div class="brand-title">
                ✦ Study Tutor
            </div>

            <div class="brand-subtitle">
                AI-powered learning companion
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="side-card">

            <div class="side-label">
                AI Tutor
            </div>

            <div class="side-value">
                Study Assistant
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="side-card">

            <div class="side-label">
                Memory
            </div>

            <div class="side-value">
                🟢 Active
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="side-card">

            <div class="side-label">
                Model
            </div>

            <div class="side-value">
                GPT-OSS 120B
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("---")


    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✦ AI STUDY ASSISTANT
        </div>

        <div class="hero-title">
            Learn smarter.
            <br>
            Understand deeper.
        </div>

        <div class="hero-text">
            Ask questions, simplify difficult concepts,
            solve problems and practice with your personal
            AI study tutor.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# QUICK ACTIONS
# ---------------------------------------------------------

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="quick-title">QUICK ACTIONS</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            <div class="quick-card">

                <div class="quick-icon">🧠</div>

                <div class="quick-name">
                    Explain a concept
                </div>

                <div class="quick-description">
                    Make difficult topics simple
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
            <div class="quick-card">

                <div class="quick-icon">📝</div>

                <div class="quick-name">
                    Practice
                </div>

                <div class="quick-description">
                    Generate questions to test yourself
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
            <div class="quick-card">

                <div class="quick-icon">📖</div>

                <div class="quick-name">
                    Summarize
                </div>

                <div class="quick-description">
                    Turn long topics into key points
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

question = st.chat_input(
    "Ask your tutor anything..."
)


if question:

    # Display student message

    with st.chat_message("user"):

        st.markdown(question)


    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # Save to memory

    add_memory(
        "Student",
        question
    )


    # Generate tutor response

    with st.chat_message("assistant"):

        with st.spinner("✦ Thinking..."):

            answer = ask_tutor(question)


        st.markdown(answer)


    # Save response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    add_memory(
        "Tutor",
        answer
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">

        ✦ Study Tutor AI &nbsp; • &nbsp;
        Powered by CrewAI + Groq

    </div>
    """,
    unsafe_allow_html=True
)
