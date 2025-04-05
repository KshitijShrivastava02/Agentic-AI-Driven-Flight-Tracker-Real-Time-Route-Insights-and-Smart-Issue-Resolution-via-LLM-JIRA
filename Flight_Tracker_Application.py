import streamlit as st 
import pandas as pd
import folium
from streamlit_folium import folium_static
import time
import os
from dotenv import load_dotenv
from jira import JIRA
import requests
import base64
from math import radians, sin, cos, sqrt, atan2

#This is My Fully Functional Code with all the testing reuirements as well,  FINAL to be submit 
#
# Load environment variables
load_dotenv()

# JIRA and Other API Configuration
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_PROJECT_KEY = "KAN"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AVIATION_API_KEY = os.getenv("AVIATION_API_KEY")

# Initialize JIRA safely
jira = None
if JIRA_DOMAIN and JIRA_API_TOKEN:
    try:
        jira_options = {"server": JIRA_DOMAIN.strip()}
        jira = JIRA(options=jira_options, basic_auth=("sm24mtech14005@iith.ac.in", JIRA_API_TOKEN))
        print("✅ JIRA Connected Successfully!")

        # Automatically create Requirement Epic
        epic_dict = {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": "Flight Tracking Feature Requirement",
            "description": "Implement real-time flight tracking with AI support.",
            "issuetype": {"name": "Epic"},
        }
        epic = jira.create_issue(fields=epic_dict)
        print(f"✅ Requirement Epic created: {epic.key}")

        # Automatically create a linked Test Task
        test_dict = {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": "Test: Flight tracking animation and location descriptions",
            "description": "Verify map rendering, LLM responses, and UI consistency.",
            "issuetype": {"name": "Task"},
        }
        test_issue = jira.create_issue(fields=test_dict)
        print(f"✅ Testing Task created: {test_issue.key}")

    except Exception as e:
        print(f"❌ JIRA Connection Failed: {e}")
else:
    print("❌ JIRA Credentials are missing!")

# Load flight path data
flight_path_file = r"D:\\Flight_Aviation\\flight_path_indore_hyderabad.csv"
df = pd.read_csv(flight_path_file)

# Coordinates for Indore and Hyderabad
indore_lat, indore_lon = 22.7196, 75.8577
hyderabad_lat, hyderabad_lon = 17.3850, 78.4867

# Haversine Distance Calculation
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad, lon1_rad = radians(lat1), radians(lon1)
    lat2_rad, lon2_rad = radians(lat2), radians(lon2)
    dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Total static distance between Indore and Hyderabad
static_total_distance = haversine_distance(indore_lat, indore_lon, hyderabad_lat, hyderabad_lon)

# Load and encode your local background image
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set background image
local_image_path = "D:\\Flight_Aviation\\flight_image.jpg"
encoded_image = get_base64_encoded_image(local_image_path)

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)),
                    url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# Function to get famous location description using LLM
def get_place_description(lat, lon):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        prompt = f"You are a tour guide. Tell in 4-5 lines what is famous about the place located at latitude {lat} and longitude {lon}. Make it sound like a welcome to a chief guest."
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful and engaging travel assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "Could not fetch location details."

# Flight tracking function
def track_flight(flight_number):
    st.subheader(f"Tracking Flight: {flight_number}")
    current_distance = 0
    path_coords = list(zip(df['Latitude'], df['Longitude']))

    flight_map = folium.Map(location=path_coords[0], zoom_start=6)
    folium.PolyLine(path_coords, color="blue", weight=2.5, opacity=0.8).add_to(flight_map)

    map_placeholder = st.empty()
    stats_placeholder = st.empty()
    right_placeholder = st.empty()

    with map_placeholder:
        folium_static(flight_map)

    speed_kmph = 657
    displayed_locations = set()

    for i in range(1, len(path_coords)):
        lat1, lon1 = path_coords[i - 1]
        lat2, lon2 = path_coords[i]

        step_distance = haversine_distance(lat1, lon1, lat2, lon2)
        current_distance += step_distance

        flight_map = folium.Map(location=[lat2, lon2], zoom_start=6)
        folium.PolyLine(path_coords, color="blue", weight=2.5, opacity=0.8).add_to(flight_map)
        flight_icon = folium.Icon(icon="plane", prefix="fa", color="blue")
        folium.Marker([lat2, lon2], icon=flight_icon, popup=f"Flight {flight_number}").add_to(flight_map)

        with map_placeholder:
            folium_static(flight_map)

        with stats_placeholder.container():
            st.markdown(f"""
            <div style='padding: 10px; background-color: rgba(255,255,255,0.7); border-radius: 10px;'>
                <h4 style='margin: 0;'>🛫 Speed: <span style='color: green;'>{speed_kmph:.1f} km/h</span></h4>
                <h4 style='margin: 0;'>🧭 Distance Covered: <span style='color: blue;'>{current_distance:.2f} / {static_total_distance:.0f} km</span></h4>
            </div>
            """, unsafe_allow_html=True)

        coord_key = (round(lat2, 2), round(lon2, 2))
        if coord_key not in displayed_locations:
            description = get_place_description(lat2, lon2)
            with right_placeholder.container():
                st.markdown(f"""
                <div style='background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin-top: 10px;'>
                    <h4>📍 Hi Chief Guest, you are passing from here!</h4>
                    <p>{description}</p>
                </div>
                """, unsafe_allow_html=True)
            displayed_locations.add(coord_key)

        time.sleep(0.3)

    st.success("✅ Flight has reached Hyderabad!")

# Streamlit UI
st.title("✈️ Flight Tracking: Indore to Hyderabad")

st.header("📋 Flight Info: Indore to Hyderabad (Live)")

def fetch_flight_data():
    params = {
        "access_key": AVIATION_API_KEY,
        "dep_iata": "IDR",
        "arr_iata": "HYD"
    }
    try:
        response = requests.get("http://api.aviationstack.com/v1/flights", params=params)
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        st.error(f"Failed to fetch flight info: {e}")
        return []

flights = fetch_flight_data()

if not flights:
    st.warning("No flight data found for today.")
else:
    for flight in flights[:3]:
        airline = flight["airline"]["name"]
        flight_number = flight["flight"]["iata"]
        departure = flight["departure"]
        arrival = flight["arrival"]
        live_status = flight.get("live", None)

        dep_gate = departure.get("gate", "N/A")
        arr_gate = arrival.get("gate", "N/A")
        dep_scheduled = departure.get("scheduled", "N/A")
        arr_scheduled = arrival.get("scheduled", "N/A")
        delay = departure.get("delay", "0")

        with st.expander(f"✈️ {airline} | Flight {flight_number}"):
            st.markdown(f"""
            - **Status:** `{flight['flight_status'].upper()}`
            - **Gate Info:** Departure Gate: `{dep_gate}` | Arrival Gate: `{arr_gate}`
            - **Scheduled Time:** 🛫 `{dep_scheduled}` → 🛬 `{arr_scheduled}`
            - **Delay:** `{delay}` minutes
            """)

flight_number = st.text_input("Enter Flight Number", "6E6916")
if st.button("Start Tracking"):
    track_flight(flight_number)

st.sidebar.title("🤖 AI Chatbot Support")
user_query = st.sidebar.text_area("Enter your complaint", "")

if st.sidebar.button("Submit Complaint"):
    if GROQ_API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": "You are a polite and helpful customer support agent for an airline."},
                    {"role": "user", "content": f"Customer complaint: {user_query}"}
                ],
                "temperature": 0.7,
                "max_tokens": 100
            }

            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
            result = response.json()
            ai_response = result['choices'][0]['message']['content'].strip()
            st.sidebar.write(f"💬 AI Response: {ai_response}")
        except Exception as e:
            st.sidebar.error(f"❌ AI Response Failed: {e}")
    else:
        st.sidebar.error("❌ GROQ API Key is missing!")

    if jira:
        issue_dict = {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": "Passenger Complaint",
            "description": user_query,
            "issuetype": {"name": "Task"},
        }
        try:
            new_issue = jira.create_issue(fields=issue_dict)
            st.sidebar.success(f"✅ Jira ticket created: {new_issue.key}")
        except Exception as e:
            st.sidebar.error(f"❌ Jira Ticket Creation Failed: {e}")
    else:
        st.sidebar.error("❌ JIRA Connection Failed. Cannot create ticket.")
