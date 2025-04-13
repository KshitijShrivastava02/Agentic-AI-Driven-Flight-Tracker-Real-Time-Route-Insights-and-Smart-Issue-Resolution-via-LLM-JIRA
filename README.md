# Agentic AI-Driven Flight Tracker with Real-Time Route Insights and Smart Issue Resolution via LLM & JIRA

This project is a powerful AI-integrated flight tracking application built using **Streamlit**, **Folium**, **LLMs (GROQ's LLaMA3)**, and **JIRA**. It visualizes a real-time animated flight journey from Indore to Hyderabad and provides smart, contextual information about locations en route. Additionally, it allows passengers to submit complaints, which are responded to using an LLM and logged directly into a JIRA board.

---
![image](https://github.com/user-attachments/assets/a3034d9c-45bd-4bc1-8d49-0e1eb865bedb)
![image](https://github.com/user-attachments/assets/c2a2e18f-9543-4062-b1ef-3bbe519c04b7)



## 🚀 Features

- 🗺️ **Real-Time Animated Flight Tracking** on an interactive Folium map.
- 📍 **Dynamic Descriptions** of popular places en route using an LLM prompt.
- 📊 **Live Flight Data** using AviationStack API.
- 🤖 **AI Chatbot Support** for passenger complaints.
- 🛠️ **Automated Ticketing System** by integrating directly with JIRA API.
- 🎨 **Beautiful UI** with a gradient and image background for rich UX.

---

## 🧠 Methodology

The application was developed with the following components and strategies:

### 📌 1. **Data Visualization with Folium**
- A CSV file containing lat-long pairs from Indore to Hyderabad is used here as real time coordinaes is taking a long time (2-3 minutes) so i prefered to collect the coordinates in a CSV file for example here i have taken Indore to Hyderabad .
- The coordinates are animated on the map to simulate real-time flight motion.
- The distance covered is updated live using the **Haversine formula**.

### 📌 2. **Flight Information API**
- Uses [AviationStack API](https://aviationstack.com/) to fetch real-time flights for example here in this project between Indore (IDR) and Hyderabad (HYD).
- Displays airline, gate, status, schedule, and delay info.

### 📌 3. **Place Insights Using LLM**
- Each significant location is reverse geo-analyzed.
- A prompt is sent to **Groq's LLaMA 3 model** to generate 4–5 line descriptions of the place above which our flight is passing through by checking its lon-lat coordinates.

### 📌 4. **Smart Complaint Handling ChatBot**
- Complaints entered by users are answered using LLaMA3.
- Automatically creates a JIRA Task Ticket under a specific project (`KAN`), categorized as "Passenger Complaint".

### 📌 5. **JIRA Integration**
- Automatically creates:
  - An **Epic** for Flight Tracker Requirements.
  - A **Task** for Testing and Validation.
  - **New Tickets** for customer issues.
![image](https://github.com/user-attachments/assets/3485ca5f-0cd1-4b60-b5fe-5696fae6c0db)

---

## 🖥️ Installation & Setup

### 1. **Clone this repository**
```bash
git clone https://github.com/your-username/agentic-flight-tracker.git
cd agentic-flight-tracker
```
### 2. **Install dependencies**
```bash
git clone https://github.com/your-username/agentic-flight-tracker.git
cd agentic-flight-tracker
```
### 2. **Setup environment variables**
```bash
Create a .env file in the project root:
JIRA_API_TOKEN=your_jira_api_token
JIRA_DOMAIN=https://your-domain.atlassian.net
GROQ_API_KEY=your_groq_api_key
AVIATION_API_KEY=your_aviationstack_api_key

```
### 2. **Running the UI**
```bash
streamlit run D:\Flight_Aviation\Flight_Tracker_Application.py
```
## Contact
**Developer: Kshitij Shrivastava**

**📧 Email: ranveer.shrivastava.rs@gmail.com**

**📍 Indian Institute of Technology Hyderabad**

