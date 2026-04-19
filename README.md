# HealthSync - Intelligent Medical Diagnostics Platform

🚀 **Live Demo:** [https://healthsync-mvru.onrender.com](https://healthsync-mvru.onrender.com)

HealthSync is a modern, AI-driven medical imaging analysis platform. Designed for both healthcare professionals and patients, it leverages advanced machine learning models (XGBoost) combined with computer vision (OpenCV) to identify anomalies such as Fractures and Tuberculosis in X-ray imagery.

---

## 🌟 Platform Highlights
- **High-Accuracy Screening:** Instant X-ray evaluations using trained XGBoost classification models.
- **Interactive Dashboards:** Dedicated experiences for Doctors (Analytics, patient overview) and Patients (Scan History).
- **Responsive & Modern UI:** A secure, intuitive frontend tailored for cross-device compatibility.
- **Explainable AI:** Provides clear reasoning behind the diagnostic features and metrics.
- **Privacy-First:** Standardized setup for role-based access, complete action logging, and user data consent.

---

## ⚙️ System Requirements

Ensure you have the required machine learning model binary files in your root directory before launching the app:
- `Fracture_XGBoost`
- `TB_XGBoost`

### Installation & Setup

1. **Obtain the Source Code:**
   ```bash
   git clone <repository-url>
   cd HealthSync
   ```

2. **Establish the Environment (Recommended):**
   ```bash
   python -m venv .venv
   
   # For Windows:
   .venv\Scripts\activate
   
   # For Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install Core Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Application:**
   ```bash
   python run.py
   ```
   Once started, the application can be accessed via `http://localhost:5000` or `https://localhost:5000` (if self-signed certificates generate correctly).

---

For inquiries or features requests, please submit an issue or open a pull request on GitHub.
