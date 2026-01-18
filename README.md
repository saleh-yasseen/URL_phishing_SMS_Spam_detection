# Phishing URL & SMS Spam Detection API

This project is a Machine Learning-based API designed to detect phishing URLs and classify SMS messages as spam or ham (legitimate). It is built using **FastAPI** for high performance and **MongoDB** for logging user payloads.

## 🚀 Features

- **Phishing URL Detection**: Analyzes URLs to extract features and predicts if they are legitimate or phishing.
- **SMS Spam Detection**: Classifies SMS text messages as spam or legitimate using Natural Language Processing (NLP).
- **Asynchronous Processing**: Uses FastAPI's async capabilities for efficient request handling.
- **Persistent Logging**: Stores all analyzed payloads and results in a MongoDB database.
- **User History**: Retrieve past analysis results for specific users.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [MongoDB](https://www.mongodb.com/) (using Motor driver)
- **Machine Learning**: Scikit-learn, XGBoost, NLTK
- **Data Processing**: Pandas, NumPy, BeautifulSoup4

## ⚙️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/saleh-yasseen/URL_phishing_SMS_Spam_detection.git
    cd URL_phishing_SMS_Spam_detection
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLTK Data**:
    If running for the first time, the application will automatically download necessary NLTK datasets (stopwords, wordnet, punkt).

## 🏃‍♂️ Usage

To run the application locally:

```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### API Endpoints

#### 1. Analyze Payload (`POST /extract-features`)

Analyzes a URL or SMS message.

**Request Body:**
```json
{
  "payload": "http://example.com",
  "model": "url",
  "uid": "user_123"
}
```
*   `model`: Use `"url"` for URL detection or `"sms"` for SMS spam detection.

**Response:**
```json
{
  "id": "65a123...",
  "payload": "http://example.com",
  "model": "url",
  "created_at": "2024-01-01T12:00:00",
  "status": 0,
  "uid": "user_123"
}
```
*   `status`:
    *   **0**: Legitimate / Ham
    *   **1** (or non-zero): Phishing / Spam

#### 2. Get User History (`GET /user-payloads/{uid}`)

Retrieves all past requests made by a specific user.

**Example:** `GET http://127.0.0.1:8000/user-payloads/user_123`

## 📂 Project Structure

- `main.py`: Entry point of the FastAPI application.
- `feature.py`: Feature extraction logic for URL detection.
- `sms_model_prep.py`: Preprocessing logic for SMS spam detection.
- `sms/`: Contains SMS datasets and pickled models.
- `pickle/`: Contains the URL detection model.
- `requirements.txt`: Python dependencies.

## 🔧 Configuration

**Note:** The MongoDB connection string is currently configured in `main.py`. For production, it is recommended to use environment variables for sensitive credentials.
