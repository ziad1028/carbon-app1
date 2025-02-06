import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Title
st.title("Carbon Footprint Calculator")

# Initialize or retrieve session state for data storage
if 'data' not in st.session_state:
    st.session_state['data'] = []

# Input fields
electricity = st.number_input("Electricity Usage (kWh):", min_value=0.0)
gas = st.number_input("Gas Consumption (litres):", min_value=0.0)
miles = st.number_input("Miles Driven:", min_value=0.0)
waste = st.number_input("Waste Generated (kg):", min_value=0.0)

# Calculate button
if st.button("Calculate"):
    total = electricity * 0.233 + gas * 2.31 + miles * 0.411 + waste * 0.91
    st.write(f"Your Total Carbon Footprint: {total:.2f} kg CO2")

    # Store the result with the date
    st.session_state['data'].append({
        "date": datetime.date.today(),
        "carbon_footprint": total
    })

# Convert the stored data to a DataFrame for plotting
df = pd.DataFrame(st.session_state['data'])

# Aggregate data for daily, weekly, monthly, and yearly
if not df.empty:
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    daily_df = df.resample('D').sum()
    weekly_df = df.resample('W').sum()
    monthly_df = df.resample('M').sum()
    yearly_df = df.resample('Y').sum()

    # Function to plot data using Matplotlib
    def plot_data(df, title):
        fig, ax = plt.subplots()
        ax.plot(df.index, df['carbon_footprint'], marker='o', label='Carbon Footprint')
        ax.set_title(title)
        ax.set_xlabel("Date")
        ax.set_ylabel("Carbon Footprint (kg CO2)")
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Debug: Display the data used for plotting
        st.write(f"{title} Data:", df)

    # Plot each aggregated DataFrame
    if not daily_df.empty:
        plot_data(daily_df, "Daily Carbon Footprint")
    if not weekly_df.empty:
        plot_data(weekly_df, "Weekly Carbon Footprint")
    if not monthly_df.empty:
        plot_data(monthly_df, "Monthly Carbon Footprint")
    if not yearly_df.empty:
        plot_data(yearly_df, "Yearly Carbon Footprint")
