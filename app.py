
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Hotel & OTA Revenue Intelligence",
    page_icon="🏨",
    layout="wide"
)

# --------------------------------------------------
# COLOUR PALETTE
# --------------------------------------------------
NAVY = "#142D4E"
TEAL = "#16A6A1"
AMBER = "#E9A23B"
RED = "#D95D5D"
SLATE = "#64748B"
PURPLE = "#8B5CF6"
BACKGROUND = "#F1F5F9"

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {BACKGROUND};
    }}

    h1, h2, h3 {{
        color: {NAVY} !important;
    }}

    [data-testid="stMetric"] {{
        background-color: white;
        border: 1px solid #E2E8F0;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(20, 45, 78, 0.06);
    }}

    [data-testid="stMetricLabel"] {{
        color: {SLATE} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {NAVY} !important;
    }}

    div[data-testid="stPlotlyChart"] {{
        background-color: white;
        border-radius: 12px;
        padding: 8px;
        border: 1px solid #E2E8F0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------
DATA_PATH = (
    r"C:\Users\sakshi\Downloads\Hotel_ETA_ Analysis"
    r"\data\raw\hotel_bookings_working.csv"
)


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    # Create arrival date
    data["arrival_date"] = pd.to_datetime(
        data["arrival_date_year"].astype(str)
        + "-"
        + data["arrival_date_month"].astype(str)
        + "-"
        + data["arrival_date_day_of_month"].astype(str),
        format="%Y-%B-%d",
        errors="coerce"
    )

    # Ensure numeric columns are numeric
    for column in [
        "adr",
        "total_nights",
        "estimated_room_revenue",
        "lead_time"
    ]:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column], errors="coerce"
            )

    return data


# --------------------------------------------------
# SHARED CHART STYLING
# --------------------------------------------------

def style_chart(fig):
    """Apply consistent styling and readable legend text."""

    fig.update_layout(
        template="plotly_white",
        font=dict(family="Arial", color=NAVY, size=12),
        title_font=dict(color=NAVY, size=17),
        legend=dict(
            font=dict(color=NAVY, size=12),
            title_font=dict(color=NAVY, size=12),
            bgcolor="rgba(255,255,255,0.95)",
            borderwidth=0
        ),
        margin=dict(l=20, r=20, t=65, b=25),
        paper_bgcolor="white",
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_color=NAVY,
            bordercolor="#CBD5E1"
        )
    )

    fig.update_xaxes(
        title_font=dict(color=NAVY),
        tickfont=dict(color=NAVY),
        gridcolor="#E2E8F0",
        zerolinecolor="#CBD5E1"
    )

    fig.update_yaxes(
        title_font=dict(color=NAVY),
        tickfont=dict(color=NAVY),
        gridcolor="#E2E8F0",
        zerolinecolor="#CBD5E1"
    )

    return fig



# --------------------------------------------------
# LOAD DATA AND HANDLE ERRORS
# --------------------------------------------------
try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "Dataset not found. Please check the DATA_PATH "
        "at the top of app.py."
    )
    st.stop()

except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()


required_columns = [
    "hotel",
    "arrival_date",
    "reservation_status",
    "estimated_room_revenue",
    "total_nights",
    "adr",
    "distribution_channel",
    "lead_time"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The dataset is missing these required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------
st.title("Hotel & OTA Revenue Intelligence")

st.caption(
    "Explore hotel booking patterns, estimated room revenue, "
    "distribution channels, and booking lead times."
)


# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.sidebar.header("Dashboard Filters")

hotel_options = ["All Hotels"] + sorted(
    df["hotel"].dropna().unique().tolist()
)

selected_hotel = st.sidebar.selectbox(
    "Hotel Type",
    hotel_options
)

valid_dates = df["arrival_date"].dropna()

if valid_dates.empty:
    st.error("No valid arrival dates were found in the dataset.")
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

selected_dates = st.sidebar.date_input(
    "Arrival Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = df.copy()

if selected_hotel != "All Hotels":
    filtered_df = filtered_df[
        filtered_df["hotel"] == selected_hotel
    ]

if isinstance(selected_dates, (tuple, list)):
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates

        filtered_df = filtered_df[
            filtered_df["arrival_date"].dt.date.between(
                start_date, end_date
            )
        ]
    elif len(selected_dates) == 1:
        filtered_df = filtered_df[
            filtered_df["arrival_date"].dt.date
            == selected_dates[0]
        ]

if filtered_df.empty:
    st.warning(
        "No bookings match the selected filters. "
        "Please change your filters."
    )
    st.stop()


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------
completed_df = filtered_df[
    filtered_df["reservation_status"] == "Check-Out"
].copy()

estimated_revenue = completed_df[
    "estimated_room_revenue"
].fillna(0).sum()

completed_bookings = len(completed_df)

room_nights = completed_df[
    "total_nights"
].fillna(0).sum()

average_adr = completed_df["adr"].mean()

if pd.isna(average_adr):
    average_adr = 0


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "Estimated Room Revenue",
    f"{estimated_revenue:,.2f}"
)

kpi2.metric(
    "Completed Bookings",
    f"{completed_bookings:,}"
)

kpi3.metric(
    "Room Nights",
    f"{room_nights:,.0f}"
)

kpi4.metric(
    "Average ADR",
    f"{average_adr:,.2f}"
)

st.caption(
    "Revenue is an estimate calculated from the dataset's "
    "estimated_room_revenue field for checked-out bookings. "
    "Currency units depend on the source dataset. "
    "This is not audited accounting revenue or profit."
)

st.divider()


# --------------------------------------------------
# CHART 1: MONTHLY REVENUE TREND
# --------------------------------------------------
st.subheader("Monthly Revenue Trend")

if completed_df.empty:
    st.info("No completed bookings are available for this filter.")
else:
    monthly_revenue = (
        completed_df
        .dropna(subset=["arrival_date"])
        .assign(
            month=lambda x: (
                x["arrival_date"].dt.to_period("M").dt.to_timestamp()
            )
        )
        .groupby(["month", "hotel"], as_index=False)
        ["estimated_room_revenue"]
        .sum()
        .rename(
            columns={
                "estimated_room_revenue": "Estimated Revenue",
                "hotel": "Hotel Type"
            }
        )
    )

    if monthly_revenue.empty:
        st.info("No monthly revenue data is available.")
    else:
        fig_monthly = px.line(
            monthly_revenue,
            x="month",
            y="Estimated Revenue",
            color="Hotel Type",
            markers=True,
            color_discrete_sequence=[NAVY, TEAL],
            labels={
                "month": "Month",
                "Estimated Revenue": "Estimated Room Revenue",
                "Hotel Type": "Hotel Type"
            },
            template="plotly_white"
        )

        fig_monthly.update_layout(
            hovermode="x unified",
            legend_title_text="Hotel Type"
        )

        fig_monthly.update_traces(
            line=dict(width=3),
            marker=dict(size=7),
            hovertemplate=(
                "Month: %{x|%b %Y}<br>"
                "Estimated Revenue: %{y:,.2f}"
                "<extra>%{fullData.name}</extra>"
            )
        )

        fig_monthly = style_chart(fig_monthly)

        # Explicitly enforce visible legend labels
        fig_monthly.update_layout(
            showlegend=True,
            legend=dict(
                font=dict(color=NAVY, size=12),
                title_font=dict(color=NAVY, size=12)
            )
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )


# --------------------------------------------------
# CHART 2: REVENUE BY HOTEL TYPE
# --------------------------------------------------
st.subheader("Revenue by Hotel Type")

if completed_df.empty:
    st.info("No completed bookings are available.")
else:
    hotel_revenue = (
        completed_df
        .groupby("hotel", as_index=False)
        ["estimated_room_revenue"]
        .sum()
        .rename(
            columns={
                "hotel": "Hotel Type",
                "estimated_room_revenue": "Estimated Revenue"
            }
        )
        .sort_values("Estimated Revenue", ascending=False)
    )

    if hotel_revenue.empty:
        st.info("No hotel revenue data is available.")
    else:
        fig_hotel = px.bar(
            hotel_revenue,
            x="Hotel Type",
            y="Estimated Revenue",
            color="Hotel Type",
            color_discrete_sequence=[NAVY, TEAL],
            text_auto=".2s",
            labels={
                "Hotel Type": "Hotel Type",
                "Estimated Revenue": "Estimated Room Revenue"
            },
            template="plotly_white"
        )

        fig_hotel.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "Hotel Type: %{x}<br>"
                "Estimated Revenue: %{y:,.2f}"
                "<extra></extra>"
            )
        )

        fig_hotel = style_chart(fig_hotel)

        fig_hotel.update_layout(
            showlegend=True,
            legend=dict(
                font=dict(color=NAVY, size=12),
                title_font=dict(color=NAVY, size=12)
            )
        )

        st.plotly_chart(
            fig_hotel,
            use_container_width=True
        )


# --------------------------------------------------
# CHART 3: BOOKING STATUS BREAKDOWN
# --------------------------------------------------
st.subheader("Booking Status Breakdown")

status_data = (
    filtered_df["reservation_status"]
    .fillna("Unknown")
    .value_counts()
    .rename_axis("Reservation Status")
    .reset_index(name="Number of Bookings")
)

if status_data.empty:
    st.info("No booking status data is available.")
else:
    status_colors = {
        "Check-Out": TEAL,
        "Canceled": RED,
        "No-Show": AMBER
    }

    fig_status = px.bar(
        status_data,
        x="Reservation Status",
        y="Number of Bookings",
        color="Reservation Status",
        color_discrete_map=status_colors,
        text_auto=True,
        labels={
            "Reservation Status": "Reservation Status",
            "Number of Bookings": "Number of Bookings"
        },
        template="plotly_white"
    )

    fig_status.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "Reservation Status: %{x}<br>"
            "Number of Bookings: %{y:,}"
            "<extra></extra>"
        )
    )

    fig_status = style_chart(fig_status)

    fig_status.update_layout(
        showlegend=True,
        legend=dict(
            font=dict(color=NAVY, size=12),
            title_font=dict(color=NAVY, size=12)
        )
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )


# --------------------------------------------------
# CHART 4: REVENUE BY DISTRIBUTION CHANNEL
# --------------------------------------------------
st.subheader("Revenue by Distribution Channel")

if completed_df.empty:
    st.info("No completed bookings are available.")
else:
    channel_revenue = (
        completed_df
        .groupby("distribution_channel", as_index=False)
        ["estimated_room_revenue"]
        .sum()
        .rename(
            columns={
                "distribution_channel": "Distribution Channel",
                "estimated_room_revenue": "Estimated Revenue"
            }
        )
        .sort_values("Estimated Revenue", ascending=False)
    )

    if channel_revenue.empty:
        st.info("No distribution channel revenue data is available.")
    else:
        fig_channel = px.bar(
            channel_revenue,
            x="Distribution Channel",
            y="Estimated Revenue",
            color="Distribution Channel",
            color_discrete_sequence=[
                NAVY, TEAL, AMBER, PURPLE, SLATE, RED
            ],
            text_auto=".2s",
            labels={
                "Distribution Channel": "Distribution Channel",
                "Estimated Revenue": "Estimated Room Revenue"
            },
            template="plotly_white"
        )

        fig_channel.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "Distribution Channel: %{x}<br>"
                "Estimated Revenue: %{y:,.2f}"
                "<extra></extra>"
            )
        )

        fig_channel = style_chart(fig_channel)

        fig_channel.update_layout(
            showlegend=True,
            legend=dict(
                font=dict(color=NAVY, size=12),
                title_font=dict(color=NAVY, size=12)
            )
        )

        st.plotly_chart(
            fig_channel,
            use_container_width=True
        )


# --------------------------------------------------
# CHART 5: BOOKING LEAD-TIME DISTRIBUTION
# --------------------------------------------------
st.subheader("Booking Lead-Time Distribution")

lead_time_data = filtered_df.dropna(
    subset=["lead_time"]
).copy()

if lead_time_data.empty:
    st.info("No booking lead-time data is available.")
else:
    fig_lead = px.histogram(
        lead_time_data,
        x="lead_time",
        nbins=40,
        color_discrete_sequence=[TEAL],
        labels={
            "lead_time": "Lead Time (Days)",
            "count": "Number of Bookings"
        },
        template="plotly_white"
    )

    fig_lead.update_traces(
        marker_line_color="white",
        marker_line_width=0.5,
        hovertemplate=(
            "Lead Time: %{x} days<br>"
            "Number of Bookings: %{y:,}"
            "<extra></extra>"
        )
    )

    fig_lead = style_chart(fig_lead)

    st.plotly_chart(
        fig_lead,
        use_container_width=True
    )



# --------------------------------------------------
# KEY BUSINESS INSIGHTS
# --------------------------------------------------
st.divider()

st.markdown(
    "<h2 style='color:#142D4E;'>Key Business Insights</h2>",
    unsafe_allow_html=True
)

insight1, insight2 = st.columns(2)

with insight1:
    st.markdown(
        "<h4 style='color:#142D4E;'>Top Revenue Distribution Channel</h4>",
        unsafe_allow_html=True
    )

    if not completed_df.empty:
        top_channel = (
            completed_df
            .groupby("distribution_channel")["estimated_room_revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        if not top_channel.empty:
            st.markdown(
                f"""
                <div style="
                    background-color: white;
                    color: #142D4E;
                    padding: 18px;
                    border-radius: 12px;
                    border: 1px solid #E2E8F0;
                    font-size: 18px;
                    font-weight: 600;
                ">
                    {top_channel.index[0]} — {top_channel.iloc[0]:,.2f}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("No channel revenue data is available.")
    else:
        st.info("No completed bookings are available.")

with insight2:
    st.markdown(
        "<h4 style='color:#142D4E;'>Highest Revenue Hotel Type</h4>",
        unsafe_allow_html=True
    )

    if not completed_df.empty:
        top_hotel = (
            completed_df
            .groupby("hotel")["estimated_room_revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        if not top_hotel.empty:
            st.markdown(
                f"""
                <div style="
                    background-color: white;
                    color: #142D4E;
                    padding: 18px;
                    border-radius: 12px;
                    border: 1px solid #E2E8F0;
                    font-size: 18px;
                    font-weight: 600;
                ">
                    {top_hotel.index[0]} — {top_hotel.iloc[0]:,.2f}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("No hotel revenue data is available.")
    else:
        st.info("No completed bookings are available.")

st.caption(
    "Revenue insights use completed bookings only. "
    "Booking status and lead-time charts include all bookings "
    "matching the selected filters."
)
