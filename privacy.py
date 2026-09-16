import streamlit as st
import pandas as pd
import json
import db

def render_privacy_policy():
    """Renders the in-app privacy note explaining data locality guarantees."""
    st.markdown("## 🛡️ Privacy Policy & Data Sovereignty Note")
    
    st.info(
        """
        **Zero-Cloud Commitment:** This application operates on a **Local-First** model. 
        Your health metrics, mood logs, and personal notes are saved exclusively to a local database on your device.
        """
    )
    
    st.markdown(
        """
        ### How Your Data Is Handled:
        1. **Local Database:** All daily logs are stored inside a local SQLite file (`health_data.db`) located in your project directory. No central server or third-party cloud database receives this data.
        2. **Analytics & Charts:** All trends, summary metrics, and visualizations (Plotly) are rendered locally inside your web browser engine.
        3. **Local AI Summaries:** When enabled, metrics are formatted and processed locally using **Ollama** (`http://localhost:11434`). Text context remains entirely on your machine.
        4. **Data Ownership:** You can export or erase your dataset at any time using the tools on this page.
        """
    )

def render_data_management():
    """Renders options for exporting, importing, and deleting local data."""
    st.markdown("## 💾 Data Portability & Backup Tools")
    
    df_logs = db.fetch_all_metrics()
    
    col_export, col_import = st.columns(2, gap="large")
    
    # --- EXPORT DATA ---
    with col_export:
        st.subheader("📤 Export Local Data")
        st.caption("Download your health metrics as a local backup file.")
        
        if not df_logs.empty:
            # CSV Download Button
            csv_data = df_logs.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv_data,
                file_name="health_data_backup.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # JSON Download Button
            json_data = df_logs.to_json(orient="records", indent=2)
            st.download_button(
                label="Download as JSON",
                data=json_data,
                file_name="health_data_backup.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.warning("No data available to export yet.")

    # --- IMPORT DATA ---
    with col_import:
        st.subheader("📥 Import Data Backup")
        st.caption("Restore records from a previously exported CSV file.")
        
        uploaded_file = st.file_uploader("Upload CSV Backup", type=["csv"])
        
        if uploaded_file is not None:
            try:
                imported_df = pd.read_csv(uploaded_file)
                
                # Basic Schema Validation
                required_cols = {"log_date", "sleep_hours", "steps", "mood"}
                if required_cols.issubset(set(imported_df.columns)):
                    if st.button("Confirm & Merge Import", type="primary", use_container_width=True):
                        success_count = 0
                        for _, row in imported_df.iterrows():
                            notes_val = str(row["notes"]) if "notes" in row and pd.notna(row["notes"]) else ""
                            saved = db.save_daily_metric(
                                log_date=str(row["log_date"]),
                                sleep_hours=float(row["sleep_hours"]),
                                steps=int(row["steps"]),
                                mood=int(row["mood"]),
                                notes=notes_val
                            )
                            if saved:
                                success_count += 1
                                
                        st.success(f"Successfully processed and merged {success_count} records!")
                        st.rerun()
                else:
                    st.error(f"Invalid file format. Missing required columns: {required_cols - set(imported_df.columns)}")
            except Exception as e:
                st.error(f"Failed to parse import file: {e}")