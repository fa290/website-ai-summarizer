
# 🌐 Website AI Summarizer

A Generative AI application that extracts content from company websites and generates organized summaries using a Large Language Model.

## 🚀 Features

- Enter a company website URL.
- Extract readable website content.
- Clean HTML content using BeautifulSoup.
- Generate AI-powered summaries.
- Display results through an interactive Streamlit interface.

## 🛠️ Technologies

- Python
- Streamlit
- Groq API
- LLM
- Requests
- BeautifulSoup

## ⚙️ Installation

1. Clone the repository:

   git clone https://github.com/fa290/website-ai-summarizer.git

2. Navigate to the project folder:

   cd website-ai-summarizer

3. Install dependencies:

   pip install streamlit requests beautifulsoup4 python-dotenv openai

4. Create a `.env` file and add your Groq API key:

   GROQ_API_KEY=your_api_key

5. Run the application:

   streamlit run app.py

## 💡 How It Works

1. The user enters a company website URL.
2. The application retrieves the webpage content.
3. BeautifulSoup extracts and cleans the text.
4. Groq API sends the content to an LLM.
5. The AI generates an organized summary.
<img width="1280" height="782" alt="image_1448-05-19_23-43-22" src="https://github.com/user-attachments/assets/81d6777a-3911-4404-9d21-75588660b410" />

## 👩‍💻 Author

Menna Farghaly
