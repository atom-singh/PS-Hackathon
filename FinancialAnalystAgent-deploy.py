## Project Overview
'''
This project is an Ai-powered Streamlit application designed to assist designed to automate 
and streamline the process of financial research and analysis for companies.
It utilizes AI agents 
to gather market insights and develop effective financial planning & strategies based on user input.

Agent 01: 
 name: Market Researcher
 task: gather_market_insight

Agent 02: 
 name: Finance Strategist
 task: develop_financial_strategy
'''

import os
import ssl
import urllib3
import requests
import streamlit as st
from dotenv import load_dotenv

from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

# --- SSL and HTTP settings ---
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    os.environ["CURL_CA_BUNDLE"] = ""
    os.environ["REQUESTS_CA_BUNDLE"] = ""
    os.environ["SSL_VERIFY"] = "false"
    os.environ["PYTHONHTTPSVERIFY"] = "0"
    os.environ["HTTPX_VERIFY"] = "false"
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception as e:
    st.warning(f"Could not configure SSL settings: {e}")

# --- Load environment variables ---


# 🗝️ Load API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
serper_api_key = st.secrets["SERPER_API_KEY"]

# --- Custom Web Search Tool ---
class WebSearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Search the web for current information and trends using SerpAPI"
    def __init__(self):
        super().__init__()
    def _run(self, query: str) -> str:
        api_key = serper_api_key
        base_url = "https://serpapi.com/search"
        if not api_key:
            return f"Search results for '{query}': [No SERPER_API_KEY provided in .env file.]"
        try:
            params = {
                'q': query,
                'api_key': api_key,
                'engine': 'google',
                'num': 5
            }
            response = requests.get(base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                if 'organic_results' in data and data['organic_results']:
                    for result in data['organic_results'][:5]:
                        title = result.get('title', 'N/A')
                        snippet = result.get('snippet', 'N/A')
                        url = result.get('link', 'N/A')
                        results.append(f"Title: {title}\nSnippet: {snippet}\nURL: {url}")
                    return "\n\n".join(results)
                else:
                    return f"No search results found for '{query}'"
            else:
                return f"Search failed with status code: {response.status_code}. Response: {response.text}"
        except requests.exceptions.Timeout:
            return f"Search timeout for query: '{query}'. Please try again."
        except requests.exceptions.RequestException as e:
            return f"Search request error for '{query}': {str(e)}"
        except Exception as e:
            return f"Unexpected error during search for '{query}': {str(e)}"

# --- Streamlit UI ---
st.set_page_config(page_title="Financial Analyst Agent", layout="wide")
st.title("📊 Financial Analyst Agent")

if not openai_api_key:
    st.error("OpenAI API key not found. Please check your .env file.")
    st.stop()

company_name = st.text_input("Enter the company name for financial research:")

if company_name:
    strategist_backstory = "Experienced in evaluation of a company’s financial performance over time and against its peers."
    search_tool = WebSearchTool()

    market_researcher = Agent(
        role="Market Researcher",
        goal="Analyze market and gather reliable data for financial strategy",
        backstory="Experienced in market research and data collection with access to current web data",
        tools=[search_tool],
        verbose=True,
    )

    finance_strategist = Agent(
        role="Financial Strategist",
        goal="Evaluate a company's financial health and performance for strategic planning",
        backstory=f"skilled in analysis of major financial statements and {strategist_backstory}",
        provider="openai",
        api_key=openai_api_key,
        model="gpt-4",
        verbose=True,
    )

    gather_market_insight_task = Task(
        description=f"Use the web search tool to gather key financial statements namely Balance sheets, Income statements, and Cash flow statements for last two years, current market insights and competitive landscape for {company_name}. Search for recent market reports, consumer behavior studies, and industry news related to {company_name}.",
        expected_output=f"Accurate and officially released financial statements namely Balance sheets, Income statements, and Cash flow statements for last two years relevant to {company_name}, based on recent web search results.",
        agent=market_researcher,
        verbose=True,
    )

    develop_financial_strategy_task = Task(
        description="Based on the market insights gathered, "
        f"create a detailed financial analysis and strategy for the {company_name} company. Include Financial Statements Analysis: Income Statements, Balance Sheet & Cash FLow Statement, Liquidity Analysis, Solvency Analysis, Profitability Analysis, Efficiency Analysis, Market Analysis.",
        expected_output="A comprehensive financial analysis & strategy document with target audience definition, competitive analysis, value proposition, and market impact notes",
        agent=finance_strategist,
        verbose=True,
    )

    crew = Crew(
        agents=[market_researcher, finance_strategist],
        tasks=[gather_market_insight_task, develop_financial_strategy_task],
        planning=True
    )

    if st.button("Run Financial Analysis"):
        with st.spinner("Running agents and gathering insights..."):
            try:
                result = crew.kickoff()
                st.success("Analysis complete!")
                st.markdown("### Financial Analysis & Strategy")
                st.text(result)
            except Exception as e:
                st.error(f"Error running analysis: {e}")
else:
    st.info("Please enter a company name to begin the financial analysis.")