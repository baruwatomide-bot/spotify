import pandas as pd
import streamlit as st
import os
from typing import List, Optional, Union

# Define column mapping for normalization
CHANGE_COLS = {
    "master_metadata_track_name": "trackName",
    "master_metadata_album_artist_name": "artistName",
    "ts": "endTime",
    "ms_played": "msPlayed",
}

@st.cache_data
def load_data(uploaded_files: Optional[List] = None, data_dir: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from uploaded files or a local directory.
    
    Args:
        uploaded_files: List of uploaded files from Streamlit file_uploader.
        data_dir: Path to a directory containing JSON files (fallback).
        
    Returns:
        pd.DataFrame: Combined dataframe of listening history.
    """
    listening_history = []

    # 1. Try loading from uploaded files
    if uploaded_files:
        for file in uploaded_files:
            try:
                # streamlit uploaded files can be read directly by pd.read_json or need to be parsed
                listening_history.append(pd.read_json(file))
            except Exception as e:
                st.error(f"Error reading file {file.name}: {e}")
                continue
    
    # 2. If no uploaded files, try local directory (useful for testing/demos)
    elif data_dir and os.path.exists(data_dir):
        for filename in os.listdir(data_dir):
            if filename.endswith(".json"):
                try:
                    path = os.path.join(data_dir, filename)
                    listening_history.append(pd.read_json(path))
                except Exception as e:
                    st.warning(f"Could not read {filename}: {e}")
    
    if not listening_history:
        return pd.DataFrame()

    all_data = pd.concat(listening_history).reset_index(drop=True)
    
    # Standardize column names
    all_data = all_data.rename(
        columns={i: CHANGE_COLS[i] for i in CHANGE_COLS if i in all_data.columns}
    )
    
    return all_data
