import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Greywater Awareness Hub",
    page_icon="💧",
    layout="wide"
)


# -----------------------------------
# SAMPLE DATA
# -----------------------------------

sample_data = pd.DataFrame({

    "country": [
        "United States",
        "India",
        "Singapore",
        "Australia"
    ],

    "state": [
        "Ohio",
        "Telangana",
        "Central Region",
        "New South Wales"
    ],

    "population": [
        11700000,
        39000000,
        5900000,
        8400000
    ],

    "greywater_tons_per_hour": [
        250000,
        900000,
        180000,
        220000
    ],

    "plumbing_style": [
        "Centralized Sewer",
        "Mixed Infrastructure",
        "Advanced Dual Plumbing",
        "Centralized Reuse System"
    ],

    "treatment_status": [
        "Moderate",
        "Limited",
        "Advanced",
        "Good"
    ]
})


# -----------------------------------
# TITLE
# -----------------------------------

st.title("💧 Greywater Awareness Hub")

st.markdown("""
### Creating awareness about global greywater production, reuse, and treatment systems.

This platform helps users understand:
- how much greywater is produced,
- plumbing infrastructure differences,
- treatment methods,
- and safe reuse opportunities worldwide.
""")


# -----------------------------------
# DASHBOARD MODULES
# -----------------------------------

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


# -----------------------------------
# COUNTRY AND STATE DROPDOWN
# -----------------------------------

st.subheader("Select Country and State")

selected_country = st.selectbox(
    "Choose Country",
    sample_data["country"].unique()
)

filtered_country = sample_data[
    sample_data["country"] == selected_country
]

selected_state = st.selectbox(
    "Choose State/Region",
    filtered_country["state"].unique()
)

selected_row = filtered_country[
    filtered_country["state"] == selected_state
].iloc[0]


# -----------------------------------
# METRICS
# -----------------------------------

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
    "Treatment Status",
    selected_row["treatment_status"]
)


# -----------------------------------
# PLUMBING STYLE
# -----------------------------------

st.subheader("Plumbing Style")

st.success(
    f"Plumbing Style: {selected_row['plumbing_style']}"
)


# -----------------------------------
# GREYWATER CHART
# -----------------------------------

st.subheader("Greywater Production Comparison")

fig = px.bar(
    sample_data,
    x="country",
    y="greywater_tons_per_hour",
    color="country",
    title="Greywater Tons Per Hour by Country"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------------
# INFORMATION CENTER
# -----------------------------------

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


# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "Greywater Awareness Hub • Sustainability • Water Reuse • Public Awareness"
)
