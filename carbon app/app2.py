import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Function to plot data using Matplotlib
def plot_data(df, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df['carbon_footprint'], linestyle='-', marker='o', label='Carbon Footprint')
    
    # Set title and labels
    ax.set_title(title, fontsize=16)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Carbon Footprint (kg CO2)", fontsize=12)

    # Date formatting for x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Add grid for better readability
    ax.grid(True)

    # Add data point annotations
    for x, y in zip(df.index, df['carbon_footprint']):
        ax.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0, 5), ha='center')

    # Show legend
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Debug: Display the data used for plotting
    st.write(f"{title} Data:", df)

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

    # Plot each aggregated DataFrame
    if not daily_df.empty:
        plot_data(daily_df, "Daily Carbon Footprint")
    if not weekly_df.empty:
        plot_data(weekly_df, "Weekly Carbon Footprint")
    if not monthly_df.empty:
        plot_data(monthly_df, "Monthly Carbon Footprint")
    if not yearly_df.empty:
        plot_data(yearly_df, "Yearly Carbon Footprint")
