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
# SIDEBAR NAVIGATION
# ---------------------------------------------------

st.sidebar.title("💧 Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Greywater Production",
        "Plumbing Styles",
        "Treatment Systems",
        "Information Center"
    ]
)


# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

if page == "Home":

    st.title("💧 Greywater Awareness Hub")

    st.markdown("""
    ### Creating awareness about global greywater production, reuse, and treatment systems.

    This platform helps users understand:
    - greywater production,
    - plumbing infrastructure,
    - treatment systems,
    - reuse opportunities,
    - and sustainability awareness worldwide.
    """)

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

    st.subheader("Global Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Countries/States",
        len(df)
    )

    col2.metric(
        "Total Greywater Tons/Hour",
        f"{df['greywater_tons_per_hour'].sum():,.0f}"
    )

    col3.metric(
        "Total Population",
        f"{df['population'].sum():,}"
    )

    fig = px.bar(
        df,
        x="country",
        y="greywater_tons_per_hour",
        color="country",
        title="Global Greywater Production"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------
# GREYWATER PAGE
# ---------------------------------------------------

elif page == "Greywater Production":

    st.title("💧 Greywater Production")

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

    st.subheader("Country Comparison")

    fig = px.bar(
        df,
        x="country",
        y="greywater_tons_per_hour",
        color="country",
        title="Greywater Production Comparison"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------
# PLUMBING PAGE
# ---------------------------------------------------

elif page == "Plumbing Styles":

    st.title("🔧 Plumbing Styles")

    selected_country = st.selectbox(
        "Choose Country",
        df["country"].unique(),
        key="plumbing_country"
    )

    filtered_country = df[
        df["country"] == selected_country
    ]

    selected_state = st.selectbox(
        "Choose State/Region",
        filtered_country["state"].unique(),
        key="plumbing_state"
    )

    selected_row = filtered_country[
        filtered_country["state"] == selected_state
    ].iloc[0]

    st.subheader("Infrastructure Information")

    st.success(
        f"Plumbing Style: {selected_row['plumbing_style']}"
    )

    st.write(
        f"Reuse Support Level: {selected_row['reuse_support']}"
    )

    st.write(
        f"Description: {selected_row['description']}"
    )


# ---------------------------------------------------
# TREATMENT PAGE
# ---------------------------------------------------

elif page == "Treatment Systems":

    st.title("⚙️ Treatment Systems")

    selected_country = st.selectbox(
        "Choose Country",
        df["country"].unique(),
        key="treatment_country"
    )

    filtered_country = df[
        df["country"] == selected_country
    ]

    selected_state = st.selectbox(
        "Choose State/Region",
        filtered_country["state"].unique(),
        key="treatment_state"
    )

    selected_row = filtered_country[
        filtered_country["state"] == selected_state
    ].iloc[0]

    st.subheader("Treatment Information")

    st.write(
        f"Treatment Available: {selected_row['treatment_available']}"
    )

    st.write(
        f"Treatment Methods: {selected_row['treatment_methods']}"
    )

    st.write(
        f"Reuse Readiness: {selected_row['reuse_readiness']}"
    )

    st.subheader("Recommended Reuse Options")

    st.info("""
    Recommended reuse options:
    - irrigation,
    - toilet flushing,
    - landscape watering,
    - cleaning purposes.
    """)


# ---------------------------------------------------
# INFORMATION PAGE
# ---------------------------------------------------

elif page == "Information Center":

    st.title("ℹ️ Information Center")

    with st.expander("What is Greywater?"):

        st.write("""
        Greywater is wastewater generated from:
        - showers,
        - sinks,
        - laundry,
        - and cleaning activities.
        """)

    with st.expander("Greywater vs Blackwater"):

        st.write("""
        Greywater does not include toilet waste.
        Blackwater contains sewage and requires advanced treatment.
        """)

    with st.expander("Treatment Methods"):

        st.write("""
        Common treatment methods:
        - filtration,
        - chlorination,
        - UV treatment,
        - SBR,
        - MBR,
        - wetlands systems.
        """)

    with st.expander("Safe Reuse"):

        st.write("""
        Safe reuse includes:
        - gardening,
        - flushing,
        - irrigation,
        - outdoor cleaning.
        """)


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Greywater Awareness Hub • Sustainability • Water Reuse • Public Awareness"
)
