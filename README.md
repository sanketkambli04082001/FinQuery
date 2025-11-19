# FinQuery 📊🤖— AI-Powered Financial Report Analyzer

## Overview

**FinQuery** is an AI-powered financial analysis tool that transforms lengthy annual and quarterly PDF reports into clear, beginner-friendly insights.

It automatically generates:

- 📄 Executive summaries  
- 🏢 Competitor insights  
- 📊 Revenue charts (annual/quarterly)  
- ❓ Interactive question-answering based on the PDF  

Designed for users who want quick, reliable financial understanding without reading 100+ page documents.

---

## Features ✨

- **AI-Powered Summary Generation**  
  Extracts the most important financial highlights using Gemini AI.

- **Competitor Detection & Market Stats**  
  Identifies competitor companies and fetches market metrics like:
  - P/E ratio
  - Market cap
  - Current stock data

- **Automatic Revenue Charting**  
  Detects revenue tables from PDFs → generates plots with Matplotlib.

- **PDF-Grounded Q&A**  
  Ask any question based on the uploaded report — the system answers ONLY using the PDF content.

- **Clean Frontend UI**  
  Built with Flask, HTML, CSS, Bootstrap, and Jinja templates.

- **Beginner-Friendly Output**  
  All financial terms are simplified for users new to finance.

---

## Tech Stack 💻

**Backend & AI:**  
- Python 
- Flask 
- Gemini AI 
- PyMuPDF 
- yfinance 
- Alpha Vantage API  

**Frontend:**  
- HTML5 
- CSS3 
- Bootstrap 
- Jinja2  

**Data Visualization:**  
- Matplotlib  

---

## Folder Structure 📁

```
FinQuery/
│
├── app.py
├── main.py
├── requirements.txt
├── .gitignore
│
├── finquery/
│   ├── analyzer.py
│   ├── database.py
│   ├── fetcher.py
│   ├── visualizer.py
│   └── __init__.py
│
├── static/
│   ├── css/
│   │   └── site.css
│   └── charts/         # auto-generated revenue charts
│
├── templates/
│   ├── index.html
│   └── report.html
│
└── Reports for testing/   # (optional sample PDFs)
```
---

## Screenshots 📸

### Upload Page  
<img width="1905" height="957" alt="image" src="https://github.com/user-attachments/assets/e353a14b-b948-4590-9597-a93b6bcd74ac" />


### Summary + Competitors  
<img width="1363" height="810" alt="image" src="https://github.com/user-attachments/assets/84d679f5-8fe2-4aa7-ace1-5e44b1bccbe7" />


### Revenue Chart  
<img width="883" height="622" alt="image" src="https://github.com/user-attachments/assets/4e5d4d27-1d91-442c-b19d-0ae3c1039e1c" />

### Q&A Section  
<img width="879" height="489" alt="image" src="https://github.com/user-attachments/assets/89031302-3042-4228-9a84-04d42b660682" />

---

## About the Project 💡

FinQuery was built as a real-world capstone project showcasing:

- Prompt engineering for finance
- End-to-end PDF analysis pipelines
- Financial data analysis  
- Data cleaning and visualization
- Full-stack Flask development  
- Clean UI/UX design  

It demonstrates the ability to build an **end-to-end AI-driven product from scratch**.

---

# ⚙️ Quick Installation Guide (Optional)

> Only for developers who want to run FinQuery locally.

### 1️⃣ Clone the repository

```bash
git clone https://github.com/sanketkambli04082001/FinQuery.git
cd FinQuery
```

2️⃣ Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate       # Windows
# or
source venv/bin/activate   # Mac/Linux
```

3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

4️⃣ Add your API keys

Create a .env file:

```bash
GOOGLE_API_KEY=your_gemini_key
ALPHA_VANTAGE_KEY=your_alpha_vantage_key
```

5️⃣ Run the Application
```bash
python app.py
```


## 👤 Author

<table>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/b2087320-3c3e-45e8-837a-d795de714f42" width="120" style="border-radius: 12px;" />
    </td>
    <td style="padding-left: 15px;">
      <b>Sanket Kambli</b><br>
      Python & AI Developer<br>
      <a href="https://www.linkedin.com/in/sanket-kambli-6bb012223" target="_blank">LinkedIn Profile</a><br>
      <a href="mailto:sanketkambli04082001@gmail.com">sanketkambli04082001@gmail.com</a>
    </td>
  </tr>
</table>

