# Coastal Threat Alert System: AI-Powered Coastal Resilience Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com/)

## 🚨 The Problem

Coastal communities in India are on the front lines of climate change, facing increasing threats from cyclones, storm surges, erosion, and pollution. Current early-warning systems are often:
- **Siloed:** Data sources are disconnected, preventing a unified view of threats.
- **Slow:** Manual analysis delays crucial alerts, costing precious evacuation time.
- **Ineffective:** Alerts often fail to drive coordinated action, leading to chaos, economic damage, and loss of life.

## 💡 Our Solution: CTAS - Threat Detection System

CTAS is a comprehensive, AI-driven resilience platform that moves beyond simple alerts. We don't just detect threats; we manage the entire response lifecycle—from AI-powered prediction and community preparedness to smart, coordinated evacuation and resource management.

## ✨ Features

### Core Features
- **Unified Threat Dashboard:** A real-time geospatial dashboard visualizing data from IMD, INCOIS, and other sources on an interactive map.
- **AI-Powered Threat Detection:** Machine learning models analyze sensor and satellite data to detect anomalies and classify threats (cyclones, floods) automatically, providing maximum lead time.
- **Multi-Channel Alert System:** Disseminate alerts via SMS (Twilio), mobile push notifications (Firebase), and web dashboards to ensure they reach everyone, from fisherfolk to authorities.

### Unique & Winning Features
1.  **Smart Evacuation Routing & Resource Mapping:**
    - **Solves:** Post-alert chaos and inefficient resource allocation.
    - **How:** During an alert, the system calculates optimal evacuation routes to the nearest shelters, avoiding predicted flood zones. It also provides authorities with a real-time view of shelter capacity and resource (food, water, kits) levels.

2.  **Gamified Preparedness Drills & Community Verification:**
    - **Solves:** Community complacency and lack of ground-truth data.
    - **How:** A mobile-friendly interface allows communities to participate in monthly mock drills, earning points and badges. During real events, users can provide one-tap "ground truth" verification (e.g., "Flooding here?"), turning citizens into a vital sensor network.

### Future Enhancement Roadmap
- Integration of satellite imagery AI to detect algal blooms and illegal dumping.
- Federated Learning model for a decentralized, buoy-based sensor network.
- Blockchain-based audit trail for alerts and actions to ensure transparency.
- AR mobile app for visualizing evacuation routes in the real world.

## 🛠️ Tech Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend** | React.js, Leaflet.js / CesiumJS, Chart.js, Tailwind CSS | Modern, component-based UI with powerful mapping and visualization. |
| **Backend** | FastAPI, Uvicorn, Python (Python 3.10+) | High-performance, asynchronous API framework with automatic docs. |
| **Database & Auth** | Supabase | Open-source Firebase alternative with real-time PostgreSQL DB and auth. |
| **AI/ML** | Scikit-learn, XGBoost, TensorFlow, Pandas, NumPy | For building and serving anomaly detection and classification models. |
| **APIs & Services** | IMD API, INCOIS API, Twilio (SMS), Firebase Cloud Messaging (Push), GraphHopper/OSRM (Routing) | Free tiers and robust Indian data sources. |
| **DevOps & Deployment** | Docker, GitHub Actions, Vercel (Frontend), Railway (Backend) | Containerized for easy setup, deployed on free-tier platforms. |

## 🧠 Our AI Models

We employ a multi-model strategy for precision:
1.  **Anomaly Detection:** An `Isolation Forest` model trained on historical data to flag unexpected sensor readings.
2.  **Threat Classification:** A `Gradient Boosting (XGBoost)` model trained on historical alert data to classify incoming data into specific threat levels and types.

## 🚀 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/nereid-platform.git
    cd nereid-platform
    ```

2.  **Backend Setup:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```

3.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install
    npm start
    ```

4.  **Environment Variables:** Create a `.env` file based on `.env.example` and populate your API keys for Twilio, Supabase, etc.

## 📋 Usage

1.  **View Dashboard:** Open `http://localhost:3000` to see the live dashboard.
2.  **Simulate a Threat:** Use the admin panel to trigger a mock cyclone alert.
3.  **See the Flow:** Watch as alerts are generated, evacuation routes are calculated on the map, and mock SMS notifications are sent.
4.  **Try a Drill:** Open the mobile view and click "Start Drill" to experience the gamified preparedness system.

## 👨‍💻 Team

*   **Frontend Team:** [Team Member 1 & 2] - UI/UX, Dashboard, Map Visualizations, Drill Interface.
*   **Backend Team:** [Team Member 3 & 4] - FastAPI Server, AI/ML Models, Database Architecture, API Integrations.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Data provided by the **India Meteorological Department (IMD)** and **Indian National Centre for Ocean Information Services (INCOIS)**.
- Built for HackOut'25.
