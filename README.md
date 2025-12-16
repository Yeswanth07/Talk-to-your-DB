# 🗣️ Talk with your DB 

[Link](https://talk-to-your-sql-db.streamlit.app/)

A powerful Streamlit application that lets you interact with your SQLite databases using natural language queries. No SQL knowledge required!

## ✨ Features

- **🔍 Database Explorer**: Visualize your database structure, table schemas, and preview data
- **💬 Natural Language Queries**: Ask questions about your data in plain English
- **🤖 AI-Powered SQL Generation**: Automatically converts natural language to SQL using Groq's LLM
- **📊 Interactive Chat Interface**: Persistent conversation history with your database
- **🎯 Smart Context Awareness**: AI understands your exact table and column names
- **⚡ Fast & Accurate**: Powered by Groq's high-performance language models

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Groq API Key** - Get yours from [Groq Console](https://console.groq.com/)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd talk-with-your-db
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run talk_with_db_app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📦 Dependencies

```txt
streamlit
pandas
agno
sqlalchemy
groq
python-dotenv
sqlite3 (built-in)
```

## 🎯 How to Use

### 1. Upload Your Database
- Click "Choose a SQLite database file" in the sidebar
- Upload your `.db`, `.sqlite`, or `.sqlite3` file
- The app will automatically analyze your database structure

### 2. Explore Your Data
- View all tables and their schemas in the sidebar
- Check row counts and column information
- Preview table data with the preview buttons

### 3. Ask Questions
Start chatting with your database using natural language:

```
"Show me all customers from Germany"
"What are the top 5 best-selling products?"
"Calculate total revenue by country"
"Find customers who haven't made any orders"
"Which genre has the highest number of tracks?"
```

## 📁 Project Structure

```
talk-with-your-db/
├── talk_with_db_app.py      # Main Streamlit application
├── sqllite_agent.py         # Original agent implementation
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for AI processing | Yes |

### Supported File Types

- `.db` - SQLite database files
- `.sqlite` - SQLite database files  
- `.sqlite3` - SQLite database files

## 🌟 Example Queries

### Basic Queries
- "How many customers do we have?"
- "Show me all products"
- "List all employees"

### Analytics Queries
- "What's our total revenue?"
- "Which month had the highest sales?"
- "Top 10 customers by purchase amount"

### Complex Queries
- "Show customers who bought more than 5 items"
- "Calculate average order value by country"
- "Find products that haven't been sold"

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit for the web interface
- **Backend**: Agno framework with SQLTools
- **AI Model**: Groq's Llama 3.3 70B Versatile
- **Database**: SQLite with SQLAlchemy

### Key Components

1. **Database Explorer**: Analyzes SQLite schema and provides table information
2. **AI Agent**: Converts natural language to SQL queries
3. **Query Processor**: Executes SQL and formats results
4. **Chat Interface**: Manages conversation history and user interactions

### Error Handling
- API key validation
- Database connection error handling
- SQL execution error recovery
- Clean error messages for users

## 🔍 Troubleshooting

### Common Issues

1. **"GROQ_API_KEY not found"**
   - Ensure your `.env` file exists and contains the API key
   - Restart the application after adding the key

2. **"No such table" errors**
   - Check your database file is valid
   - Use the database explorer to see available tables

3. **Connection errors**
   - Ensure your SQLite file isn't corrupted
   - Try with a different database file

### Getting Help

If you encounter issues:
1. Check the error messages in the app
2. Verify your API key is valid
3. Ensure your database file is accessible
4. Check the console for detailed error logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for the high-performance language models
- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [Agno](https://github.com/agno-ai/agno) for the agent framework
- The open-source community for the excellent tools and libraries

## 🔮 Roadmap

- [ ] Support for multiple database types (MySQL, PostgreSQL)
- [ ] Query result visualization with charts
- [ ] Export query results to CSV/Excel
- [ ] Query history and favorites
- [ ] Multi-table join optimization
- [ ] Custom SQL query editor
- [ ] Database schema recommendations

---

**Made with ❤️ and AI**

*Transform your database interactions with the power of natural language!*
