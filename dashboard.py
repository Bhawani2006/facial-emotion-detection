"""
Streamlit Dashboard for Emotion Detection System
Provides real-time visualization and analytics.
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Emotion Detection Dashboard",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection
@st.cache_resource
def get_db_connection():
    """Get database connection with caching."""
    return sqlite3.connect('emotion_detection.db', check_same_thread=False)

# Initialize session state
if 'current_session' not in st.session_state:
    st.session_state.current_session = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# ── Helper Functions ──────────────────────────────────────────────────────
def get_user_stats(user_id=None):
    """Get statistics for user(s)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if user_id:
        cursor.execute('''
            SELECT emotion, SUM(total_frames) as total_frames, 
                   AVG(avg_confidence) as avg_confidence,
                   MAX(peak_confidence) as peak_confidence
            FROM emotion_stats 
            WHERE user_id = ?
            GROUP BY emotion
            ORDER BY total_frames DESC
        ''', (user_id,))
    else:
        cursor.execute('''
            SELECT emotion, SUM(total_frames) as total_frames, 
                   AVG(avg_confidence) as avg_confidence,
                   MAX(peak_confidence) as peak_confidence
            FROM emotion_stats 
            GROUP BY emotion
            ORDER BY total_frames DESC
        ''')
    
    rows = cursor.fetchall()
    return rows

def get_recent_sessions(limit=10):
    """Get recent sessions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.start_time, s.end_time, u.username, u.age, u.gender,
               COUNT(el.id) as detection_count,
               GROUP_CONCAT(DISTINCT el.emotion) as emotions_detected
        FROM sessions s
        LEFT JOIN users u ON s.user_id = u.id
        LEFT JOIN emotion_logs el ON s.id = el.session_id
        GROUP BY s.id
        ORDER BY s.start_time DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    return rows

def get_session_emotion_timeline(session_id):
    """Get emotion timeline for a session."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, emotion, confidence, face_id
        FROM emotion_logs 
        WHERE session_id = ?
        ORDER BY timestamp
    ''', (session_id,))
    rows = cursor.fetchall()
    return rows

def get_live_stats():
    """Get live statistics for the last hour."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Last hour's activity
    cursor.execute('''
        SELECT 
            COUNT(DISTINCT s.id) as active_sessions,
            COUNT(DISTINCT u.id) as active_users,
            COUNT(el.id) as detections,
            AVG(el.confidence) as avg_confidence
        FROM emotion_logs el
        JOIN sessions s ON el.session_id = s.id
        JOIN users u ON s.user_id = u.id
        WHERE el.timestamp > datetime('now', '-1 hour')
    ''')
    
    row = cursor.fetchone()
    return row

# ── Dashboard Layout ──────────────────────────────────────────────────────
st.sidebar.title("🎭 Emotion Detection Dashboard")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["📊 Overview", "👤 User Analytics", "📈 Session Details", "⚙️ System Settings", "🎥 Live Detection"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")

# Show quick stats in sidebar
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
total_users = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM sessions")
total_sessions = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM emotion_logs")
total_detections = cursor.fetchone()[0]


st.sidebar.metric("👥 Users", total_users)
st.sidebar.metric("📂 Sessions", total_sessions)
st.sidebar.metric("🎭 Detections", f"{total_detections:,}")

# Main content area
if page == "📊 Overview":
    st.title("📊 System Overview")
    
    # Overall statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", total_users)
    with col2:
        st.metric("Total Sessions", total_sessions)
    with col3:
        st.metric("Total Detections", f"{total_detections:,}")
    with col4:
        live_stats = get_live_stats()
        if live_stats and live_stats[0]:
            st.metric("Active Sessions", live_stats[0])
        else:
            st.metric("Active Sessions", 0)
    
    st.markdown("---")
    
    # Recent sessions table
    st.subheader("📋 Recent Sessions")
    recent_sessions = get_recent_sessions(5)
    
    if recent_sessions:
        session_df = pd.DataFrame(recent_sessions, 
                                 columns=['ID', 'Start Time', 'End Time', 'Username', 
                                         'Age', 'Gender', 'Detections', 'Emotions'])
        st.dataframe(session_df, use_container_width=True)
    else:
        st.info("No sessions recorded yet.")
    
    # Emotion distribution chart
    st.subheader("📈 Overall Emotion Distribution")
    stats = get_user_stats()
    
    if stats:
        df_stats = pd.DataFrame(stats, columns=['Emotion', 'Frames', 'Avg Confidence', 'Peak Confidence'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.pie(df_stats, values='Frames', names='Emotion',
                         title="Distribution by Frame Count",
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(df_stats, x='Emotion', y='Avg Confidence',
                         title="Average Confidence per Emotion",
                         color='Emotion',
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig2, use_container_width=True)
    
    # Activity timeline
    st.subheader("📅 Recent Activity")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date(el.timestamp) as date, 
               COUNT(*) as detections,
               COUNT(DISTINCT el.session_id) as sessions
        FROM emotion_logs el
        WHERE el.timestamp > datetime('now', '-7 days')
        GROUP BY date(el.timestamp)
        ORDER BY date
    ''')
    
    timeline_data = cursor.fetchall()
    
    if timeline_data:
        df_timeline = pd.DataFrame(timeline_data, columns=['Date', 'Detections', 'Sessions'])
        fig3 = go.Figure()
        
        fig3.add_trace(go.Scatter(
            x=df_timeline['Date'], y=df_timeline['Detections'],
            mode='lines+markers', name='Detections',
            line=dict(color='#636EFA', width=3)
        ))
        
        fig3.add_trace(go.Scatter(
            x=df_timeline['Date'], y=df_timeline['Sessions'],
            mode='lines+markers', name='Sessions',
            line=dict(color='#EF553B', width=3)
        ))
        
        fig3.update_layout(
            title="Activity Timeline (Last 7 Days)",
            xaxis_title="Date",
            yaxis_title="Count",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig3, use_container_width=True)

elif page == "👤 User Analytics":
    st.title("👤 User Analytics")
    
    # User selector
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users ORDER BY username")
    users = cursor.fetchall()
    
    if users:
        user_options = [f"{row[1]} (ID: {row[0]})" for row in users]
        user_options.insert(0, "All Users")
        
        selected_user = st.selectbox("Select User", user_options)
        
        if selected_user == "All Users":
            user_id = None
            username = "All Users"
        else:
            user_id = int(selected_user.split("ID: ")[1].rstrip(")"))
            username = selected_user.split(" (ID")[0]
        
        # User statistics
        st.subheader(f"📊 Statistics for {username}")
        
        stats = get_user_stats(user_id)
        
        if stats:
            df_stats = pd.DataFrame(stats, 
                                   columns=['Emotion', 'Frames', 'Avg Confidence', 'Peak Confidence'])
            
            # KPI metrics
            total_frames = df_stats['Frames'].sum()
            avg_confidence = df_stats['Avg Confidence'].mean()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Frames", f"{total_frames:,}")
            with col2:
                st.metric("Average Confidence", f"{avg_confidence:.1f}%")
            with col3:
                dominant_emotion = df_stats.loc[df_stats['Frames'].idxmax(), 'Emotion']
                st.metric("Dominant Emotion", dominant_emotion)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.pie(df_stats, values='Frames', names='Emotion',
                             title=f"Emotion Distribution - {username}",
                             color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.bar(df_stats, x='Emotion', y=['Avg Confidence', 'Peak Confidence'],
                             title=f"Confidence Analysis - {username}",
                             barmode='group',
                             color_discrete_sequence=['#636EFA', '#EF553B'])
                fig2.update_layout(yaxis_title="Confidence (%)")
                st.plotly_chart(fig2, use_container_width=True)
            
            # Session history for selected user
            if user_id:
                st.subheader("📋 Session History")
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT s.id, s.start_time, s.end_time,
                           COUNT(el.id) as detections,
                           GROUP_CONCAT(DISTINCT el.emotion) as emotions
                    FROM sessions s
                    LEFT JOIN emotion_logs el ON s.id = el.session_id
                    WHERE s.user_id = ?
                    GROUP BY s.id
                    ORDER BY s.start_time DESC
                    LIMIT 10
                ''', (user_id,))
                
                user_sessions = cursor.fetchall()
                
                if user_sessions:
                    session_df = pd.DataFrame(user_sessions,
                                            columns=['ID', 'Start Time', 'End Time', 
                                                    'Detections', 'Emotions'])
                    st.dataframe(session_df, use_container_width=True)
    else:
        st.info("No users found in the database.")

elif page == "📈 Session Details":
    st.title("📈 Session Details")
    
    # Session selector
    recent_sessions = get_recent_sessions(20)
    
    if recent_sessions:
        session_options = []
        for session in recent_sessions:
            session_id = session[0]
            start_time = session[1]
            username = session[3] or "Anonymous"
            session_options.append(f"Session {session_id} - {start_time} ({username})")
        
        selected_session = st.selectbox("Select Session", session_options)
        session_id = int(selected_session.split(" ")[1].split(" -")[0])
        
        # Session overview
        st.subheader("Session Overview")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.start_time, s.end_time, u.username, u.age, u.gender,
                   COUNT(el.id) as total_detections,
                   COUNT(DISTINCT el.face_id) as unique_faces,
                   MIN(el.timestamp) as first_detection,
                   MAX(el.timestamp) as last_detection
            FROM sessions s
            LEFT JOIN users u ON s.user_id = u.id
            LEFT JOIN emotion_logs el ON s.id = el.session_id
            WHERE s.id = ?
        ''', (session_id,))
        
        session_info = cursor.fetchone()
        
        if session_info:
            # Session metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Start Time", session_info[0][:19])
            with col2:
                if session_info[1]:
                    st.metric("End Time", session_info[1][:19])
                else:
                    st.metric("End Time", "Active")
            with col3:
                st.metric("Detections", session_info[5])
            with col4:
                st.metric("Unique Faces", session_info[6])
            
            # User info
            if session_info[2]:
                st.markdown("**👤 User Information**")
                user_col1, user_col2, user_col3 = st.columns(3)
                with user_col1:
                    st.text_input("Username", session_info[2], disabled=True)
                with user_col2:
                    st.text_input("Age", session_info[3] or "N/A", disabled=True)
                with user_col3:
                    st.text_input("Gender", session_info[4] or "N/A", disabled=True)
            
            # Emotion timeline
            st.subheader("📊 Emotion Timeline")
            timeline_data = get_session_emotion_timeline(session_id)
            
            if timeline_data:
                df_timeline = pd.DataFrame(timeline_data,
                                          columns=['Timestamp', 'Emotion', 'Confidence', 'Face ID'])
                
                # Convert timestamp to datetime
                df_timeline['Timestamp'] = pd.to_datetime(df_timeline['Timestamp'])
                
                # Plot
                fig = px.line(df_timeline, x='Timestamp', y='Confidence',
                            color='Emotion', title="Emotion Confidence Over Time",
                            markers=True, line_shape='spline')
                
                fig.update_layout(
                    xaxis_title="Time",
                    yaxis_title="Confidence (%)",
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Raw data view
                with st.expander("📋 View Raw Session Data"):
                    st.dataframe(df_timeline, use_container_width=True)
            
    else:
        st.info("No sessions found in the database.")

elif page == "⚙️ System Settings":
    st.title("⚙️ System Settings")
    
    tab1, tab2, tab3 = st.tabs(["Database", "User Management", "Export Data"])
    
    with tab1:
        st.subheader("Database Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Database Information**")
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get table sizes
            tables = ['users', 'sessions', 'emotion_logs', 'emotion_stats']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                st.metric(f"📊 {table.title()}", f"{count:,}")
            
            # Get database size
            import os
            db_size = os.path.getsize('emotion_detection.db') / (1024 * 1024)  # MB
            st.metric("💾 Database Size", f"{db_size:.2f} MB")
            
        
        with col2:
            st.markdown("**Maintenance Actions**")
            
            if st.button("🔄 Refresh Database", type="secondary"):
                st.cache_resource.clear()
                st.success("Database cache cleared!")
                st.rerun()
            
            if st.button("📋 Export Schema", type="secondary"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                schema_text = "```sql\n"
                for table in tables:
                    schema_text += table[0] + ";\n\n"
                schema_text += "```"
                
                st.code(schema_text, language='sql')
    
    with tab2:
        st.subheader("User Management")
        
        # Create new user
        with st.form("create_user_form"):
            st.markdown("### Create New User")
            
            new_username = st.text_input("Username*", 
                                        help="Required field")
            new_age = st.number_input("Age", min_value=0, max_value=120, value=0)
            new_gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
            
            if st.form_submit_button("Create User"):
                if new_username:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            'INSERT INTO users (username, age, gender) VALUES (?, ?, ?)',
                            (new_username, new_age if new_age > 0 else None,
                             new_gender if new_gender else None)
                        )
                        conn.commit()
                        st.success(f"✅ User '{new_username}' created successfully!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("❌ Username already exists.")
                    finally:
                        pass
                else:
                    st.error("❌ Please enter a username.")
        
        # User list
        st.markdown("### Existing Users")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, age, gender, created_at
            FROM users
            ORDER BY created_at DESC
        ''')
        
        users = cursor.fetchall()
        
        if users:
            user_df = pd.DataFrame(users, 
                                 columns=['ID', 'Username', 'Age', 'Gender', 'Created At'])
            st.dataframe(user_df, use_container_width=True)
        else:
            st.info("No users found.")
    
    with tab3:
        st.subheader("Data Export")
        
        st.markdown("""
        Export your emotion detection data for analysis in other tools.
        """)
        
        export_format = st.selectbox("Export Format", ["CSV", "JSON", "Excel"])
        
        if st.button("📥 Export All Data", type="primary"):
            conn = get_db_connection()
            
            # Export emotion logs
            df_logs = pd.read_sql_query("SELECT * FROM emotion_logs", conn)
            df_sessions = pd.read_sql_query("SELECT * FROM sessions", conn)
            df_users = pd.read_sql_query("SELECT * FROM users", conn)
            df_stats = pd.read_sql_query("SELECT * FROM emotion_stats", conn)
            
            
            if export_format == "CSV":
                csv = df_logs.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="emotion_logs.csv",
                    mime="text/csv"
                )
            elif export_format == "JSON":
                json_data = df_logs.to_json(orient='records')
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name="emotion_logs.json",
                    mime="application/json"
                )
            elif export_format == "Excel":
                # Create Excel writer
                import io
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_logs.to_excel(writer, sheet_name='Emotion Logs', index=False)
                    df_sessions.to_excel(writer, sheet_name='Sessions', index=False)
                    df_users.to_excel(writer, sheet_name='Users', index=False)
                    df_stats.to_excel(writer, sheet_name='Statistics', index=False)
                
                st.download_button(
                    label="Download Excel",
                    data=buffer.getvalue(),
                    file_name="emotion_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

elif page == "🎥 Live Detection":
    st.title("🎥 Live Detection Interface")
    
    st.markdown("""
    This interface provides real-time emotion detection from webcam.
    Requires the main detection script to be running.
    """)
    
    # Session controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Session Control")
        
        username = st.text_input("Username (optional)", 
                                placeholder="Enter name for personalized stats")
        age = st.number_input("Age (optional)", min_value=0, max_value=120, value=0)
        gender = st.selectbox("Gender (optional)", ["", "Male", "Female", "Other"])
        
        if st.button("▶️ Start Detection Session", type="primary", use_container_width=True):
            # This would start the actual detection
            st.session_state.detection_active = True
            
            # Show instructions
            st.success("""
            ### Session Started!
            
            To start live detection:
            
            1. Open a new terminal
            2. Run: `python enhanced_emotion_detector.py --mode detect --username "YourName"`
            3. Press 'q' in the camera window to stop
            """)
    
    with col2:
        st.subheader("Live Preview")
        
        # Placeholder for live feed
        live_container = st.empty()
        
        # Simulate live data
        if st.session_state.get('detection_active', False):
            import random
            
            # Mock live metrics
            col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
            with col_metrics1:
                st.metric("Current Emotion", random.choice(['😊 Happy', '😨 Fear', '😢 Sad']), 
                         f"{random.randint(65, 92)}%")
            with col_metrics2:
                st.metric("Faces Detected", random.randint(1, 5))
            with col_metrics3:
                st.metric("FPS", random.randint(25, 30))
            
            # Mock live visualization
            st.markdown("**Live Emotion Distribution**")
            mock_data = {
                'Emotion': ['Sad', 'Happy', 'Fear'],
                'Count': [random.randint(1, 10) for _ in range(5)]
            }
            mock_df = pd.DataFrame(mock_data)
            
            fig = px.bar(mock_df, x='Emotion', y='Count', 
                        title="Current Frame Analysis",
                        color='Emotion',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
    
    # Instructions panel
    with st.expander("📋 Setup Instructions"):
        st.markdown("""
        ### How to Set Up Live Detection
        
        1. **Install Required Packages:**
        ```bash
        pip install mediapipe opencv-python tensorflow streamlit
        ```
        
        2. **Initialize Database:**
        ```bash
        python enhanced_emotion_detector.py --mode test
        ```
        
        3. **Start Live Detection:**
        ```bash
        python enhanced_emotion_detector.py --mode detect --username "YourName"
        ```
        
        4. **View Dashboard:**
        ```bash
        streamlit run dashboard.py
        ```
        
        ### Keyboard Controls (Detection Window)
        - **Q**: Quit detection
        - **Space**: Pause/Resume
        - **S**: Take screenshot
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Emotion Detection System Dashboard • Built with Streamlit & MediaPipe</p>
    <p>Database: SQLite • Face Detection: MediaPipe BlazeFace • Emotion Model: Custom CNN</p>
</div>
""", unsafe_allow_html=True)

if __name__ == '__main__':
    # This would typically be run with: streamlit run dashboard.py
    pass
