import streamlit as st
from pypdf import PdfReader

from agent import ask_tutor
from memory import add_memory


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Study Tutor AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ==============================
       MAIN APPLICATION BACKGROUND
       ============================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 170, 255, 0.13),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 80%,
                rgba(110, 70, 255, 0.12),
                transparent 30%
            ),
            #070b17;

        color: #f4f7ff;
    }


    /* ==============================
       TOP BAR
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

        border-right:
            1px solid
            rgba(80, 180, 255, 0.15);
    }


    /* ==============================
       BRAND
       ============================== */

    .brand {
        padding: 10px 5px 25px 5px;
    }


    .brand-title {

        font-size: 26px;

        font-weight: 800;

        background:
            linear-gradient(
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

        margin-top: 5px;
    }


    /* ==============================
       SIDEBAR CARDS
       ============================== */

    .side-card {

        background:
            rgba(255, 255, 255, 0.035);

        border:
            1px solid
            rgba(255, 255, 255, 0.06);

        border-radius: 14px;

        padding: 14px;

        margin-bottom: 12px;
    }


    .side-label {

        color: #8795b2;

        font-size: 11px;

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
       HERO SECTION
       ============================== */

    .hero {

        padding:
            35px
            20px
            20px
            20px;
    }


    .hero-badge {

        display: inline-block;

        padding:
            6px
            12px;

        border-radius: 30px;

        background:
            rgba(0, 190, 255, 0.08);

        border:
            1px solid
            rgba(0, 200, 255, 0.25);

        color: #55d8ff;

        font-size: 12px;

        margin-bottom: 14px;
    }


    .hero-title {

        font-size: 44px;

        line-height: 1.1;

        font-weight: 800;

        background:
            linear-gradient(
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

        max-width: 720px;
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

        border:
            1px solid
            rgba(120, 180, 255, 0.12);

        border-radius: 16px;

        padding: 16px;

        height: 100px;

        transition: 0.2s;
    }


    .quick-card:hover {

        border-color:
            rgba(0, 200, 255, 0.4);

        transform:
            translateY(-2px);
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
       CHAT MESSAGES
       ============================== */

    div[data-testid="stChatMessage"] {

        background:
            rgba(255,255,255,0.025);

        border:
            1px solid
            rgba(255,255,255,0.05);

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

        background:
            rgba(10, 18, 38, 0.9);

        color: white;

        border:
            1px solid
            rgba(80, 190, 255, 0.25);

        border-radius: 16px;
    }


    /* ==============================
       BUTTONS
       ============================== */

    .stButton > button {

        border-radius: 12px;

        border:
            1px solid
            rgba(80, 190, 255, 0.25);

        background:
            rgba(20, 40, 75, 0.65);

        color: #dcecff;

        font-weight: 600;

        transition: 0.2s;
    }


    .stButton > button:hover {

        border-color:
            #00c8ff;

        background:
            rgba(0, 150, 255, 0.15);

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

        box-shadow:
            0 0 10px #00e5a8;
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


    /* ==============================
       FILE UPLOADER
       ============================== */

    div[data-testid="stFileUploader"] {

        background:
            rgba(255,255,255,0.02);

        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "study_material" not in st.session_state:

    st.session_state.study_material = ""


if "pdf_name" not in st.session_state:

    st.session_state.pdf_name = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # ---------------------------------------------
    # BRAND
    # ---------------------------------------------

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


    # ---------------------------------------------
    # AI TUTOR CARD
    # ---------------------------------------------

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


    # ---------------------------------------------
    # MEMORY CARD
    # ---------------------------------------------

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


    # ---------------------------------------------
    # MODEL CARD
    # ---------------------------------------------

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


    # ---------------------------------------------
    # PDF UPLOAD
    # ---------------------------------------------

    st.markdown(
        """
        <div class="side-label">
            STUDY MATERIAL
        </div>
        """,
        unsafe_allow_html=True
    )


    uploaded_file = st.file_uploader(
        "Upload your study PDF",
        type=["pdf"],
        help="Upload lecture notes, textbooks, or study material."
    )


    # ---------------------------------------------
    # READ PDF
    # ---------------------------------------------

    if uploaded_file is not None:

        if st.session_state.pdf_name != uploaded_file.name:

            try:

                reader = PdfReader(uploaded_file)

                pdf_text = ""

                for page in reader.pages:

                    text = page.extract_text()

                    if text:

                        pdf_text += text + "\n"


                st.session_state.study_material = pdf_text

                st.session_state.pdf_name = uploaded_file.name


            except Exception as error:

                st.error(
                    f"Could not read PDF: {error}"
                )


        if st.session_state.study_material:

            st.success(
                f"Loaded: {uploaded_file.name}"
            )


    # ---------------------------------------------
    # CLEAR CHAT
    # ---------------------------------------------

    st.markdown("---")


    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# MAIN HERO
# =========================================================

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


# =========================================================
# QUICK ACTIONS
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="quick-title">QUICK ACTIONS</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    # ---------------------------------------------
    # EXPLAIN
    # ---------------------------------------------

    with col1:

        st.markdown(
            """
            <div class="quick-card">

                <div class="quick-icon">
                    🧠
                </div>

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


    # ---------------------------------------------
    # PRACTICE
    # ---------------------------------------------

    with col2:

        st.markdown(
            """
            <div class="quick-card">

                <div class="quick-icon">
                    📝
                </div>

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


    # ---------------------------------------------
    # SUMMARY
    # ---------------------------------------------

    with col3:

        st.markdown(
            """
            <div class="quick-card">

                <div class="quick-icon">
                    📖
                </div>

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


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask your tutor anything..."
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # ---------------------------------------------
    # SHOW USER MESSAGE
    # ---------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)


    # Save to current session

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # Save to long-term/simple memory

    add_memory(
        "Student",
        question
    )


    # ---------------------------------------------
    # ASK AGENT
    # ---------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "✦ Your tutor is thinking..."
        ):

            try:

                answer = ask_tutor(question)

            except Exception as error:

                answer = (
                    "Sorry, I encountered an error "
                    "while processing your question.\n\n"
                    f"Error: `{error}`"
                )


        st.markdown(answer)


    # ---------------------------------------------
    # SAVE AI RESPONSE
    # ---------------------------------------------

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


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        ✦ Study Tutor AI
        &nbsp; • &nbsp;
        Powered by CrewAI + Groq

    </div>
    """,
    unsafe_allow_html=True
)
