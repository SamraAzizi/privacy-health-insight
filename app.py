import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import db

# -----------------------------------------------------------------------------
# App Configuration & Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Privacy-First Health Tracker",
    page_icon="🌿",
    layout="wide"
)

db.init_db()

# -----------------------------------------------------------------------------
# Header Section
# -----------------------------------------------------------------------------
st.title("🌿 Privacy-First Health Insight App")
st.markdown(
    """
    Track daily health metrics with zero cloud transmission. 
    All data is stored directly on your local device.
    """
)

st.divider()

# -----------------------------------------------------------------------------
# Sidebar Navigation & Settings
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("Settings & Navigation")
    st.info("🔒 **Data Locality:** Local SQLite Database active.")

# -----------------------------------------------------------------------------
# Main Dashboard Layout (Two Columns for Data Logging & History)
# -----------------------------------------------------------------------------
col_form, col_history = st.columns([1, 1.2], gap="large")

# --- COLUMN 1: Daily Logging Form ---
with col_form:
    st.subheader("📝 Log Daily Metrics")
    
    with st.form("health_metric_form", clear_on_submit=False):
        selected_date = st.date_input(
            "Log Date",
            value=datetime.date.today(),
            max_value=datetime.date.today()
        )
        
        sleep_hours = st.number_input(
            "Sleep Duration (Hours)",
            min_value=0.0,
            max_value=24.0,
            value=7.5,
            step=0.5
        )
        
        steps = st.number_input(
            "Steps Count",
            min_value=0,
            max_value=100000,
            value=8000,
            step=500
        )
        
        mood = st.slider(
            "Mood Rating (1 = Low, 10 = High)",
            min_value=1,
            max_value=10,
            value=7
        )
        
        notes = st.text_area(
            "Daily Journal / Notes (Optional)",
            placeholder="Felt energetic after morning walk...",
            height=100
        )
        
        submitted = st.form_submit_button("Save Entry", use_container_width=True)
        
        if submitted:
            date_str = selected_date.strftime("%Y-%m-%d")
            success = db.save_daily_metric(
                log_date=date_str,
                sleep_hours=sleep_hours,
                steps=steps,
                mood=mood,
                notes=notes
            )
            
            if success:
                st.success(f"✅ Entry saved for {date_str}!")
                st.rerun()
            else:
                st.error("❌ Failed to save metric. Check application logs.")

# --- COLUMN 2: Historical Logs ---
with col_history:
    st.subheader("📋 Log History")
    
    df_logs = db.fetch_all_metrics()
    
    if df_logs.empty:
        st.info("No records logged yet. Use the form on the left to add your first entry!")
    else:
        st.caption(f"Total Logs Recorded: **{len(df_logs)}**")
        
        st.dataframe(
            df_logs,
            column_config={
                "log_date": "Date",
                "sleep_hours": st.column_config.NumberColumn("Sleep (hrs)", format="%.1f"),
                "steps": st.column_config.NumberColumn("Steps", format="%d"),
                "mood": st.column_config.NumberColumn("Mood (1-10)", format="%d"),
                "notes": "Notes"
            },
            hide_index=True,
            use_container_width=True
        )
        
        with st.expander("🗑️ Delete an Entry"):
            dates_available = df_logs["log_date"].tolist()
            date_to_delete = st.selectbox("Select Date to Delete", options=dates_available)
            if st.button("Delete Log", type="primary"):
                db.delete_metric_by_date(date_to_delete)
                st.warning(f"Deleted entry for {date_to_delete}.")
                st.rerun()

st.divider()

# -----------------------------------------------------------------------------
# PHASE 3: Trends & Analytics Section
# -----------------------------------------------------------------------------
st.subheader("📊 Health Trends & Visual Analytics")

if not df_logs.empty:
    # Data Preparation: Ensure correct data types
    df_logs["log_date"] = pd.to_datetime(df_logs["log_date"])
    df_logs = df_logs.sort_values("log_date")

    # Time Range Filter Controls
    col_filter1, col_filter2 = st.columns([1, 3])
    with col_filter1:
        time_filter = st.selectbox(
            "Time Horizon",
            options=["Last 7 Days", "Last 30 Days", "All Time"],
            index=0
        )
    
    # Filter Data based on user selection
    max_date = df_logs["log_date"].max()
    if time_filter == "Last 7 Days":
        min_date = max_date - pd.Timedelta(days=7)
        filtered_df = df_logs[df_logs["log_date"] >= min_date]
    elif time_filter == "Last 30 Days":
        min_date = max_date - pd.Timedelta(days=30)
        filtered_df = df_logs[df_logs["log_date"] >= min_date]
    else:
        filtered_df = df_logs.copy()

    # Display KPI Summary Cards
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        avg_sleep = filtered_df["sleep_hours"].mean()
        st.metric("Avg Sleep", f"{avg_sleep:.1f} hrs")
    with col_kpi2:
        avg_steps = filtered_df["steps"].mean()
        st.metric("Avg Daily Steps", f"{avg_steps:,.0f}")
    with col_kpi3:
        avg_mood = filtered_df["mood"].mean()
        st.metric("Avg Mood Score", f"{avg_mood:.1f} / 10")

    # Multi-Subplot Interactive Chart (Plotly)
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=("Sleep Duration (Hours)", "Daily Step Count", "Mood Score (1-10)")
    )

    # Subplot 1: Sleep
    fig.add_trace(
        go.Scatter(
            x=filtered_df["log_date"],
            y=filtered_df["sleep_hours"],
            mode="lines+markers",
            name="Sleep (hrs)",
            line=dict(color="#4F46E5", width=3),
            marker=dict(size=7)
        ),
        row=1, col=1
    )

    # Subplot 2: Steps
    fig.add_trace(
        go.Bar(
            x=filtered_df["log_date"],
            y=filtered_df["steps"],
            name="Steps",
            marker_color="#10B981"
        ),
        row=2, col=1
    )

    # Subplot 3: Mood
    fig.add_trace(
        go.Scatter(
            x=filtered_df["log_date"],
            y=filtered_df["mood"],
            mode="lines+markers",
            name="Mood",
            line=dict(color="#F59E0B", width=3),
            marker=dict(size=7)
        ),
        row=3, col=1
    )

    # Update Chart Formatting
    fig.update_layout(
        height=650,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified"
    )

    # Y-axis bounds configuration
    fig.update_yaxes(title_text="Hours", row=1, col=1)
    fig.update_yaxes(title_text="Steps", row=2, col=1)
    fig.update_yaxes(title_text="Score", range=[0, 10.5], row=3, col=1)

    # Render Plotly Chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Log at least 2 entries to generate trend charts.")