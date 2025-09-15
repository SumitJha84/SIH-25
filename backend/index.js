// backend/index.js
const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();

const allowedOrigins = [
  'http://localhost:5173', // For your local development
  'https://sih-25-frontend.vercel.app' // Your deployed frontend
];

const corsOptions = {
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  }
};

// --- THIS IS THE KEY CHANGE ---
// Handle preflight OPTIONS requests for all routes
app.options('*', cors(corsOptions));

// Use the CORS options for all other requests
app.use(cors(corsOptions));
// --- END OF CONFIGURATION ---

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