# 🚀 Al-Powered Crop Yield Prediction and Optimization

This README provides an overview of the project, including team details, relevant links, tasks completed, tech stack, key features, and steps to run the project locally
---

## 👥 Team Details  

- **Team Name:** Hack-a-holics  
- **Team Leader:** @SumitJha84  

### 🧑‍🤝‍🧑 Team Members
- Sumit Jha - 2023UCB6065 - @SumitJha84  
- Arpita Chhabra - 2023UBT1094 - @Arpitaacodes  
- Ritika  - 2023UBT1024 - @ritika-works  
- Parth Bisht - ROLL_NUMBER - @  
- Jai Verma - 2023UEI2821 - @Jaiverma0923  
- Abdul Raqeeb - 2023UCB6048 - @Raqeeb786  

---

## 🔗 Project Links  

- 📑 **SIH Presentation:** [[Final SIH Presentation]](https://github.com/SumitJha84/SIH-25/blob/main/files/internal_PPT_HACK-O-HOLICS.pdf)  
- 🎥 **Video Demonstration:** [[Watch Video]](https://www.youtube.com/watch?v=gpZB9ZwrJmY)
- 🌐 **Live Deployment:** [[View Deployment]](https://sih-25-frontend.vercel.app/) 
- 💻 **Source Code:** [[GitHub Repository]](https://github.com/SumitJha84/SIH-25.git)
- 📚 **Additional Resource_1:** [[soil data]](https://agri.odisha.gov.in/sites/default/files/2025-05/OAS%20A4.pdf)
- 📚 **Additional Resource_2:** [[past yield data]](https://idc.icrisat.org/idc/wp-content/uploads/2020/12/Odisha%20Soil%20Atlas%20dated%202.12.2020.pdf)


---

## ✅ Tasks Completed  

- [x] Requirement analysis & brainstorming  
- [x] Problem statement understanding  
- [x] UI/UX design & wireframing  
- [x] Backend development  
- [x] Frontend integration  
- [x] Testing & debugging  
- [x] Final presentation & video preparation  

---

## 🛠️ Tech Stack  

- **Frontend:** React.js / Tailwind CSS / typescript  
- **Backend:** Node.js / Express.js /  Fast API's
- **Database:** MongoDB / PostgreSQL  
- **Deployment:** Vercel  
- **Other Tools:** Git, GitHub, Figma, Postman, etc.  

---

## 🌟 Key Features  

- Feature 1: AI-Driven Multi-Source Integration
              Combines agriculture, weather, and soil data to generate holistic, hyper-local crop yield 
              predictions.
- Feature 2:  Dynamic, Context-Aware Recommendations
 Continuously updates farming advice based on real-time conditions and farmer feedback 
for maximum accuracy.
- Feature 3: Offline-First Access with Local Language Support
 Runs without internet, supports Odia voice, SMS, and IVR—built for rural farmers using 
feature phones or low-end smartphones. 
- Feature 4: Built for Small-Scale & Marginal Farmers
 Designed to solve the challenges of low-resource farmers often ignored by large agri-tech 
platforms. 
---

## 🖥️ Run Project Locally  

Follow these steps to run the project on your local machine:  

```bash
# Clone the repository
git clone [GITHUB_LINK_TO_THE_REPO](https://github.com/SumitJha84/SIH-25.git)

# Navigate to project folder
cd SIH-25

# Install dependencies
npm install   # or yarn install

# Start development server
# For frontend
cd frontend 
npm run dev   # or yarn dev

# For backend
cd..
cd backend
npm start 

# RUN ON TERMINAL FOR ACTIVATING PREDICTION MODEL API :

uvicorn backend.yield_prediction_model.model_api:app --reload

#example input:
# {
#   "Crop": "Rice",
#   "Season": "Kharif",
#   "Dist_Name": "Cuttack",
#   "Year": 2023,
#   "PreMonsoon_MAM_max": 38.5,
#   "Monsoon_JJAS_max": 32.3,
#   "PostMonsoon_OND_max": 29.1,
#   "Winter_JF_max": 27.8,
#   "Annual_MaxTemp": 31.5,
#   "PreMonsoon_MAM_min": 23.6,
#   "Monsoon_JJAS_min": 25.1,
#   "PostMonsoon_OND_min": 18.5,
#   "Winter_JF_min": 15.2,
#   "Annual_minTemp": 22.6,
#   "JJAS": 1400.5,
#   "OND": 210.3,
#   "JF": 28.4,
#   "MAM": 85.2,
#   "Annual": 1724.4,
#   "Soil_Acidic": 22.1,
#   "Soil_Alkaline": 5.4,
#   "Soil_B": 0.5,
#   "Soil_Ca": 3.4,
#   "Soil_Cu": 1.2,
#   "Soil_EC_conditions": 0.8,
#   "Soil_Fe": 4.3,
#   "Soil_K": 320.5,
#   "Soil_Mg": 2.8,
#   "Soil_Mn": 1.1,
#   "Soil_Neutral": 71.2,
#   "Soil_OC": 0.78,
#   "Soil_P": 42.0,
#   "Soil_S": 28.7,
#   "Soil_Zn": 1.6,
#   "Soil_samples": 101.0
# }

