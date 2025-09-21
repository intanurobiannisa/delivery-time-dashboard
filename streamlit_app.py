import streamlit as st
import pandas as pd
import altair as alt

st.title("🍱🛍️📦 Courier Delivery Time Analysis")
st.write(
    """Created by Intan Nur Robi Annisa – student of Data Science and Data Analyst Bootcamp at Dibimbing.  
    [LinkedIn Profile](https://www.linkedin.com/in/intannurrobiannisa)"""
)

# Load the data from a CSV
@st.cache_data
def load_data():
    df = pd.read_csv("data/df_da.csv")
    return df

df = load_data()

st.subheader("Preview")
st.write(
    """Analyzing food delivery times is essential to provide accurate estimates, manage customer expectations, and reduce frustration."""
)

st.subheader("Brief Summary")
st.write(
    """The data reveals that delivery time is most strongly influenced by distance, with a correlation of 0.78, making it the dominant factor. 
    Clear weather and low traffic consistently lead to faster deliveries, while snowy conditions and high traffic significantly increase delays. 
    Scooters emerge as the most efficient vehicle type, showing the lowest and most consistent delivery times. 
    Night deliveries tend to be slightly quicker than other times of day, and courier experience shows a modest impact—performance improves gradually, peaking around year two. 
    Overall, delivery times are relatively stable, ranging between 53 and 61 minutes, suggesting a well-controlled operational environment with a few key levers for optimization."""
)

# Show a multiselect widget with the industry sector using `st.multiselect`.
vehicle = st.multiselect(
    "Courier Vehicle Type",
    df.Vehicle_Type.unique(),
)

# Filter the DataFrame based on selection
if vehicle:
    filtered_df = df[df.Vehicle_Type.isin(vehicle)]
else:
    filtered_df = df  # Show all data if nothing is selected

# Display the filtered data as a table
with st.expander("Display DataFrame"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Weather",
    "Traffic Level",
    "Delivery Time",
    "Vehicle Type"
])

with tab1:
    # Weather Distribution
    st.subheader("Total Delivery by Weather Condition")
    weather_counts = filtered_df['Weather'].value_counts().reset_index()
    weather_counts.columns = ['Weather', 'count']
    # Find the weather type with the maximum count
    max_weather = weather_counts.loc[weather_counts['count'].idxmax()]
    st.markdown(
        f"Most common weather condition: {max_weather['Weather']} with {max_weather['count']} total deliveries."
    )
    weather_chart = alt.Chart(weather_counts).mark_bar().encode(
        x=alt.X('count:Q', title='Number of Deliveries'),
        y=alt.Y('Weather:O', title=None),
        color=alt.Color('Weather:N', title='Weather'),
        tooltip=['Weather', 'count']
    )
    st.altair_chart(weather_chart, use_container_width=True)

with tab2:
    # Traffic Level Distribution
    st.subheader("Total Delivery by Traffic Level")
    traffic_counts = filtered_df['Traffic_Level'].value_counts().reset_index()
    traffic_counts.columns = ['Traffic_Level', 'count']
    traffic_counts = traffic_counts.sort_values('Traffic_Level')
    # Find the traffic level with the maximum count
    max_traffic = traffic_counts.loc[traffic_counts['count'].idxmax()]
    st.markdown(
        f"The most common traffic level: {max_traffic['Traffic_Level']} traffic with {max_traffic['count']} total deliveries."
    )
    traffic_chart = alt.Chart(traffic_counts).mark_bar().encode(
        x=alt.X('Traffic_Level:O', title='Traffic Level', axis=alt.Axis(labelAngle=360)),
        y=alt.Y('count:Q', title='Number of Deliveries'),
        color=alt.Color('count:Q', scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=['Traffic_Level', 'count']
    )
    st.altair_chart(traffic_chart, use_container_width=True)

with tab3:
    # Delivery Time Distribution
    st.subheader("Total Delivery by Delivery Time of Day")
    dt_counts = filtered_df['Time_of_Day'].value_counts().reset_index()
    dt_counts.columns = ['Time_of_Day', 'count']
    dt_counts = dt_counts.sort_values('Time_of_Day')
    # Find the delivery time with the maximum count
    max_dt = dt_counts.loc[dt_counts['count'].idxmax()]
    st.markdown(
        f"The most common delivery time: {max_dt['Time_of_Day']} with {max_dt['count']} total deliveries."
    )
    dt_chart = alt.Chart(dt_counts).mark_bar().encode(
        x=alt.X('Time_of_Day:O', title='Delivery Time of Day', axis=alt.Axis(labelAngle=360)),
        y=alt.Y('count:Q', title='Number of Deliveries'),
        color=alt.Color('count:Q', scale=alt.Scale(scheme='greens'), legend=None),
        tooltip=['Time_of_Day', 'count']
    )
    st.altair_chart(dt_chart, use_container_width=True)

with tab4:
    # Vehicle Type Distribution
    st.subheader("Total Delivery by Vehicle Type")
    vehicle_counts = filtered_df['Vehicle_Type'].value_counts().reset_index()
    vehicle_counts.columns = ['Vehicle_Type', 'count']
    vehicle_counts = vehicle_counts.sort_values('Vehicle_Type')
    # Find the vehicle type with the maximum count
    max_vehicle = vehicle_counts.loc[vehicle_counts['count'].idxmax()]
    st.markdown(
        f"Most common vehicle type used by the courier: {max_vehicle['Vehicle_Type']} with {max_vehicle['count']} total deliveries."
    )
    vehicle_chart = alt.Chart(vehicle_counts).mark_bar().encode(
        y=alt.Y('Vehicle_Type:O', title=None, axis=alt.Axis(labelAngle=360)),
        x=alt.X('count:Q', title='Number of Deliveries'),
        color=alt.Color('Vehicle_Type:N', title='Vehicle Type'),
        tooltip=['Vehicle_Type', 'count']
    )
    st.altair_chart(vehicle_chart, use_container_width=True)

st.subheader("Findings")
st.write(
    """\n
    Clear weather yields the fastest deliveries, lowest median and tight spread.\n
    Snowy conditions show the highest median and widest spread, meaning delays are common and unpredictable.\n
    High traffic increases both median and variability.\n
    Night deliveries have a slightly lower median (~60 mins), possibly due to less traffic and fewer orders.\n
    Scooters and Bike have similar median time, but Scooters have tightest spread means they’re fast and consistent.
"""
)

st.subheader("💡 Recommendation")
st.write(
    "1. Optimize for Short-Distance Deliveries:\n" \
    "Prioritize routing and batching nearby orders. Consider dynamic pricing to encourage short-distance requests.\n" \
    "2. Streamline Preparation Time:\n" \
    "Improve kitchen workflows, automate order prep alerts, and pre-batch high-frequency items.\n" \
    "3. Deploy Scooters Strategically:\n" \
    "Assign scooters to high-density zones or time-sensitive deliveries, especially during peak hours."
)

st.markdown("<small>Code Reference: https://github.com/intanurobiannisa/delivery-time-dashboard/</small>", unsafe_allow_html=True)