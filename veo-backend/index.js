// =================================================================
//                 FINAL "REAL API" v2 (Using .predict)
// =================================================================

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { v1 } = require('@google-cloud/aiplatform');

// --- 1. INITIALIZE APP and PORT ---
const app = express();
const port = 3000;

// --- 2. SETUP MIDDLEWARE ---
app.use(cors());
app.use(express.json());

// --- 3. GOOGLE CLOUD CLIENT SETUP ---
let predictionServiceClient;
try {
    if (!process.env.GCP_PROJECT_ID || !process.env.GCP_LOCATION) {
        throw new Error('GCP_PROJECT_ID and GCP_LOCATION must be set in your .env file.');
    }
    const clientOptions = {
        apiEndpoint: `${process.env.GCP_LOCATION}-aiplatform.googleapis.com`,
    };
    predictionServiceClient = new v1.PredictionServiceClient(clientOptions);
    console.log("✅ Google Cloud client initialized successfully.");
} catch (error) {
    console.error("❌ FATAL ERROR: Could not initialize Google Cloud client.", error.message);
    process.exit(1);
}

// --- 4. API ROUTE (Simplified for Synchronous .predict) ---

app.post('/api/generate-video-from-text', async (req, res) => {
    const { prompt } = req.body;
    console.log(`[${new Date().toISOString()}] Received REAL request for prompt: "${prompt}"`);

    if (!prompt) {
        return res.status(400).json({ error: 'No prompt provided.' });
    }

    try {
        console.log('Attempting to generate video with .predict()...');

        const publisher = "google";
        const model = "veo-3.0-generate-preview";
        const endpoint = `projects/${process.env.GCP_PROJECT_ID}/locations/${process.env.GCP_LOCATION}/publishers/${publisher}/models/${model}`;

        // This payload structure is still a guess. The "View Code" button is the best way to confirm.
        const instances = [{ "prompt": prompt }];
        const parameters = { "videoLength": "8s" };

        const request = { endpoint, instances, parameters };

        // Use the correct .predict() method
        const [response] = await predictionServiceClient.predict(request);
        
        console.log('✅ Received successful response from Vertex AI.');
        
        // The structure of the response.predictions object needs to be verified from the docs.
        // We assume the video URL is in the first prediction.
        const videoUrl = response.predictions[0].structValue.fields.url.stringValue;

        // Since .predict() is synchronous, we can return the URL directly.
        // No polling needed for this approach.
        res.status(200).json({
            status: 'completed',
            videoUrl: videoUrl
        });

    } catch (error) {
        console.error('❌ Google Cloud API Error Details:', error);
        res.status(500).json({
            error: 'Failed during video generation on Vertex AI.',
            details: error.message
        });
    }
});


// We don't need the /video-status endpoint if we use the synchronous .predict() method.
// You can remove it or leave it commented out.

// --- 5. START THE SERVER ---
app.listen(port, (err) => {
    if (err) {
        console.error("❌ Error starting server:", err);
        return;
    }
    console.log('----------------------------------------------------');
    console.log(`✅ REAL API Backend is ALIVE on http://localhost:${port}`);
    console.log('   (Using synchronous .predict() method)');
    console.log('----------------------------------------------------');
});