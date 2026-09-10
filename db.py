import streamlit as st
import datetime
import pandas as pd
import db

# -----------------------------------------------------------------------------
# App Configuration & Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Privacy-First Health Tracker",
    page_icon="🌿",
    layout="wide"
)

# Initialize Database on app start
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
# Main Dashboard Layout (Two Columns)
# -----------------------------------------------------------------------------
col_form, col_history = st.columns([1, 1.2], gap="large")

# --- COLUMN 1: Daily Logging Form ---
with col_form:
    st.subheader("📝 Log Daily Metrics")
    
    with st.form("health_metric_form", clear_on_submit=False):
        # 1. Date Picker (Defaults to today)
        selected_date = st.date_input(
            "Log Date",
            value=datetime.date.today(),
            max_value=datetime.date.today()
        )
        
        # 2. Sleep Duration (0.0 to 24.0 hours, step 0.5)
        sleep_hours = st.number_input(
            "Sleep Duration (Hours)",
            min_value=0.0,
            max_value=24.0,
            value=7.5,
            step=0.5
        )
        
        # 3. Step Count
        steps = st.number_input(
            "Steps Count",
            min_value=0,
            max_value=100000,
            value=8000,
            step=500
        )
        
        # 4. Mood Rating (1 to 10 visual slider)
        mood = st.slider(
            "Mood Rating (1 = Low, 10 = High)",
            min_value=1,
            max_value=10,
            value=7
        )
        
        # 5. Optional Notes
        notes = st.text_area(
            "Daily Journal / Notes (Optional)",
            placeholder="Felt energetic after morning walk...",
            height=100
        )
        
        # Form Submission Button
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
            else:
                st.error("❌ Failed to save metric. Check application logs.")

# --- COLUMN 2: Historical Logs ---
with col_history:
    st.subheader("📋 Log History")
    
    # Fetch records from SQLite
    df_logs = db.fetch_all_metrics()
    
    if df_logs.empty:
        st.info("No records logged yet. Use the form on the left to add your first entry!")
    else:
        # Display summary statistics
        st.caption(f"Total Logs Recorded: **{len(df_logs)}**")
        
        # Interactive DataFrame Table
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
        
        # Quick Delete Option
        with st.expander("🗑️ Delete an Entry"):
            dates_available = df_logs["log_date"].tolist()
            date_to_delete = st.selectbox("Select Date to Delete", options=dates_available)
            if st.button("Delete Log", type="primary"):
                db.delete_metric_by_date(date_to_delete)
                st.warning(f"Deleted entry for {date_to_delete}.")
                st.rerun()