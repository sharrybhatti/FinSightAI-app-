# utils.py

import os
from dotenv import load_dotenv
from sec_api import QueryApi, ExtractorApi # Assuming sec_api is installed

load_dotenv()
# 🔐 Set SEC API Key
sec_api_key = os.getenv('SEC_API_KEY')

# Global variable for SEC API key (ensure it's loaded from .env or set securely)
# For this example, we'll assume it's set in the environment or passed.
# If you have it hardcoded or in .env, ensure it's accessible.
# sec_api_key = os.getenv("SEC_API_KEY") # Or hardcode it here for testing if needed

def get_filings(ticker: str, sec_api_key: str) -> tuple[str, str]:
    """
    Fetches the most recent 10-K filing for a given stock ticker.
    Extracts Section 1A (Risk Factors) and Section 7 (Management Discussion).
    
    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").
        sec_api_key (str): Your SEC API key.

    Returns:
        - combined_text (str): Combined content from both sections
        - filing_url (str): URL of the original SEC filing
    """
    if not sec_api_key:
        print("SEC API Key not provided. Using placeholder data.")
        # Consolidated Placeholder data
        placeholder_data = {
            "AAPL": {
                "text": "Apple Inc. (AAPL) designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells related services. The Company's products include iPhone, Mac, iPad, AirPods, Apple TV, Apple Watch, Beats products, HomePod, and iPod touch. Apple also offers various services such as AppleCare, iCloud, and licensing. Its fiscal year ends in September. Key risks include intense competition, reliance on third-party manufacturers, and supply chain disruptions. Recent financials show strong revenue growth in services and wearable segments, despite some slowdown in iPhone sales.",
                "url": "https://www.sec.gov/Archives/edgar/data/320193/000032019323000066/aapl-20230930.htm"
            },
            "MSFT": {
                "text": "Microsoft Corporation (MSFT) develops and supports software, services, devices, and solutions worldwide. The Company's segments include Productivity and Business Processes, Intelligent Cloud, and More Personal Computing. Its products include Office, Exchange, SharePoint, Teams, Skype, Azure, Windows, Xbox, Surface, and LinkedIn. Microsoft faces risks from cybersecurity threats, regulatory changes, and economic downturns. Financial results highlight strong performance in cloud services (Azure) and enterprise software, indicating a shift towards subscription-based models.",
                "url": "https://www.sec.gov/Archives/edgar/data/789019/000162828023035315/msft-20230630.htm"
            },
            "TSLA": {
                "text": "Tesla, Inc. (TSLA) designs, manufactures, and sells electric vehicles and energy generation and storage systems. Its automotive products include Model 3, Model Y, Model S, and Model X. It also offers solar energy generation and energy storage products. Risks include intense competition in the EV market, supply chain challenges, and regulatory hurdles. Recent reports indicate increased vehicle deliveries and expansion of manufacturing capacity, alongside investments in charging infrastructure and AI for autonomous driving.",
                "url": "https://www.sec.gov/Archives/edgar/data/1318605/000162828023035905/tsla-20231231.htm"
            }
        }
        
        data = placeholder_data.get(ticker)
        if data:
            return data["text"], data["url"]
        else:
            text = f"No filing data available for {ticker} in this example."
            url = "N/A"
            return text, url

    
    # If SEC API key is available, use the actual API
    queryApi = QueryApi(api_key=sec_api_key)
    extractorApi = ExtractorApi(api_key=sec_api_key)

    # Define query for latest 10-K filing
    query = {
        "query": f"ticker:{ticker} AND formType:\"10-K\"",
        "from": "0",
        "size": "1",
        "sort": [{ "filedAt": { "order": "desc" } }]
    }

    # Retrieve filing metadata
    filings = queryApi.get_filings(query)
    if not filings.get("filings"):
        print(f"No 10-K filings found for ticker: {ticker}. Using placeholder data.")
        # Fallback to placeholder if no filings found via API
        return get_filings(ticker, None) # Call self with None key to get placeholder

    # Get the filing URL
    filing_url = filings["filings"][0]["linkToFilingDetails"]

    # Extract relevant sections
    section_1a = ""
    try:
        section_1a = extractorApi.get_section(filing_url, "1A", "text")
    except Exception as e:
        print(f"Warning: Could not extract Section 1A for {ticker} from {filing_url}: {e}")

    section_7 = ""
    try:
        section_7 = extractorApi.get_section(filing_url, "7", "text")
    except Exception as e:
        print(f"Warning: Could not extract Section 7 for {ticker} from {filing_url}: {e}")

    # Combine sections with headers
    combined_text = (
        f"--- Section 1A: Risk Factors ---\n{section_1a}\n\n"
        f"--- Section 7: Management Discussion ---\n{section_7}"
    )

    return combined_text, filing_url
