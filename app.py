import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Personal Trainer Market Explorer", page_icon="💪", layout="wide")

# -------------------------
# 1. DATA – combine fitness, crime & politics
# -------------------------
data = [
    ("Cary","NC",190,630,3.6,122,66,2,3,1.07,12.58,33,62.3,35.8,"Harold Weinbrecht (D)"),
    ("Apex","NC",75,625,8.8,48,26,1,1,0.55,9.00,58,62.3,35.8,"Jacques Gilbert (NP)"),
    ("Huntersville","NC",65,627,10.2,38,26,1,1,1.99,14.24,27,66.7,31.6,"Christy Clark (D)"),
    ("Concord","NC",100,626,5.8,59,39,2,4,1.14,10.00,54,44.5,53.9,"Bill Dusch (NP)"),
    ("Wilmington","NC",80,623,5.1,61,17,2,3,4.87,35.08,5,50.2,48.0,"Bill Saffo (D)"),
    ("Mount Pleasant","SC",56,630,6.4,38,16,2,2,1.46,13.13,57,55.5,42.6,"Will Haynie (R)"),
    ("Charleston","SC",98,632,4.0,57,38,3,3,4.08,20.54,14,55.5,42.6,"William Cogswell (R)"),
    ("Greer","SC",19,624,12.5,9,9,1,1,2.34,18.18,19,39.9,58.1,"Rick Danner (R)"),
    ("Summerville","SC",26,626,11.9,15,10,1,1,4.32,30.86,6,43.8,54.2,"Russ Touchberry (NP)"),
    ("Franklin","TN",100,637,7.0,64,35,1,1,1.49,10.20,60,36.1,62.2,"Ken Moore (R)"),
    ("Collierville","TN",50,624,12.2,30,19,1,1,6.00,13.60,40,64.4,34.0,"Maureen Fraser (R)"),
    ("Hendersonville","TN",60,633,9.8,30,29,1,1,3.10,23.30,30,29.9,68.5,"Jamie Clary (R)"),
    ("Brentwood","TN",50,639,14.2,34,15,1,1,0.70,9.30,80,36.1,62.2,"Rhea Little (R)")
]
cols = ["City","State","Gyms","Trainers","TrainerDensity","BoutiqueGyms","BigBoxGyms","CommunityGyms","RentableVenues","ViolentCrimePer1k","PropertyCrimePer1k","CrimeIndex","BidenPct","TrumpPct","Mayor"]
df = pd.DataFrame(data, columns=cols)
df["TotalCrimePer1k"] = df["ViolentCrimePer1k"] + df["PropertyCrimePer1k"]
df["GymDensity"] = df["Gyms"] / 10  # proxy gyms per 10k residents

# -------------------------
# 2. SIDEBAR – filters & quick stats
# -------------------------
with st.sidebar:
    st.header("🔍 Filter Cities")
    state_choice = st.multiselect("State", options=df["State"].unique(), default=list(df["State"].unique()))
    max_crime = st.slider("Max Total Crime per 1k", 5.0, 40.0, 20.0, 0.5)
    min_income_bias = st.radio("Political Leaning", options=["Any","Democratic-leaning","Republican-leaning"], index=0)
    # derive leaning from vote share
    df["Lean"] = df.apply(lambda r: "Democratic-leaning" if r["BidenPct"] > r["TrumpPct"] else "Republican-leaning", axis=1)
    filtered = df[(df["State"].isin(state_choice)) & (df["TotalCrimePer1k"] <= max_crime)]
    if min_income_bias != "Any":
        filtered = filtered[filtered["Lean"] == min_income_bias]

    st.markdown(f"**{len(filtered)} of {len(df)} cities match** the criteria.")

# -------------------------
# 3. OVERVIEW
# -------------------------
st.title("💪 Personal Trainer Market Explorer – NC · SC · TN (2025)")

st.markdown("""
This dashboard blends **fitness infrastructure**, **crime rates**, and **political context** for 12 high‑income, high‑growth cities in North Carolina, South Carolina, and Tennessee. Use the sidebar filters to narrow the list, then explore interactive charts to identify the **best launch markets** for a premium personal‑training business.
""")

# -------------------------
# 4. METRICS SUMMARY CARDS
# -------------------------
col1,col2,col3 = st.columns(3)
col1.metric("Median Gyms / City", f"{df['Gyms'].median():.0f}")
col2.metric("Median Trainers / City", f"{df['Trainers'].median():.0f}")
col3.metric("Median Crime Index", f"{df['CrimeIndex'].median():.0f} (↑ safer)")

# -------------------------
# 5. TABS FOR INSIGHTS
# -------------------------
fitness_tab, crime_tab, politics_tab, recommend_tab = st.tabs(["🏋️‍♂️ Fitness","🚨 Safety","🗳️ Politics","🎯 Recommendations"])

# --- Fitness Tab ---
with fitness_tab:
    st.subheader("Gyms & Trainers Overview")
    fig1 = px.bar(filtered, x="City", y="Gyms", color="State", title="Gyms per City")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(filtered, x="City", y="TrainerDensity", color="State", title="Trainer Density (per 10k residents)")
    st.plotly_chart(fig2, use_container_width=True)

    # stacked gym type
    fig3 = px.bar(filtered, x="City", y=["BoutiqueGyms","BigBoxGyms","CommunityGyms"], title="Gym Type Breakdown", labels={"value":"Gyms","variable":"Type"})
    st.plotly_chart(fig3, use_container_width=True)

# --- Crime Tab ---
with crime_tab:
    st.subheader("Crime Rate Breakdown – Violent vs Property")
    fig4 = px.bar(filtered, x="City", y=["ViolentCrimePer1k","PropertyCrimePer1k"], title="Crime Rates (per 1k residents)", labels={"value":"Incidents per 1k","variable":"Crime Type"})
    st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.scatter(filtered, x="GymDensity", y="CrimeIndex", size="Trainers", color="State", hover_name="City", title="Safety vs Gym Density")
    st.plotly_chart(fig5, use_container_width=True)

# --- Politics Tab ---
with politics_tab:
    st.subheader("2020 Presidential Vote Share (County Level)")
    fig6 = px.bar(filtered, x="City", y=["BidenPct","TrumpPct"], title="2020 Vote %", labels={"value":"% Vote","variable":"Candidate"})
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("Cities shaded **blue** lean Democratic; **red** lean Republican. Local leadership (mayor) party is annotated in the table below.")
    st.dataframe(filtered[["City","Mayor","BidenPct","TrumpPct","Lean"]].set_index("City"))

# --- Recommendation Tab ---
with recommend_tab:
    st.subheader("✨ Target Market Recommendations")

    # simple heuristic: low crime, high income vibe (use CrimeIndex > 50 and TrainerDensity between 5–10)
    ideal = df[(df["CrimeIndex"] > 50) & (df["TrainerDensity"] >= 5) & (df["TrainerDensity"] <= 10)]
    st.markdown("**Top Picks for Launching a Premium Personal‑Training Studio in 2025:**")
    st.write("Based on low crime, solid gym ecosystem, and manageable trainer competition:")
    for _, row in ideal.iterrows():
        st.markdown(f"- **{row['City']}, {row['State']}** – CrimeIndex {row['CrimeIndex']}, TrainerDensity {row['TrainerDensity']:.1f}, {row['Gyms']} gyms, {row['Trainers']} trainers")

    if ideal.empty:
        st.info("No cities match all ideal criteria. Try relaxing filters or adjust the heuristic.")

# -------------------------
# 6. RAW DATA EXPANDER
# -------------------------
with st.expander("📊 Full Data Table"):
    st.dataframe(df.set_index("City"))

st.caption("Data compiled from Census ACS 2023 estimates, FBI UCR 2023, NeighborhoodScout, local government statistics, and premium‑fitness directory listings (June 2025 update).")
st.markdown("Created by [FuentesTech](https://fuentes.tech) – Data Science & Analytics for Fitness Industry Insights")
