# Financial Analyst Agent (Streamlit Edition)

## Overview

The **Financial Analyst Agent** is an AI-powered assistant designed to automate and streamline the process of financial research and analysis for companies. Built using [CrewAI](https://github.com/joaomdmoura/crewAI), OpenAI's GPT models, and SerpAPI for web search, this project leverages autonomous agents to gather, analyze, and present financial insights in a user-friendly Streamlit web application.

## Key Objectives

- **Automate Financial Research:** Reduce manual effort in collecting and analyzing financial statements and market data.
- **Leverage AI Agents:** Use specialized agents for market research and financial strategy, each with distinct roles and expertise.
- **Provide Actionable Insights:** Deliver comprehensive financial analysis and strategic recommendations for any company.
- **User-Friendly Interface:** Enable users to interact with the system through a simple web interface, requiring only the company name as input.

## Features

- **Streamlit Web App:** Interactive UI for entering company names and viewing results.
- **Autonomous Agents:**
  - **Market Researcher:** Gathers up-to-date financial statements, market trends, and competitive landscape using web search.
  - **Financial Strategist:** Analyzes gathered data to produce detailed financial reports and strategic recommendations.
- **Web Search Integration:** Uses SerpAPI to fetch the latest financial documents and news.
- **Comprehensive Analysis:** Covers income statements, balance sheets, cash flow, liquidity, solvency, profitability, efficiency, and market analysis.
- **Secure API Key Management:** Loads sensitive credentials from a `.env` file for security.
- **Robust SSL Handling:** Handles SSL certificate issues for seamless API access in various network environments.

## How It Works

1. **User Input:** Enter the company name in the Streamlit app.
2. **Market Research:** The Market Researcher agent collects relevant financial data and market insights.
3. **Financial Analysis:** The Financial Strategist agent analyzes the data and generates a comprehensive report.
4. **Results Displayed:** The app presents the analysis and recommendations directly in the browser.

## Getting Started

1. **Install Requirements:**
   - Python 3.8+
   - `pip install -r requirements.txt`
2. **Set Up Environment Variables:**
   - Create a `.env` file with your `OPENAI_API_KEY` and `SERPER_API_KEY`.
3. **Run the App:**
   - `streamlit run hackathon/FinancialAnalystAgent-Streamlit.py`
4. **Use the App:**
   - Enter a company name and click "Run Financial Analysis" to get instant insights.

---

*This project was developed for a hackathon to showcase the power of autonomous AI agents in financial analysis