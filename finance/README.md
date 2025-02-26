# AI Tax Calculator

## Overview
A streamlined tax calculation system that combines traditional tax computation with AI-powered insights for India and USA tax regimes.

## Features
- 🌍 Supports Indian and US tax systems
- 🤖 AI-powered tax rule summaries
- 💰 Comprehensive income and deduction fields
- 📊 Detailed tax breakdown
- 🔄 Multiple tax regime support (India)
- 💡 Real-time calculations

## Setup

1. **Prerequisites**
   ```bash
   Python 3.8 or higher
   pip (Python package manager)
   ```

2. **Installation**
   ```bash
   # Clone the repository
   git clone [your-repository-url]
   cd finance

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configuration**
   - Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update `config.py` with your API key

4. **Running the Application**
   ```bash
   streamlit run tax_calculator_app.py
   ```

## Usage

1. **Select Country**
   - Choose between India and USA

2. **View Tax Rules**
   - Check current tax rules summary
   - Review applicable deductions

3. **Enter Income Details**
   - Basic Salary
   - Allowances
   - Other Income

4. **Input Deductions**
   ### India
   - Section 80C investments (up to ₹1.5L)
   - Section 80D health insurance
   - HRA and rent details
   - Home loan interest

   ### USA
   - 401(k) contributions
   - IRA contributions
   - Medical expenses
   - Charitable donations

5. **Calculate Tax**
   - Get instant tax calculation
   - View detailed breakdown
   - See effective tax rate

## Project Structure

finance/
├── tax_calculator_app.py   # Main application file
├── config.py              # Configuration and API keys
├── requirements.txt       # Project dependencies
└── README.md             # Documentation

## Technical Details

Framework: Streamlit
AI Integration: Google Gemini AI
Key Libraries:
streamlit
google-generativeai
python-dotenv

## Error Handling


Fallback tax summaries if AI service is unavailable
Input validation for deduction limits
Clear error messages for API issues
Graceful degradation of features


## Security Note


API keys should be kept confidential
User data is processed locally
No data is stored or transmitted
##  Limitations


Tax calculations are approximate
Always verify with a tax professional
Rules may change with tax years
Limited to basic tax scenarios
