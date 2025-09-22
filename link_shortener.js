const express = require('express');
const crypto = require('crypto');
const path = require('path');
const app = express();
const port = 8081;

// In-memory storage for URLs (in production, use a database)
const urlDatabase = {};

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from public directory
app.use(express.static('public'));

// Function to generate a short code
function generateShortCode() {
  return crypto.randomBytes(3).toString('hex');
}

// Redirect endpoint
app.get('/:shortCode', (req, res) => {
  const shortCode = req.params.shortCode;
  const originalUrl = urlDatabase[shortCode];
  
  if (originalUrl) {
    res.redirect(originalUrl);
  } else {
    res.status(404).send('Short URL not found');
  }
});

// API endpoint to shorten URLs
app.post('/shorten', (req, res) => {
  const originalUrl = req.body.url;
  
  if (!originalUrl) {
    return res.status(400).json({ error: 'URL is required' });
  }
  
  // Generate a unique short code
  let shortCode = generateShortCode();
  while (urlDatabase[shortCode]) {
    shortCode = generateShortCode();
  }
  
  // Store the mapping
  urlDatabase[shortCode] = originalUrl;
  
  // Return the short URL
  const shortUrl = `http://localhost:${port}/${shortCode}`;
  res.json({ shortUrl, shortCode });
});

// Main page
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>BeEF Link Shortener</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        input[type="url"] { width: 70%; padding: 10px; }
        button { padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background: #45a049; }
        #result { margin-top: 20px; padding: 10px; background: #e9f7ef; border-radius: 4px; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>BeEF Link Shortener</h1>
        <p>Enter the BeEF hook URL to shorten it:</p>
        <form id="shortenForm">
          <input type="url" id="urlInput" placeholder="http://localhost:3000/hook.js" required>
          <button type="submit">Shorten</button>
        </form>
        <div id="result"></div>
      </div>
      <script>
        document.getElementById('shortenForm').addEventListener('submit', async (e) => {
          e.preventDefault();
          const url = document.getElementById('urlInput').value;
          const response = await fetch('/shorten', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
          });
          const data = await response.json();
          if (data.shortUrl) {
            document.getElementById('result').innerHTML = 
              '<p><strong>Short URL:</strong> <a href="' + data.shortUrl + '" target="_blank">' + data.shortUrl + '</a></p>';
          } else {
            document.getElementById('result').innerHTML = '<p>Error: ' + data.error + '</p>';
          }
        });
      </script>
    </body>
    </html>
  `);
});

app.listen(port, () => {
  console.log(`Link shortener running on http://localhost:${port}`);
  console.log(`BeEF hook URL: http://localhost:3000/hook.js`);
  console.log('Shorten it by visiting this page and entering the hook URL');
});