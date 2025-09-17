// backend/index.js
const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();

// --- START: FINAL CORS CONFIGURATION ---

const allowedOrigins = [
  'http://localhost:5173',          // Local development
  'https://sih-25-frontend.vercel.app' // Deployed frontend
];

const corsOptions = {
  origin: (origin, callback) => {
    // On localhost, the 'origin' header might be undefined during server-side rendering or certain requests.
    // The !origin condition allows these requests to pass, which is essential for local development.
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
  credentials: true,
  optionsSuccessStatus: 204 // Some legacy browsers choke on 200
};

// Use this single middleware for all CORS handling.
// It will handle preflight OPTIONS requests automatically.
app.use(cors(corsOptions));

// --- END: FINAL CORS CONFIGURATION ---

app.use(express.json());

// Routes
const weatherRoutes = require('./route/weatherRoutes');
app.use('/api/weather', weatherRoutes);

// Only start server for local development
if (require.main === module) {
  const PORT = process.env.PORT || 5000;
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}

// Export the app for Vercel
module.exports = app;