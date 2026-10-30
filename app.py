
import os
import requests
import streamlit as st

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY was not found. Check your .env file.")
    st.stop()


client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "openai/gpt-oss-120b"


st.set_page_config(
    page_title="Website AI Summarizer",
    page_icon="🌐",
    layout="wide"
)


def get_website_content(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "noscript"
    ]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""

    text = soup.get_text(separator=" ", strip=True)

    return title, text


def summarize_website(title, website_text):

    prompt = f"""
    You are a professional website analysis assistant.

    Analyze the following company website content.

    Create a clear and organized summary including:

    1. Company Overview
    2. Main Products and Services
    3. Target Audience
    4. Important Information

    Use only the information provided.
    Do not invent missing details.
    If information is unavailable, say so.

    Website Title:
    {title}

    Website Content:
    {website_text[:15000]}
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


st.title("🌐 Website AI Summarizer")

st.write(
    "Enter a company website URL and let AI analyze "
    "and summarize its content."
)

url = st.text_input(
    "Company Website URL",
    placeholder="https://example.com"
)

if st.button("✨ Summarize Website", type="primary"):

    if not url.strip():
        st.warning("Please enter a website URL.")

    elif not url.startswith(("http://", "https://")):
        st.warning("Please enter a valid URL starting with http:// or https://")

    else:

        try:
            with st.spinner("Reading website content..."):

                title, website_text = get_website_content(url)

            if len(website_text.strip()) < 100:
                st.error(
                    "Not enough readable text was found on this website."
                )
                st.stop()

            with st.spinner("AI is analyzing the website..."):

                summary = summarize_website(
                    title,
                    website_text
                )

            st.success("Website summarized successfully!")

            st.subheader(" Website Information")
            st.write(f"**Website Title:** {title}")
            st.write(f"**URL:** {url}")

            st.divider()

            st.subheader("AI Summary")
            st.markdown(summary)

            with st.expander("View extracted website text"):
                st.write(website_text[:15000])

        except requests.exceptions.RequestException as error:
            st.error(f"Could not access the website: {error}")

        except Exception as error:
            st.error(f"Something went wrong: {error}")
