import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Greywater Awareness Hub",
    page_icon="💧",
    layout="wide"
)


# ---------------------------------------------------
# LOAD DATASETS
# ---------------------------------------------------

greywater_df = pd.read_csv(
    "data/countries_greywater.csv"
)

plumbing_df = pd.read_csv(
    "data/plumbing_styles.csv"
)

treatment_df = pd.read_csv(
    "data/treatment_systems.csv"
)


# ---------------------------------------------------
# MERGE DATASETS
# ---------------------------------------------------

df = greywater_df.merge(
    plumbing_df,
    on=["country", "state"],
    how="left"
)

df = df.merge(
    treatment_df,
    on=["country", "state"],
    how="left"
)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("💧 Greywater Awareness Hub")

st.markdown("""
### Creating awareness about global greywater production, reuse, and treatment systems.

This platform helps users understand:
- how much greywater is produced,
- plumbing infrastructure differences,
- treatment methods,
- and safe reuse opportunities worldwide.
""")


# ---------------------------------------------------
# MODULE CARDS
# ---------------------------------------------------

st.subheader("Explore Modules")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("💧 Greywater Production")

with col2:
    st.info("🔧 Plumbing Styles")

with col3:
    st.info("⚙️ Treatment Systems")

with col4:
    st.info("ℹ️ Information Center")


# ---------------------------------------------------
# COUNTRY SELECTION
# ---------------------------------------------------

st.subheader("Select Country and State")

selected_country = st.selectbox(
    "Choose Country",
    df["country"].unique()
)

filtered_country = df[
    df["country"] == selected_country
]

selected_state = st.selectbox(
    "Choose State/Region",
    filtered_country["state"].unique()
)

selected_row = filtered_country[
    filtered_country["state"] == selected_state
].iloc[0]


# ---------------------------------------------------
# METRICS
# ---------------------------------------------------

st.subheader("Greywater Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Population",
    f"{selected_row['population']:,}"
)

col2.metric(
    "Greywater Tons/Hour",
    f"{selected_row['greywater_tons_per_hour']:,}"
)

col3.metric(
    "Greywater m³/Year",
    f"{selected_row['greywater_m3_year']:,}"
)


# ---------------------------------------------------
# PLUMBING STYLE
# ---------------------------------------------------

st.subheader("Plumbing Infrastructure")

st.success(
    f"Plumbing Style: {selected_row['plumbing_style']}"
)

st.write(
    f"Reuse Support Level: {selected_row['reuse_support']}"
)

st.write(
    f"Infrastructure Description: {selected_row['description']}"
)


# ---------------------------------------------------
# TREATMENT SYSTEMS
# ---------------------------------------------------

st.subheader("Treatment Systems")

st.write(
    f"Treatment Available: {selected_row['treatment_available']}"
)

st.write(
    f"Treatment Methods: {selected_row['treatment_methods']}"
)

st.write(
    f"Reuse Readiness: {selected_row['reuse_readiness']}"
)


# ---------------------------------------------------
# GREYWATER CHART
# ---------------------------------------------------

st.subheader("Greywater Production Comparison")

fig = px.bar(
    df,
    x="country",
    y="greywater_tons_per_hour",
    color="country",
    title="Greywater Tons Per Hour by Country"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------
# INFORMATION CENTER
# ---------------------------------------------------

st.subheader("What is Greywater?")

st.write("""
Greywater is wastewater generated from:
- showers,
- sinks,
- laundry,
- and household cleaning activities.

It does NOT include toilet waste.

Greywater can often be treated and reused for:
- gardening,
- toilet flushing,
- irrigation,
- and cleaning purposes.
""")


# ---------------------------------------------------
# SAFE REUSE GUIDE
# ---------------------------------------------------

st.subheader("Safe Greywater Reuse Options")

st.write("""
Common reuse options include:
- garden irrigation,
- toilet flushing,
- car washing,
- outdoor cleaning,
- landscape watering.

Avoid direct reuse for:
- drinking,
- cooking,
- bathing,
- or food preparation without advanced treatment.
""")


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Greywater Awareness Hub • Sustainability • Water Reuse • Public Awareness"
)
