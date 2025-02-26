import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Gemini with correct model name
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro')  # Updated model name

def get_current_tax_summary(country: str) -> str:
    prompt = f"""
    Provide current tax rules summary for {country} (2024-25) covering:
    1. Income Tax Slabs
    2. Standard Deductions
    3. Investment Benefits
    4. Special Deductions
    5. Additional Charges (cess, surcharge)
    Format as clear bullet points.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback summary if API fails
        if country == "India":
            return """
            • New Tax Regime (2024-25):
              - Up to ₹3L: No tax
              - ₹3-6L: 5%
              - ₹6-9L: 10%
              - ₹9-12L: 15%
              - ₹12-15L: 20%
              - Above ₹15L: 30%
              
            • Standard Deduction: ₹50,000
            • 4% Health & Education Cess
            • Major Deductions:
              - 80C: Up to ₹1.5L
              - 80D: Up to ₹25,000
              - HRA: As per rules
            """
        else:
            return """
            • Federal Tax Brackets (2024):
              - 10%: Up to $11,000
              - 12%: $11,001-44,725
              - 22%: $44,726-95,375
              - Higher brackets up to 37%
              
            • Standard Deduction:
              - Single: $13,850
              - Married: $27,700
              
            • Key Benefits:
              - 401(k): $22,500 limit
              - IRA: $6,500 limit
            """

def calculate_tax(country: str, data: dict, regime: str = "New") -> dict:
    """Calculate tax based on inputs without using LLM"""
    total_income = data['basic_salary'] + data['allowances'] + data['other_income']
    
    if country == "India":
        # Indian Tax Calculation
        total_deductions = (
            (data.get('section_80c', 0) if data.get('section_80c', 0) <= 150000 else 150000) +
            (data.get('section_80d', 0) if data.get('section_80d', 0) <= 25000 else 25000) +
            min(data.get('home_loan_interest', 0), 200000) +
            data.get('medical_expenses', 0) +
            data.get('donations', 0) * 0.5  # 50% of donations
        )
        
        # Tax brackets for new regime
        if regime == "New":
            brackets = [
                (0, 300000, 0),
                (300001, 600000, 0.05),
                (600001, 900000, 0.10),
                (900001, 1200000, 0.15),
                (1200001, 1500000, 0.20),
                (1500001, float('inf'), 0.30)
            ]
        else:  # Old regime
            brackets = [
                (0, 250000, 0),
                (250001, 500000, 0.05),
                (500001, 1000000, 0.20),
                (1000001, float('inf'), 0.30)
            ]
        
        currency = "₹"
        
    else:  # USA
        # US Tax Calculation
        total_deductions = (
            min(data.get('retirement', 0), 22500) +
            min(data.get('ira', 0), 6500) +
            data.get('medical_expenses', 0) +
            data.get('donations', 0)
        )
        
        brackets = [
            (0, 11000, 0.10),
            (11001, 44725, 0.12),
            (44726, 95375, 0.22),
            (95376, 182100, 0.24),
            (182101, 231250, 0.32),
            (231251, 578125, 0.35),
            (578126, float('inf'), 0.37)
        ]
        
        currency = "$"

    # Calculate taxable income
    taxable_income = max(0, total_income - total_deductions)
    
    # Calculate tax
    total_tax = 0
    tax_breakdown = []
    remaining_income = taxable_income
    
    for min_income, max_income, rate in brackets:
        if remaining_income <= 0:
            break
            
        bracket_amount = min(
            remaining_income,
            max_income - min_income if max_income != float('inf') else remaining_income
        )
        bracket_tax = bracket_amount * rate
        total_tax += bracket_tax
        
        tax_breakdown.append({
            'bracket': f"{currency}{min_income:,} - {currency}{max_income:,}",
            'rate': f"{rate*100}%",
            'tax_amount': round(bracket_tax, 2)
        })
        
        remaining_income -= bracket_amount

    # Add education cess for India
    if country == "India":
        cess = total_tax * 0.04
        total_tax += cess
        tax_breakdown.append({
            'bracket': 'Education & Health Cess',
            'rate': '4%',
            'tax_amount': round(cess, 2)
        })

    return {
        'total_tax': round(total_tax, 2),
        'taxable_income': round(taxable_income, 2),
        'total_deductions': round(total_deductions, 2),
        'effective_rate': round((total_tax / total_income * 100), 2) if total_income > 0 else 0,
        'breakdown': tax_breakdown
    }

def main():
    st.set_page_config(page_title="Tax Calculator", page_icon="💰", layout="wide")
    st.title("Income Tax Calculator")

    # Basic Information
    country = st.selectbox("Select Country", ["India", "USA"])
    
    # Display tax rules summary
    with st.expander("Current Tax Rules Summary", expanded=True):
        summary = get_current_tax_summary(country)
        st.markdown(summary)
        st.warning("Please verify with official sources for accurate information.")

    # Income Details
    st.subheader("Income Details")
    col1, col2 = st.columns(2)
    
    with col1:
        basic_salary = st.number_input("Basic Salary (Annual)", min_value=0.0, step=1000.0)
        allowances = st.number_input("Allowances (HRA, etc.)", min_value=0.0, step=1000.0)
        
    with col2:
        other_income = st.number_input("Other Income", min_value=0.0, step=1000.0)
        if country == "India":
            regime = st.radio("Tax Regime", ["New", "Old"])

    # Deductions and Investments
    st.subheader("Deductions & Investments")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Basic Deductions")
        if country == "India":
            section_80c = st.number_input("80C Investments", min_value=0.0, max_value=150000.0, help="PPF, ELSS, etc.")
            section_80d = st.number_input("80D (Health Insurance)", min_value=0.0, max_value=25000.0)
        else:
            retirement = st.number_input("401(k) Contribution", min_value=0.0, max_value=22500.0)
            ira = st.number_input("IRA Contribution", min_value=0.0, max_value=6500.0)

    with col2:
        st.markdown("#### Housing")
        hra = st.number_input("HRA Received", min_value=0.0)
        rent_paid = st.number_input("Rent Paid", min_value=0.0)
        home_loan_interest = st.number_input("Home Loan Interest", min_value=0.0)

    with col3:
        st.markdown("#### Other Deductions")
        medical_expenses = st.number_input("Medical Expenses", min_value=0.0)
        education_expenses = st.number_input("Education Expenses", min_value=0.0)
        donations = st.number_input("Charitable Donations", min_value=0.0)

    if st.button("Calculate Tax"):
        # Collect all inputs into a data dictionary
        data = {
            'basic_salary': basic_salary,
            'allowances': allowances,
            'other_income': other_income,
            'section_80c': section_80c if country == "India" else 0,
            'section_80d': section_80d if country == "India" else 0,
            'retirement': retirement if country == "USA" else 0,
            'ira': ira if country == "USA" else 0,
            'hra': hra,
            'rent_paid': rent_paid,
            'home_loan_interest': home_loan_interest,
            'medical_expenses': medical_expenses,
            'education_expenses': education_expenses,
            'donations': donations
        }

        try:
            # Calculate tax using our function instead of LLM
            results = calculate_tax(
                country=country,
                data=data,
                regime=regime if country == "India" else "New"
            )

            # Display Results
            st.header("Tax Calculation Results")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Total Tax",
                    f"{'₹' if country == 'India' else '$'}{results['total_tax']:,.2f}"
                )
                st.metric(
                    "Effective Tax Rate",
                    f"{results['effective_rate']}%"
                )

            with col2:
                st.metric(
                    "Taxable Income",
                    f"{'₹' if country == 'India' else '$'}{results['taxable_income']:,.2f}"
                )
                st.metric(
                    "Total Deductions",
                    f"{'₹' if country == 'India' else '$'}{results['total_deductions']:,.2f}"
                )

            # Show detailed breakdown
            with st.expander("Detailed Tax Breakdown", expanded=True):
                st.table(results['breakdown'])

        except Exception as e:
            st.error("Error in tax calculation. Please check your inputs.")
            st.exception(e)

if __name__ == "__main__":
    main()
