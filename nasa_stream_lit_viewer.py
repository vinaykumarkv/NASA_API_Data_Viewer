import requests
from datetime import date, timedelta
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
load_dotenv()
api_key = os.getenv("NASA_API_KEY")

#get data from nasa api
def get_nasa_data(api_key,start_date, end_date):
    params={
        "api_key": api_key,
        "start_date": start_date,
        "end_date": end_date,
        "thumbs" : True
    }
    response = requests.get("https://api.nasa.gov/planetary/apod",params=params)
    content = response.json()
    return content


#Stream lit app start
today = date.today()
default_start = today - timedelta(days=7)

date_range = st.date_input(
    "Select Date Range",
    value=(default_start, today),
    format="YYYY-MM-DD"
)

st.title("NASA API")
st.sidebar.subheader("Top Images from NASA API")

if st.button("Search"):
    # Validate that both start and end dates were selected
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        st.success(f"Searching from {start_date} to {end_date}...")
        content = get_nasa_data(api_key, start_date, end_date)
        for item in content:
            st.subheader(f"Title: {item['title']}, Date: {item['date']}")
            if item["media_type"] == "image":
                image_r = requests.get(item["url"])
                st.image(image_r.content)
            elif item["media_type"] == "video":
                image_g = requests.get(item["thumbnail_url"])
                st.image(image_g.content)

            st.write(f"{item['explanation']}")
    else:
        st.warning("Please select both a start and end date.")
