# Debug configuration
# VS Code debugging is configured in launch.json
# Set breakpoints in your code and use the "Python: Streamlit App" or "Python: Debug chat.py" launch configuration

import streamlit as st
import asyncio
import logging
from chat import process_message, reset_chat_history
from multi_agent import run_multi_agent

# Configure logging
logging.basicConfig(level=logging.INFO)


def configure_sidebar():
    """Configure a clean, modern sidebar"""
    # Ensure theme default exists early so we can style sidebar conditionally
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"
    # Initialize selected option
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = "Chat"
    # Theme-aware sidebar CSS
    if st.session_state.theme == "Dark":
        st.sidebar.markdown(
            """
        <style>
        .sidebar .sidebar-content { background: #1a1a1a; }
        .nav-container { background: #262626; border-radius: 12px; padding: 16px; margin-bottom: 24px; border: 1px solid #404040; }
        .nav-title { color: #ffffff; font-size: 18px; font-weight: 600; margin-bottom: 16px; text-align: center; letter-spacing: -0.025em; }
        .nav-button { display:block; width:100%; padding:12px 16px; margin:8px 0; background: transparent; border:2px solid #6b7280; border-radius:8px; color:#e5e5e5; font-weight:500; transition: all .2s ease; cursor:pointer; }
        .nav-button:hover { background:#3b82f6; border-color:#3b82f6; color:#ffffff; transform: translateY(-1px); }
        .nav-button.active { background:#10b981; border-color:#10b981; color:#ffffff; }
        .stats-container { background:#262626; border-radius:12px; padding:16px; border:1px solid #404040; }
        .stats-title { color:#ffffff; font-size:16px; font-weight:600; margin-bottom:12px; }
        .stat-item { display:flex; justify-content:space-between; padding:8px 0; color:#e5e5e5; border-bottom:1px solid #404040; }
        .stat-item:last-child { border-bottom:none; }
        .stat-label { font-weight:500; }
        .stat-value { color:#10b981; font-weight:600; }
        </style>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.markdown(
            """
        <style>
        .sidebar .sidebar-content { background: #f3f4f6; }
        .nav-container { background: #ffffff; border-radius: 12px; padding: 16px; margin-bottom: 24px; border: 1px solid #111827; }
        .nav-title { color: #111827; font-size: 18px; font-weight: 700; margin-bottom: 16px; text-align: center; letter-spacing: -0.02em; }
        .nav-button { display:block; width:100%; padding:12px 16px; margin:8px 0; background:#ffffff; border:2px solid #111827; border-radius:8px; color:#111827; font-weight:600; transition: all .2s ease; cursor:pointer; }
        .nav-button:hover { background:#111827; color:#ffffff; border-color:#111827; }
        .nav-button.active { background:#111827; color:#ffffff; border-color:#111827; }
        .stats-container { background:#ffffff; border-radius:12px; padding:16px; border:1px solid #111827; }
        .stats-title { color:#111827; font-size:16px; font-weight:700; margin-bottom:12px; }
        .stat-item { display:flex; justify-content:space-between; padding:8px 0; color:#111827; border-bottom:1px solid #111827; }
        .stat-item:last-child { border-bottom:none; }
        .stat-label { font-weight:600; color:#111827; }
        .stat-value { color:#065f46; font-weight:700; }
        </style>
        """,
            unsafe_allow_html=True,
        )

    # Navigation section
    st.sidebar.markdown(
        """
    <div class="nav-container">
        <div class="nav-title">🚀 AI Workshop for Developers</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    # Theme toggle with immediate rerun
    _old_theme = st.session_state.theme
    st.sidebar.selectbox(
        "Theme",
        ["Dark", "Light"],
        index=(0 if st.session_state.theme == "Dark" else 1),
        key="theme",
    )
    if st.session_state.theme != _old_theme:
        st.rerun()

    # Navigation buttons
    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("💬 Chat", key="nav_chat", use_container_width=True):
            st.session_state.selected_option = "Chat"

    with col2:
        if st.button("🤖 Team", key="nav_multi", use_container_width=True):
            st.session_state.selected_option = "Multi-Agent"

    # Session stats
    st.sidebar.markdown("---")

    if st.session_state.selected_option == "Chat":
        chat_count = len(st.session_state.get("chat_history", []))
        st.sidebar.metric("Messages", chat_count, delta=None)
    else:
        multi_agent_count = len(st.session_state.get("multi_agent_history", []))
        st.sidebar.metric("Team Messages", multi_agent_count, delta=None)

    return st.session_state.selected_option


def render_chat_ui(title, on_submit):
    """Renders a modern, clean chat UI"""
    # Minimal UI CSS only: layout spacing
    st.markdown(
        """
    <style>
    .main .block-container { padding-top: 2rem; max-width: 1200px; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Header with new chat button
    header_col1, header_col2 = st.columns([5, 1])

    with header_col1:
        if title == "Chat":
            st.markdown(
                """
            <div class="chat-header">
                <h1 class="chat-title">💬 AI Assistant</h1>
                <p class="chat-subtitle">Your intelligent coding companion</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
            <div class="chat-header">
                <h1 class="chat-title">🤖 AI Team</h1>
                <p class="chat-subtitle">Collaborative intelligence at work</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with header_col2:
        if st.button(
            "🔄 Reset",
            key=f"new_chat_{title}",
            use_container_width=True,
            type="secondary",
        ):
            if title == "Chat":
                st.session_state.chat_history = []
                reset_chat_history()
                st.success("Chat reset!")
            elif title == "Multi-Agent":
                st.session_state.multi_agent_history = []
                st.success("Team session reset!")
            st.rerun()

    # Chat input
    if title == "Chat":
        user_input = st.chat_input("Ask me anything...", key="chat_input")
    else:
        user_input = st.chat_input(
            "Describe your project requirements...", key="multi_agent_input"
        )

    if user_input:
        on_submit(user_input)


def chat():
    """Enhanced chat functionality"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def on_chat_submit(user_input):
        if user_input:
            try:
                # Add user message
                st.session_state.chat_history.append(
                    {"role": "user", "message": user_input}
                )

                # Show processing indicator
                with st.spinner("Processing..."):
                    assistant_response = asyncio.run(process_message(user_input))

                # Add assistant response
                st.session_state.chat_history.append(
                    {"role": "assistant", "message": str(assistant_response)}
                )

                st.rerun()

            except Exception as e:
                import traceback

                error_msg = f"Error: {str(e)}"
                logging.error(error_msg)
                tb = traceback.format_exc()
                logging.error(f"Traceback: {tb}")

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "message": f"**Error**: {error_msg}\n\nPlease try again.",
                    }
                )

                st.session_state.show_error_details = True
                st.session_state.error_traceback = tb

    render_chat_ui("Chat", on_chat_submit)
    display_chat_history(st.session_state.chat_history)

    # Error details expander
    if st.session_state.get("show_error_details", False):
        with st.expander("Debug Info", expanded=False):
            st.code(st.session_state.error_traceback, language="python")
        st.session_state.show_error_details = False


def multi_agent():
    """Enhanced multi-agent system"""
    if "multi_agent_history" not in st.session_state:
        st.session_state.multi_agent_history = []

    def on_multi_agent_submit(user_input):
        if user_input:
            try:
                st.session_state.multi_agent_history.append(
                    {"role": "user", "message": user_input}
                )

                with st.spinner("Team collaborating..."):
                    result = asyncio.run(run_multi_agent(user_input))

                for response in result:
                    st.session_state.multi_agent_history.append(
                        {"role": response["role"], "message": response["message"]}
                    )

                st.rerun()

            except Exception as e:
                logging.error(f"Multi-agent error: {e}")
                st.session_state.multi_agent_history.append(
                    {
                        "role": "assistant",
                        "message": f"**Team Error**: {str(e)}\n\nPlease try again.",
                    }
                )

    render_chat_ui("Multi-Agent", on_multi_agent_submit)
    display_chat_history(st.session_state.multi_agent_history)


def display_chat_history(chat_history):
    """Display chat history with modern styling"""
    # Role avatars and colors
    role_config = {
        "user": {"avatar": "👤", "name": "You"},
        "assistant": {"avatar": "🤖", "name": "Assistant"},
        "BusinessAnalyst": {"avatar": "📊", "name": "Business Analyst"},
        "SoftwareEngineer": {"avatar": "⚡", "name": "Engineer"},
        "ProductOwner": {"avatar": "🎯", "name": "Product Owner"},
    }

    if not chat_history:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown("**Ready to help!** What can I do for you today?")
        return

    for chat in chat_history:
        role = chat.get("role", "assistant")
        message = chat.get("message", "")

        config = role_config.get(role, {"avatar": "🤖", "name": role})

        with st.chat_message(
            "user" if role == "user" else "assistant", avatar=config["avatar"]
        ):
            # Show role name for agents
            if role not in ["user", "assistant"]:
                st.markdown(f"**{config['name']}**")

            # Display message
            if isinstance(message, str):
                if "error" in message.lower():
                    st.error(message)
                elif "success" in message.lower():
                    st.success(message)
                else:
                    st.markdown(message)
            else:
                st.write(message)


def main():
    """Main application with modern dark theme"""
    st.set_page_config(
        page_title="AI Workshop",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Minimal theming override (simplified):
    if st.session_state.get("theme", "Dark") == "Dark":
        st.markdown(
            """
            <style>
            :root { --bg: #111827; --fg: #f9fafb; }
            html, body { background-color: var(--bg) !important; }
            .stApp { background-color: var(--bg) !important; color: var(--fg) !important; }
            /* Sidebar transparency */
            .stSidebar { background: transparent !important; }
            /* Header/Footer */
            [data-testid="stHeader"], [data-testid="stDecoration"] { background: var(--bg) !important; border-bottom: 1px solid #374151; }
            [data-testid="stFooter"], footer { background: var(--bg) !important; border-top: 1px solid #374151; }
            /* Theme select */
            :is(.stSelectbox, [data-testid="stSelectbox"]) :is(div[data-baseweb="select"], div[role="combobox"]) {
                background: transparent !important;
                color: #f9fafb !important;
                border: none !important;
            }
            :is(.stSelectbox, [data-testid="stSelectbox"]) div[role="listbox"] {
                background: #1f2937 !important;
                color: #f9fafb !important;
                border: 1px solid #e5e7eb !important;
            }
            :is(.stSelectbox, [data-testid="stSelectbox"]) svg { fill: #f9fafb !important; }
            /* Buttons */
            .stButton > button,
            .stButton > button[kind="secondary"] {
                background: #1f2937 !important;
                color: #f9fafb !important;
                border: 1px solid #e5e7eb !important;
            }
            /* Chat input */
            [data-testid="stChatInput"] > div,
            [data-testid="stChatInput"] div[data-baseweb="textarea"],
            [data-testid="stChatInput"] div[data-baseweb="base-input"] {
                background: #1f2937 !important;
                border: none !important;
                border-radius: 12px !important;
            }
            [data-testid="stChatInput"] textarea,
            [data-testid="stChatInput"] input {
                background: transparent !important;
                color: #f9fafb !important;
                border: none !important;
            }
            /* Messages and avatars */
            .stChatMessage, .stChatMessage * { color: #f9fafb !important; }
            .stChatMessage [data-testid*="avatar"],
            .stChatMessage [class*="avatar"],
            .stChatMessage > div:first-child,
            .stChatMessage > div:first-child * {
                background: transparent !important;
                color: #f9fafb !important;
                fill: #f9fafb !important;
            }
            /* Subtitle */
            .chat-subtitle { color: #d1d5db !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            :root { --bg: #ffffff; --fg: #000000; }
            html, body { background-color: var(--bg) !important; color: var(--fg) !important; }
            .stApp { background-color: var(--bg) !important; color: var(--fg) !important; }
            /* Sidebar transparency */
            .stSidebar { background: #ffffff !important; }
            /* Header & footer */
            [data-testid="stHeader"], [data-testid="stDecoration"] { background: #ffffff !important; border-bottom: 1px solid #e5e7eb; color: #000000 !important;}
            [data-testid="stToolbar"], [data-testid="stBottomBlockContainer"], footer { background: #ffffff !important; border-top: 1px solid #e5e7eb; color: #000000 !important;}
            [data-testid="stHeader"] [data-testid="stStatusWidget"],
            [data-testid="stHeader"] [data-testid="stStatusWidget"] *,
            [data-testid="stHeader"] [data-testid="stBaseButton-Header"],
            [data-testid="stHeader"] [data-testid="stBaseButton-Header"] * {
                color: #111827 !important;
            }
            /* Theme select (container, combobox, dropdown) */
            :is(.stSelectbox, [data-testid="stSelectbox"]) label {
                color: #111827 !important;
            }
            :is(.stSelectbox, [data-testid="stSelectbox"]) div[data-baseweb="select"] {
                background: #ffffff !important;
                color: #111827 !important;
                border: 1px solid #111827 !important;
                border-radius: 8px !important;
            }
            :is(.stSelectbox, [data-testid="stSelectbox"]) div[data-baseweb="select"] > div {
                background: #ffffff !important;
                color: #111827 !important;
            }
            :is(.stSelectbox, [data-testid="stSelectbox"]) div[role="combobox"] {
                background: #ffffff !important;
                color: #111827 !important;
            }
            :is(.stSelectbox, [data-testid="stSelectbox"]) div[role="listbox"] {
                background: #ffffff !important;
                color: #111827 !important;
                border: 1px solid #111827 !important;
            }
            :is(.stSelectbox, [data-testid="stSelectbox"]) div[role="option"] {
                color: #111827 !important;
            }
            :is(.stSelectbox, [data-testid="stSelectbox"]) div[data-baseweb="popover"],
            :is(.stSelectbox, [data-testid="stSelectbox"]) div[data-baseweb="menu"] {
                background: #ffffff !important;
                color: #111827 !important;
                border: 1px solid #111827 !important;
            }
            :is(.stSelectbox, [data-testid="stSelectbox"]) svg { fill: #111827 !important; }
            /* Sidebar buttons */
            .stButton > button,
            .stButton > button[kind="secondary"] {
                background: #ffffff !important;
                color: #111827 !important;
                border: 1px solid #111827 !important;
            }
            /* Chat input */
            [data-testid="stChatInput"] > div,
            [data-testid="stChatInput"] div[data-baseweb="textarea"],
            [data-testid="stChatInput"] div[data-baseweb="base-input"] {
                background: #ffffff !important;
                border: none !important;
                border-radius: 12px !important;
            }
            [data-testid="stChatInput"] textarea,
            [data-testid="stChatInput"] input,
            [data-testid="stChatInput"] textarea[data-testid="stChatInputTextArea"] {
                background: #f0f0f0 !important;
                color: #111827 !important;
                border: none !important;
            }
            [data-testid="stChatInput"] textarea[data-testid="stChatInputTextArea"]::placeholder {
                color: #6b7280 !important;
                padding-left: 5px !important;
            }
            /* Messages & avatars */
            .stChatMessage, .stChatMessage * { color: #111827 !important; }
            .stChatMessage [data-testid*="avatar"],
            .stChatMessage [class*="avatar"],
            .stChatMessage > div:first-child,
            .stChatMessage > div:first-child * {
                background: transparent !important;
                color: #111827 !important;
                fill: #111827 !important;
            }
            /* Subtitle */
            .chat-title { color: #111827 !important; }
            .chat-subtitle { color: #1f2937 !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Configure sidebar and get operation
    chosen_operation = configure_sidebar()

    # Route to functionality
    if chosen_operation == "Chat":
        chat()
    elif chosen_operation == "Multi-Agent":
        multi_agent()


if __name__ == "__main__":
    main()
