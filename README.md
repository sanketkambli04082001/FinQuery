# FinQuery 📊🤖

## Description

**FinQuery** is an AI-powered Financial Analysis System that converts complex annual and quarterly PDF reports into clear, actionable insights. It automatically generates **executive summaries**, **competitor insights**, **revenue charts**, and an interactive **Q&A analysis**, all inside a clean Flask web interface.

Built using **Python**, **Flask**, **Gemini AI**, **yfinance**, **PyMuPDF**, and **Matplotlib**, this system helps beginners, investors, analysts, and students quickly understand financial reports without manually reading hundreds of pages.

FinQuery follows an end-to-end pipeline:  
**PDF → Extract → Summarize → Analyze → Visualize → Q&A**.

---

## Features

- 📄 **AI-Generated Executive Summary**  
  Produces clear, beginner-friendly summaries with accurate financial explanations.

- 🏢 **Competitor Detection & Market Stats**  
  Identifies competitors using Gemini AI and fetches their metrics (P/E, MarketCap).

- 📊 **Automatic Revenue Charts**  
  Detects annual or quarterly revenue tables and renders bar charts via Matplotlib.

- ❓ **Smart Q&A System**  
  Ask questions about the report — answers come only from the report text using a tri-chunk PDF technique.

- 🎨 **Clean Flask UI**  
  Built with HTML, CSS, Bootstrap & Jinja2 for a smooth user experience.

- 🔐 **Secure API Management**  
  Uses `.env` for your Gemini API key.

---

## Core Technologies

- **Backend / AI:**  
  Python • Flask • Gemini AI • yfinance • Alpha Vantage API • PyMuPDF • Matplotlib

- **Frontend:**  
  HTML5 • CSS3 • Bootstrap • Jinja2 Templates

- **Tools:**  
  Git • GitHub • Virtualenv

---

## Screenshots

> Replace these with your actual project screenshots

### 📥 Upload Page  
![Upload Screenshot](your_image_url_here)

### 📈 Revenue Chart  
![Chart Screenshot](your_image_url_here)

### 🧠 AI Summary + Q&A  
![Summary Screenshot](your_image_url_here)

---

## Installation & Setup

Clone the repository:

```bash
git clone https://github.com/sanketkambli04082001/FinQuery.git
cd FinQuery
