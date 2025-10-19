import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Define the URL of the CSV file
URL = "https://raw.githubusercontent.com/Wanioooo/tuto-SV/refs/heads/main/arts_faculty_data.csv"

# --- Streamlit App Setup ---


st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Scientific Visualization", divider="gray")


st.title("🎓 Arts Faculty Student Survey Analysis")

col1, col2, col3, col4 = st.columns(4)
   
col1.metric(label="PLO 2", value=f"3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value=f"3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value=f"4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value=f"4.3", help="PLO 5: Communication Skill", border=True)

st.markdown("Exploring student demographics, academic performance, and satisfaction using Plotly visualizations.")

# --- Data Loading and Caching ---

@st.cache_data
def load_data(url):
    """Loads the data from a given URL into a pandas DataFrame."""
    try:
        arts_df = pd.read_csv(url)
        return arts_df
    except Exception as e:
        st.error(f"🚨 An error occurred while loading data: {e}")
        return None

arts_df = load_data(URL)

if arts_df is None:
    st.stop() # Stop the app if data failed to load

# Use 'df' for convenience as it was used in the original code snippets
df = arts_df.copy()

st.header("🔍 Data Preview")
st.dataframe(df)

# --- Data Preprocessing Functions (for Plotly Visualizations) ---

def clean_gpa_data(data):
    """Cleans and prepares GPA data for the line chart."""
    gpa_cols = [
        '1st Year Semester 1', '1st Year Semester 2', '1st Year Semester 3',
        '2nd Year Semester 1', '2nd Year Semester 2', '2nd Year Semester 3',
        '3rd Year Semester 1', '3rd Year Semester 2', '3rd Year Semester 3',
        '4th Year Semester 1', '4th Year Semester 2', '4th Year Semester 3'
    ]
    
    # Convert GPA columns to numeric, coercing errors to NaN
    for col in gpa_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    gpa_means = data[gpa_cols].mean().reset_index()
    gpa_means.columns = ['Semester', 'Mean GPA']

    # Clean up semester names for better plotting
    gpa_means['Semester'] = gpa_means['Semester'].str.replace(' Year Semester ', 'Y S')
    gpa_means['Semester'] = gpa_means['Semester'].str.replace('1st', '1').str.replace('2nd', '2').str.replace('3rd', '3').str.replace('4th', '4')
    
    # Define a custom order for the semesters
    semester_order = [
        '1Y S1', '1Y S2', '1Y S3',
        '2Y S1', '2Y S2', '2Y S3',
        '3Y S1', '3Y S2', '3Y S3',
        '4Y S1', '4Y S2', '4Y S3'
    ]
    # Ensure all semesters are in the order if they exist in the means
    gpa_means['Semester'] = pd.Categorical(gpa_means['Semester'], categories=semester_order, ordered=True)
    gpa_means = gpa_means.sort_values('Semester').dropna(subset=['Mean GPA'])
    
    return gpa_means


# --- Visualization Functions (using Plotly) ---
    
def plot_gender_distribution(data):
    """Creates a Plotly Pie chart for Gender Distribution."""
    gender_counts = data['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    
    fig = px.pie(
        gender_counts,
        values='Count',
        names='Gender',
        title='Gender Distribution in Arts Faculty',
        hole=.3,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    st.info(" The people who took this survey are mostly women, making up about 76% of the total. This means the overall results mainly reflect the female students' experience in the faculty. So, the opinions of male students are less represented in this feedback.")

def plot_gpa_trend(data):
    """Creates a Plotly Line chart for Mean GPA Trend."""
    gpa_means = clean_gpa_data(data.copy())
    
    fig = px.line(
        gpa_means,
        x='Semester',
        y='Mean GPA',
        markers=True,
        title='Mean GPA Trend Across Academic Semesters (Arts Faculty)',
        color_discrete_sequence=['#4c78a8'] # Blue color
    )
    fig.update_layout(
        xaxis_title='Semester',
        yaxis_title='Mean GPA',
        xaxis={'categoryorder':'array', 'categoryarray': gpa_means['Semester'].unique().tolist()}
    )
    fig.update_yaxes(gridcolor='lightgray')
    st.plotly_chart(fig, use_container_width=True)
    st.info("Student grades are very consistent over their four years, never going up or down much. This shows a stable academic environment where students maintain a steady performance level. The faculty's grading seems predictable, and students aren't facing sudden difficulty changes.")

def plot_expectation_comparison(data):
    """Creates a Plotly Box plot for Expectation vs. Satisfaction."""
    expectation_cols = [
        'Q1 [What was your expectation about the University as related to quality of education?]',
        'Q2 [What was your expectation about the University as related to quality of Faculty?]',
        'Q3 [What was your expectation about the University as related to quality of resources?]',
        'Q4 [What was your expectation about the University as related to quality of learning environment?]'
    ]
    satisfaction_col = 'Q5 [To what extent your expectation was met?]'

    # Calculate the mean expectation score
    data['Mean Expectation'] = data[expectation_cols].mean(axis=1)

    # Prepare data for boxplot
    plot_data = data[['Mean Expectation', satisfaction_col]].melt(
        value_vars=['Mean Expectation', satisfaction_col],
        var_name='Metric',
        value_name='Score'
    ).dropna() # Drop any rows where either value is NaN

    # Rename for clarity
    plot_data['Metric'] = plot_data['Metric'].replace({
        'Mean Expectation': 'Average Initial Expectation',
        satisfaction_col: 'Expectation Met Score'
    })
    
    fig = px.box(
        plot_data,
        x='Metric',
        y='Score',
        title='Comparison of Initial Expectation and Expectation Met Score',
        color='Metric', # Color by metric
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        yaxis_title='Score (1-5 Scale)',
        xaxis_title='Metric',
        yaxis_range=[1, 5.2]
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("The faculty has done a great job which is the students felt their initial hopes and expectations were met and then some. They were already optimistic coming in, but the program delivered even slightly better than expected. This is a very positive sign that the faculty is successfully living up to its promises.")

def plot_top_best_aspects(data):
    """Creates a Plotly Bar chart for the Top 5 Best Aspects."""
    aspect_column = 'Q7. In your opinion,the best aspect of the program is'
    best_aspect_counts = data[aspect_column].value_counts().head(5).reset_index()
    best_aspect_counts.columns = ['Aspect', 'Responses']

    fig = px.bar(
        best_aspect_counts,
        x='Responses', # Use Responses on the x-axis for a horizontal bar chart
        y='Aspect',
        orientation='h',
        title='Top 5 Best Aspects of the Program (According to Students)',
        color='Responses',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_layout(
        xaxis_title='Number of Responses',
        yaxis_title='Best Aspect'
    )
    fig.update_yaxes(automargin=True)
    st.plotly_chart(fig, use_container_width=True)
    st.info("The best things about this program are the professors and the way they teach. These two factors are the program's biggest strengths according to the students. Everything else, like resources or facilities, is seen as much less important than the quality of the teaching staff.")

def plot_improvement_perception_by_gender(data):
    """Creates a Plotly Grouped Bar chart for Improvement Perception."""
    q_edu = 'Do you feel that the quality of education improved at EU over the last year?'
    q_img = 'Do you feel that the image of the University improved over the last year?'

    # Calculate proportion of 'Yes' responses grouped by Gender
    improvement_df = data.groupby('Gender')[[q_edu, q_img]].apply(lambda x: (x == 'Yes').sum() / x.shape[0]).reset_index()

    # Melt the DataFrame for easier plotting
    improvement_melted = improvement_df.melt(id_vars='Gender', var_name='Question', value_name='Proportion_Yes')

    # Clean up question names for labels
    improvement_melted['Question'] = improvement_melted['Question'].replace({
        q_edu: 'Quality of Education Improved',
        q_img: 'University Image Improved'
    })

    fig = px.bar(
        improvement_melted,
        x='Question',
        y='Proportion_Yes',
        color='Gender',
        barmode='group',
        title='Perception of University Improvement: By Gender',
        labels={'Proportion_Yes': 'Proportion of Respondents who answered "Yes"', 'Question': 'Improvement Area'},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_yaxes(tickformat=".0%", range=[0, 1.0])
    st.plotly_chart(fig, use_container_width=True)
    st.info("Men and women see the university's progress differently. More men think the quality of education is getting better, while more women think the university's reputation is improving. This highlights that the two groups are noticing and prioritizing different types of positive changes at the university.")

def plot_policy_vs_implementation_ratings(data):
    """Creates a Plotly Bar chart for Average Rating: Policy vs. Implementation."""
    area_evaluation_cols = [col for col in data.columns if col.startswith('Area of Evaluation')]
    item_cols = [col for col in data.columns if col.startswith('Item')]

    # Ensure these are numeric (needed if data loading was only partial in the script)
    data[area_evaluation_cols] = data[area_evaluation_cols].apply(pd.to_numeric, errors='coerce')
    data[item_cols] = data[item_cols].apply(pd.to_numeric, errors='coerce')

    avg_area = data[area_evaluation_cols].mean(axis=1).mean()
    avg_item = data[item_cols].mean(axis=1).mean()

    plot_data = pd.DataFrame({
        'Category': ['Academic/Administrative Policy', 'Specific Teaching/Support Items'],
        'Mean Rating': [avg_area, avg_item]
    })
    
    fig = px.bar(
        plot_data,
        x='Category',
        y='Mean Rating',
        title='Average Student Rating: Policy vs. Implementation Items (Scale: 1-5)',
        color='Category',
        color_discrete_sequence=px.colors.sequential.Sunsetdark # Use a dark sequential palette
    )
    fig.update_layout(
        xaxis_title='Survey Category',
        yaxis_title='Mean Rating Score',
        yaxis_range=[3.5, 5.0]
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("Students approve of the written rules and plans (policies) more than they approve of how those rules are carried out in reality. There's a small gap here. The university should focus on improving the delivery of day-to-day things, like better resources or facilities, to match the quality of its policies.")


# --- Streamlit Layout: Columns and Sections ---

st.header("📊 Demographic and Academic Performance")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Gender Distribution")
    plot_gender_distribution(df)
with col2:
    st.subheader("Mean GPA Trend")
    plot_gpa_trend(df)

st.header("💡 Expectation and Satisfaction Analysis")

col3, col4 = st.columns(2)
with col3:
    st.subheader("Initial Expectation vs. Satisfaction")
    plot_expectation_comparison(df)
with col4:
    st.subheader("Top Best Aspects of the Program")
    plot_top_best_aspects(df)

st.header("📈 Improvement Perception and Overall Rating")

col5, col6 = st.columns(2)
with col5:
    st.subheader("Perception of University Improvement by Gender")
    plot_improvement_perception_by_gender(df)
with col6:
    st.subheader("Average Rating: Policy vs. Implementation")
    plot_policy_vs_implementation_ratings(df)


# Note: The original code contained a call to a function `plot_mean_rating_by_year(df.copy())` 
# and a few print statements which are replaced by the structured Streamlit layout and Plotly charts.
