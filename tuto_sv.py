
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Scientific Visualization", divider="gray")


# Define the URL of the CSV file
URL = "https://raw.githubusercontent.com/Wanioooo/tuto-SV/refs/heads/main/arts_faculty_data.csv"

# --- Streamlit App Layout ---

st.title("Arts Faculty Data: Gender Distribution")
st.markdown("Loading data and visualizing the distribution of students by gender.")

# --- Data Loading ---

@st.cache_data # Cache the data loading for better performance
def load_data(url):
    """Loads the data from a given URL into a pandas DataFrame."""
    try:
        arts_df = pd.read_csv(url)
        return arts_df
    except Exception as e:
        st.error(f"🚨 An error occurred while loading data: {e}")
        return None

arts_df = load_data(URL)

# --- Data Display (Optional) ---

if arts_df is not None:
    st.subheader("Raw Data Preview")
    st.dataframe(arts_df.head())

    # --- Plotly Visualization ---

    st.subheader("Distribution of Gender in Arts Faculty")

    # Get the value counts of the 'Gender' column
    gender_counts = arts_df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count'] # Rename columns for clarity in Plotly

    # Create a Plotly Pie Chart
    # Plotly Express makes creating interactive charts simple
    fig = px.pie(
        gender_counts,
        values='Count',
        names='Gender',
        title='Distribution of Gender in Arts Faculty',
        hole=.3, # Optional: makes it a donut chart
        color_discrete_sequence=px.colors.qualitative.Pastel # Optional: change color scheme
    )

    # Update layout for better presentation (optional)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', legend_title="Gender")

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# --- Instructions to Run ---

st.sidebar.info(
    "To run this application, save the code as a Python file (e.g., `app.py`) "
    "and execute it using the command: \n\n"
    "**`streamlit run app.py`**"
)
