import streamlit as st
import requests
import json
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Audio Transcript & Sentiment Analysis",
    page_icon="🎤",
    layout="wide"
)

# Title
st.title("🎤 Audio Transcript & Sentiment Analysis")
st.markdown("Upload an audio file to get transcription and sentiment analysis")

# API endpoint configuration
API_URL = st.sidebar.text_input(
    "API URL",
    value="http://localhost:8000",
    help="Enter the FastAPI backend URL"
)

# File uploader
uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=['mp3', 'wav', 'm4a', 'ogg', 'flac', 'webm', 'mp4'],
    help="Supported formats: MP3, WAV, M4A, OGG, FLAC, WEBM, MP4"
)

if uploaded_file is not None:
    # Display file info
    st.info(f"📁 File: {uploaded_file.name} | Size: {uploaded_file.size / 1024:.2f} KB")
    
    # Process button
    if st.button("🚀 Process Audio", type="primary"):
        with st.spinner("Processing audio file... This may take a moment."):
            try:
                # Prepare file for upload
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                
                # Send request to FastAPI backend
                response = requests.post(
                    f"{API_URL}/process-audio",
                    files=files,
                    timeout=300  # 5 minutes timeout for long audio files
                )
                
                # Check response
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    st.success("✅ Processing completed!")
                    
                    # Create columns for better layout
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📝 Transcript")
                        st.text_area(
                            "Transcription",
                            value=result.get("transcript", ""),
                            height=200,
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        st.subheader("💭 Sentiment Analysis")
                        
                        sentiment = result.get("sentiment", "")
                        confidence = result.get("confidence", 0.0)
                        
                        # Display sentiment with color
                        if sentiment == "Positive":
                            st.success(f"**Sentiment:** {sentiment}")
                        elif sentiment == "Negative":
                            st.error(f"**Sentiment:** {sentiment}")
                        elif sentiment == "Neutral":
                            st.info(f"**Sentiment:** {sentiment}")
                        else:
                            st.write(f"**Sentiment:** {sentiment}")
                        
                        # Display confidence with progress bar
                        st.write(f"**Confidence:** {confidence:.2%}")
                        st.progress(confidence)
                    
                    # Check for errors
                    if "error" in result:
                        error_type = result.get("error", "")
                        if error_type == "transcription_error":
                            st.warning("⚠️ Transcription failed. Please check your audio file.")
                        elif error_type == "sentiment_error":
                            st.warning("⚠️ Sentiment analysis failed. Transcript was generated successfully.")
                    
                    # Show raw JSON (collapsible)
                    with st.expander("📋 View Raw Response"):
                        st.json(result)
                        
                else:
                    st.error(f"❌ Error: {response.status_code}")
                    st.text(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the API. Make sure the FastAPI server is running.")
                st.info("Start the server with: `uvicorn app.main:app --reload`")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The audio file might be too long.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                print(f"tk -- Streamlit error: {str(e)}")

# Sidebar information
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Instructions")
st.sidebar.markdown("""
1. Make sure the FastAPI backend is running
2. Upload an audio file
3. Click "Process Audio"
4. View the transcript and sentiment analysis
""")

st.sidebar.markdown("### 🔧 API Status")
if st.sidebar.button("Check API Health"):
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✅ API is running")
        else:
            st.sidebar.error("❌ API returned an error")
    except:
        st.sidebar.error("❌ Cannot reach API")

