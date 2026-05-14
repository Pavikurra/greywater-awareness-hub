import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from src.auth import auth


st.set_page_config(
    page_title="Greywater Awareness Hub",
    page_icon="💧",
    layout="wide"
)


def login_page():

    st.title("💧 Greywater Awareness Hub")

    st.write(
        "Login or sign up to explore greywater production, "
        "plumbing styles, treatment systems, and safe reuse awareness."
    )

    choice = st.radio(
        "Choose option",
        ["Login", "Sign Up"]
    )

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if choice == "Sign Up":

        name = st.text_input("Full Name")

        if st.button("Create Account"):

            try:

                user = auth.create_user_with_email_and_password(
                    email,
                    password
                )

                st.session_state["logged_in"] = True

                st.session_state["user_email"] = email

                st.session_state["user_name"] = name

                st.success(
                    "Account created successfully!"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    "Account already exists or password must be at least 6 characters."
                )

    else:

        if st.button("Login"):

            try:

                user = auth.sign_in_with_email_and_password(
                    email,
                    password
                )

                st.session_state["logged_in"] = True

                st.session_state["user_email"] = email

                st.success(
                    "Login successful!"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    "No account found with this email or incorrect password."
                )


def main_app():

    greywater_df = pd.read_csv(
        "data/countries_greywater.csv"
    )

    plumbing_df = pd.read_csv(
        "data/plumbing_styles.csv"
    )

    treatment_df = pd.read_csv(
        "data/treatment_systems.csv"
    )

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

    st.sidebar.title("💧 Navigation")

    st.sidebar.write(
        f"Logged in as: {st.session_state.get('user_email', '')}"
    )

    if st.sidebar.button("Logout"):

        st.session_state["logged_in"] = False

        st.session_state["user_email"] = ""

        st.rerun()

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

    if page == "Home":

        st.title("💧 Greywater Awareness Hub")

        st.markdown("""
        ### Creating awareness about global greywater production,
        reuse, and treatment systems.

        This platform helps users understand:
        - greywater production
        - plumbing infrastructure
        - treatment systems
        - reuse opportunities
        - sustainability awareness worldwide
        """)

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

        st.success(
            f"Plumbing Style: {selected_row['plumbing_style']}"
        )

        st.write(
            f"Reuse Support Level: {selected_row['reuse_support']}"
        )

        st.write(
            f"Description: {selected_row['description']}"
        )

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

        st.write(
            f"Treatment Available: {selected_row['treatment_available']}"
        )

        st.write(
            f"Treatment Methods: {selected_row['treatment_methods']}"
        )

        st.write(
            f"Reuse Readiness: {selected_row['reuse_readiness']}"
        )

        st.info("""
        Recommended reuse options:
        - irrigation
        - toilet flushing
        - landscape watering
        - outdoor cleaning
        """)

    elif page == "Information Center":

        st.title("ℹ️ Information Center")

        with st.expander("What is Greywater?"):

            st.write("""
            Greywater is wastewater generated from showers,
            sinks, laundry, and household cleaning activities.
            """)

        with st.expander("Greywater vs Blackwater"):

            st.write("""
            Greywater does not include toilet waste.
            Blackwater contains sewage and requires advanced treatment.
            """)

        with st.expander("Treatment Methods"):

            st.write("""
            Common treatment methods include filtration,
            chlorination, UV treatment, SBR, MBR,
            and wetlands systems.
            """)

        with st.expander("Safe Reuse"):

            st.write("""
            Safe reuse includes gardening,
            flushing, irrigation,
            and outdoor cleaning.
            """)

    st.markdown("---")

    st.caption(
        "Greywater Awareness Hub • Sustainability • Water Reuse • Public Awareness"
    )


if "logged_in" not in st.session_state:

    st.session_state["logged_in"] = False


if st.session_state["logged_in"]:

    main_app()

else:

    login_page()
