"""
Streamlit UI application for Country Information AI Agent.
Web interface for querying country information.
"""

import streamlit as st
from agent import CountryInformationAgent
from config import Config


def initialize_agent():
    """Initialize the agent and store it in session state."""
    if "agent" not in st.session_state:
        try:
            Config.validate()
            st.session_state.agent = CountryInformationAgent()
            st.session_state.agent_initialized = True
        except ValueError as e:
            st.session_state.agent_initialized = False
            st.session_state.agent_error = str(e)
    return st.session_state.get("agent")


def initialize_chat_history():
    """Initialize chat history in session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def main():
    """Main application."""
    st.set_page_config(
        page_title="Country Information AI Agent",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🌍 Country Information AI Agent")
    st.markdown("Ask me questions about countries! I can help you find information about population, capital, currency, and more.")
    
    initialize_chat_history()
    agent = initialize_agent()
    
    if not st.session_state.get("agent_initialized", False):
        st.error(f"Configuration Error: {st.session_state.get('agent_error', 'OpenAI API key not configured.')}")
        st.info("Please set your OPENAI_API_KEY in the .env file or environment variables.")
        return
    
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This AI agent uses LangGraph to answer questions about countries.
        
        **Features:**
        - Intent identification
        - Data fetching from REST Countries API
        - Natural language answer synthesis
        
        **Example Questions:**
        - What is the population of Germany?
        - What currency does Japan use?
        - What is the capital and population of Brazil?
        """)
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask a question about any country..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Processing your query..."):
                try:
                    answer = agent.query(prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    error_message = f"I encountered an error while processing your query: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})


if __name__ == "__main__":
    main()

