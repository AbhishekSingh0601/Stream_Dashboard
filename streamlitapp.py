
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Cache the data loading function
@st.cache_data
def load_data():
    # Load the dataset
    df = pd.read_csv('D:\Assignment_streamlit\github_dataset.csv')  # Update with the correct path

    # Clean up column names (remove any leading/trailing spaces)
    df.columns = df.columns.str.strip()

    return df

# Load the data
df = load_data()

# Display column names and first few rows for debugging
st.write("### Columns in the dataset:")
st.write(df.columns)

st.write("### Preview of the Dataset:")
st.write(df.head())

# Step 1: Ensure all necessary columns are present
required_columns = ['repositories', 'stars_count', 'forks_count', 'issues_count', 'pull_requests', 'contributors', 'language']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing required columns: {', '.join(missing_columns)}")
else:
    st.success("All required columns are present!")

# Step 2: Handle missing values

# Check for missing data and allow the user to decide how to handle it
st.sidebar.header("Handle Missing Data")
fill_option = st.sidebar.radio("How do you want to handle missing values?", ("Drop Rows", "Fill with Default"))

if fill_option == "Drop Rows":
    # Drop rows with missing values in critical columns
    df = df.dropna(subset=['stars_count', 'forks_count', 'language'])
    st.warning("Rows with missing values in 'stars_count', 'forks_count', or 'language' have been dropped.")
else:
    # Fill missing values with default values
    df['stars_count'] = df['stars_count'].fillna(0)  # Filling numeric columns with 0
    df['forks_count'] = df['forks_count'].fillna(0)
    df['language'] = df['language'].fillna('Unknown')  # Filling categorical column with 'Unknown'
    st.info("Missing values have been filled with default values: 0 for numeric columns and 'Unknown' for language.")

# Step 3: Sidebar filters and interactivity
st.sidebar.header('Filter Options')

# Filter by programming language (dropdown)
languages = df['language'].dropna().unique()  # Remove NaN values from language column
selected_language = st.sidebar.selectbox('Select Programming Language', ['All'] + list(languages))

# Filter by star range (slider) - Make sure to use the correct column names
min_stars, max_stars = st.sidebar.slider(
    'Select star range',
    min_value=int(df['stars_count'].min()),
    max_value=int(df['stars_count'].max()),
    value=(int(df['stars_count'].min()), int(df['stars_count'].max()))
)

# Apply the filters
if selected_language != 'All':
    df = df[df['language'] == selected_language]

df = df[(df['stars_count'] >= min_stars) & (df['stars_count'] <= max_stars)]

# Step 4: Visualizations

# Display Summary Stats
st.write(f"### Showing {len(df)} repositories with stars between {min_stars} and {max_stars}")
st.write("#### Dataset Summary")
st.write(df.describe())

# **Stars vs Forks - Plotly Scatter Plot**
st.subheader('Stars vs Forks (Interactive Plotly Scatter Plot)')

fig = px.scatter(df, x='stars_count', y='forks_count', color='language', hover_data=['repositories', 'language', 'stars_count', 'forks_count'],
                 title="Stars vs Forks by Language")
st.plotly_chart(fig)

# **Top 10 Repositories by Stars - Matplotlib Bar Plot**
st.subheader('Top 10 Repositories by Stars')

top_repositories = df.sort_values(by='stars_count', ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_repositories['repositories'], top_repositories['stars_count'], color='skyblue')
ax.set_xlabel('Stars')
ax.set_title('Top 10 GitHub Repositories by Stars')
st.pyplot(fig)

# **Most Popular Programming Languages - Plotly Bar Chart**
st.subheader('Most Popular Programming Languages')

language_counts = df['language'].value_counts()
fig = px.bar(language_counts, x=language_counts.index, y=language_counts.values,
             title="Most Popular Programming Languages", labels={'x': 'Programming Language', 'y': 'Number of Repositories'})
st.plotly_chart(fig)

# Step 5: Display Raw Data Option
if st.checkbox('Show Raw Data'):
    st.write("### Raw Data")
    st.write(df)
