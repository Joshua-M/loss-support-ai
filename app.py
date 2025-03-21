import streamlit as st
from loss_calculator import calculate_loss, generate_summary
from gpt_helper import generate_gpt_explanation

st.set_page_config(page_title="Loss of Support AI", layout="centered")
st.title("⚖️ Loss of Support Calculator (SA + GPT)")
st.markdown("""
Enter details below to calculate the estimated loss of support due to a motor vehicle accident,
and receive an AI-powered explanation of the results.
""")

# --- Sidebar for Inputs ---
st.sidebar.header("📋 Claim Inputs")
accident_date = st.sidebar.date_input("Date of Accident")
calculation_date = st.sidebar.date_input("Date of Calculation")
birth_date = st.sidebar.date_input("Date of Birth")

annual_earnings = st.sidebar.number_input("Annual Earnings at Time of Accident (R)", min_value=0.0, value=100205.0)
retirement_age = st.sidebar.slider("Retirement Age", 55, 70, 65)
ceiling_earnings = st.sidebar.number_input("Ceiling Earnings (R)", min_value=0.0, value=100205.0)
discount_rate = st.sidebar.slider("Discount Rate (%)", 0.0, 10.0, 4.0) / 100
contingency = st.sidebar.slider("Contingency Deduction (%)", 0.0, 50.0, 15.0) / 100

# --- Calculate Button ---
if st.sidebar.button("Calculate Loss"):
    with st.spinner("Calculating loss and fetching GPT explanation..."):
        results = calculate_loss(
            accident_date=accident_date.strftime("%Y-%m-%d"),
            calculation_date=calculation_date.strftime("%Y-%m-%d"),
            annual_earnings=annual_earnings,
            birth_date=birth_date.strftime("%Y-%m-%d"),
            retirement_age=retirement_age,
            ceiling_earnings=ceiling_earnings,
            discount_rate=discount_rate,
            contingency=contingency
        )

        summary_text = generate_summary(results)
        explanation = generate_gpt_explanation(summary_text)

        # --- Results Display ---
        st.success("✅ Calculation Complete")
        st.subheader("📊 Results")
        st.write(results)

        st.subheader("🧠 GPT Explanation")
        st.markdown(explanation)

        # Optional download block (future enhancement)
        # st.download_button("Download Report", data=pdf_bytes, file_name="loss_report.pdf")
else:
    st.info("Use the sidebar to enter claim details and click 'Calculate Loss' to begin.")
