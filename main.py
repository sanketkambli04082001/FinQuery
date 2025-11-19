from finquery.fetcher import DataFetcher
from finquery.analyzer import ReportAnalyzer
from finquery.visualizer import DataVisualizer
from finquery.database import DataBaseManager

import json
import os

if __name__ == "__main__":
    print("----Running FinQuery Test----")
    fetcher = DataFetcher()
    analyzer = ReportAnalyzer()
    visualizer = DataVisualizer()
    db = DataBaseManager()


    report_data = {
        "ticker" : "UNKNOWN",
        "summary" : "",
        "competitors" : [],
        "chart_filename": "none"
    }

    pdf_path = "JIO_report.pdf"
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        exit()

# ---------------------------------------------------------------------------------------------------------------
# Phase 1 : Analyzing the user's PDF
# ---------------------------------------------------------------------------------------------------------------
    print("*" * 100)
    print(f"\n[Phase 1] Reading and analyzing {pdf_path}...")

    pdf_text = analyzer.extract_text_from_pdf(pdf_path)

    if pdf_text:
        print(f"\n --- Successfully extracted {len(pdf_text)} characters from PDF ---")
        print("-" * 100)

        print(" --> Generating AI summary...")
        pdf_summary = analyzer.summarize_text(pdf_text[:10000])
        report_data["summary"] = pdf_summary

        print("\n=== EXECUTIVE SUMMARY ===")
        print(pdf_summary)
        print("=========================\n")
    else:
        print("--- PDF Extraction Failed ---")
        exit()


    print("\n --- Test Completed ---") 
    
# ---------------------------------------------------------------------------------------------------------------
# Phase 2 : Competitors data
# ---------------------------------------------------------------------------------------------------------------
    print("*" * 100)
    print("\n[Phase 2] Identifying competitors...")

    # competitors = analyzer.get_competitors(pdf_text[:10000])
    # if not competitors:
    #     print(" -> Could not identify any competitors. Ending workflow.")
    #     exit()

    # print(f" -> AI identified these competitors: {competitors}")
    # print("-" * 100)
    # print("\n--- Gathering Competitor Data ---")
    # print("-" * 100)

    # for ticker in competitors:
    #     print(f" -> Fetching data for {ticker}...")
    #     data = fetcher.get_company_overview(ticker)
    #     if data:
    #         print(f"    [SUCCESS] Got data for {ticker}")
    #         print(f"    - P/E Ratio: {data.get('PERatio', 'N/A')}")
    #         print(f"    - Market Cap: {data.get('MarketCapitalization', 'N/A')}")
    #     else:
    #          print(f"    [FAILED] Could not fetch data for {ticker}")

    company_info = analyzer.get_competitors(pdf_text[:15000])
    report_data["ticker"] = company_info.get("main_ticker", "UNKNOWN")
    competitors = company_info.get("competitors", [])
    report_data["competitors"] = competitors 

    print(f" -> Main Company: {report_data['ticker']}")
    print(f" -> Competitors: {competitors}")
    
    if competitors:
        print("\n--- Gathering Competitor Data ---")
        for ticker in competitors:
            print(f" -> Fetching data for {ticker}...")
            data = fetcher.get_company_overview(ticker)
            if data:
                 print(f"    [SUCCESS] {ticker} P/E: {data.get('PERatio', 'N/A')}")
            else:
                 print(f"    [FAILED] Could not fetch data for {ticker}")
            print("-" * 30)
    else:
        print(" -> No competitors found to research.")

    print("*" * 100)

# ---------------------------------------------------------------------------------------------------------------
# Phase 3 : Query analyzer (Interactive Q&A)
# ---------------------------------------------------------------------------------------------------------------
    print("\n[Phase 3] Starting Interactive Q&A...")
    print("You can now ask questions about the PDF. Type 'exit' to stop.")

    while True:
        print("'exit', 'quit', 'stop' to end")
        user_question = input("\nYour Question: ")
        if user_question.lower() in ['exit', 'quit', 'stop']:
            break
        answer = analyzer.answer_question(pdf_text[:20000], user_question)
        print("\n>>> AI Answer:")
        print(answer)
        print("-" * 100)

# ---------------------------------------------------------------------------------------------------------------
# Phase 4 : Chart Analysis
# ---------------------------------------------------------------------------------------------------------------
    print("*" * 100)
    print("\n[Phase 4] Generating Financial Chart...")
    chart_data = analyzer.extract_financial_table(pdf_text[:20000])
    if chart_data:
        print(f" -> Successfully extracted data for chart: {chart_data}")
        chart_filename = f"{report_data['ticker']}_revenue_chart.png"
        report_data["chart_filename"] = chart_filename
        keys = list(chart_data.keys())
        if keys and str(keys[0]).upper().startswith("Q"):
            chart_title = "Quarterly Revenue (Cr)"
        else:
            chart_title = "Annual Revenue (Cr)"

        if visualizer.create_bar_chart(chart_data, chart_title, chart_filename):
            print(f" -> Chart saved to your project folder as: {chart_filename}")
        else:
            print(" -> Failed to create chart.")
    else:
        print(" -> Could not extract table data for chart.")


# ---------------------------------------------------------------------------------------------------------------
# Phase 5 : Database
# ---------------------------------------------------------------------------------------------------------------
    print("*" * 100)
    print("\n[Phase 5] Archiving Report...")
    db.save_report(report_data)

print("*" * 100)
print("\n--- Workflow Complete ---")