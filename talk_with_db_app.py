import streamlit as st
import os
import tempfile
import sqlite3
import pandas as pd
import re
from agno.agent import Agent
from agno.tools.sql import SQLTools
from agno.models.groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Page configuration
st.set_page_config(
    page_title="Talk with your DB",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_agent_response(query, db_path):
    """Modified version of the original function to work with uploaded files"""
    # First, get table information to provide context
    table_info = explore_database(db_path)
    table_names = list(table_info.keys())
    
    # Create enhanced system message with table context
    system_message = f"""
    You are a helpful assistant that translates natural language to SQL queries for a SQLite database.
    
    IMPORTANT DATABASE CONTEXT:
    Available tables: {', '.join(table_names)}
    
    Table details:
    """
    
    for table_name, info in table_info.items():
        columns = [col[1] for col in info['columns']]  # Get column names
        system_message += f"\n- {table_name}: columns = {', '.join(columns)}"
    
    system_message += """
    
    IMPORTANT RULES:
    - Use the EXACT table names and column names as provided above
    - Do not include any `limit` parameter when calling tools unless explicitly requested by the user
    - Always return numeric values (not strings) for tool parameters
    - First use list_tables() to confirm available tables if unsure
    - Provide clear, well-formatted responses with explanations when appropriate
    """
    
    agent = Agent(
        name="SQLite Agent",
        model=Groq(id="qwen/qwen3-32b", api_key=groq_api_key),  # Changed model
        markdown=True,
        system_message=system_message,
        tools=[SQLTools(db_url=f'sqlite:///{db_path}')],
        retries=3,
        reasoning=False,  # Disabled reasoning to avoid JSON mode issues
    )
    
    # Get the agent's response without printing debug info
    try:
        response = agent.run(query)
        # Extract just the main response content, removing debug formatting
        if hasattr(response, 'content'):
            clean_response = response.content
        else:
            clean_response = str(response)
        
        # Remove ANSI color codes and formatting
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_response = ansi_escape.sub('', clean_response)
        
        # Remove extra whitespace and clean up
        clean_response = clean_response.strip()
        
        return clean_response
    except Exception as e:
        return f"Error processing query: {str(e)}"

def explore_database(db_path):
    """Function to explore database structure"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    table_info = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        table_info[table_name] = {
            'columns': columns,
            'row_count': row_count
        }
    
    conn.close()
    return table_info

def preview_table(db_path, table_name, limit=5):
    """Function to preview table data"""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", conn)
    conn.close()
    return df

# Main app
def main():
    st.title("🗣️ Talk with your DB")
    st.markdown("Upload your SQLite database and ask questions in natural language!")
    
    # Sidebar for database upload and exploration
    with st.sidebar:
        st.header("📁 Database Upload")
        uploaded_file = st.file_uploader(
            "Choose a SQLite database file",
            type=['db', 'sqlite', 'sqlite3'],
            help="Upload your SQLite database file to start querying"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite') as tmp_file:
                tmp_file.write(uploaded_file.read())
                db_path = tmp_file.name
            
            st.success(f"✅ Database '{uploaded_file.name}' loaded successfully!")
            
            # Store db_path in session state
            st.session_state.db_path = db_path
            st.session_state.db_name = uploaded_file.name
            
            # Database exploration
            st.header("🔍 Database Structure")
            try:
                table_info = explore_database(db_path)
                
                for table_name, info in table_info.items():
                    with st.expander(f"📊 {table_name} ({info['row_count']} rows)"):
                        st.write("**Columns:**")
                        col_df = pd.DataFrame(info['columns'], 
                                            columns=['Column ID', 'Name', 'Type', 'Not Null', 'Default', 'Primary Key'])
                        st.dataframe(col_df[['Name', 'Type', 'Not Null', 'Primary Key']], width='stretch')
                        
                        if st.button(f"Preview {table_name}", key=f"preview_{table_name}"):
                            preview_df = preview_table(db_path, table_name)
                            st.dataframe(preview_df, width='stretch')
            
            except Exception as e:
                st.error(f"Error exploring database: {str(e)}")
    
    # Main content area
    if 'db_path' in st.session_state:
        st.header("💬 Chat with your Database")
        st.info(f"Currently connected to: **{st.session_state.db_name}**")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your database..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get agent response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing your query..."):
                    try:
                        if not groq_api_key:
                            st.error("❌ GROQ_API_KEY not found. Please set your API key in the environment variables.")
                            response = "Please configure your GROQ API key to use this feature."
                        else:
                            # Show available tables for context
                            try:
                                table_info = explore_database(st.session_state.db_path)
                                table_names = list(table_info.keys())
                                st.info(f"📊 Available tables: {', '.join(table_names)}")
                            except:
                                pass
                            
                            response = get_agent_response(prompt, st.session_state.db_path)
                            
                        st.markdown(response)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        error_msg = f"❌ Error processing query: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        # Clear chat button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Clear Chat History", width='stretch'):
                st.session_state.messages = []
                st.rerun()
    
    else:
        # Welcome screen
        st.header("👋 Welcome!")
        st.markdown("""
        ### How to use this app:
        
        1. **Upload your SQLite database** using the sidebar
        2. **Explore your database structure** in the sidebar to understand your data
        3. **Ask questions in natural language** about your data
        4. **Get AI-powered SQL queries and results** instantly!
        
        ### Example queries you can try:
        - "Show me all customers from Germany"
        - "What are the top 5 best-selling products?"
        - "Calculate total revenue by country"
        - "Find customers who haven't made any orders"
        - "Show me monthly sales trends"
        
        ### Features:
        - 🔍 **Database exploration** - View table structures and preview data
        - 💬 **Natural language queries** - No need to write SQL
        - 📊 **Intelligent responses** - Get explanations along with results
        - 🔄 **Chat history** - Keep track of your conversation
        - 🚀 **Powered by Groq's Llama model** - Fast and accurate responses
        """)
        
        # API Key check
        if not groq_api_key:
            st.warning("⚠️ **GROQ_API_KEY not configured.** Please set your API key in environment variables to use AI features.")
            st.code("export GROQ_API_KEY=your_api_key_here")

if __name__ == "__main__":
    main()