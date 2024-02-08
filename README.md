# Flask Email Processor

## Overview

This Flask application allows users to log in with their email credentials and processes emails from their inbox that match specific criteria (e.g., emails related to job applications). The processed emails are then saved into a CSV file, summarizing the job title, position title, decision status, and application date.

## Features

- Secure login with email credentials.
- Fetching and processing emails with specific subject lines.
- Extracting relevant information from emails and saving it to a CSV file.
- Simple and user-friendly web interface.

## Installation

### Prerequisites

- Python 3.6 or higher
- Flask
- A Gmail account with IMAP access enabled

### Setup

1. **Clone the repository**

   ```bash
   git clone https://your-repository-url.git
   cd flask-email-processor
   
2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install required packages**
   
   ```bash
   pip install Flask

4. **Set environment variables**
Replace your_email@gmail.com and your_password with your actual email and password. For Unix-based systems:

  ```bash
  export MY_EMAIL='your_email@gmail.com'
  export MY_PASSWORD='your_password'
```

*For Windows:*

  ```bash
  set MY_EMAIL=your_email@gmail.com
  set MY_PASSWORD=your_password
  ```

5. **Run the application**
   ```bash
   python app.py

The application will be accessible at http://127.0.0.1:5000/.

## Usage

- Navigate to http://127.0.0.1:5000/ in your web browser.
- Log in using your email credentials.
- Once logged in, the application will automatically process your emails and save the relevant data into a CSV file.
- The results page will confirm the successful processing of your emails.

## Security Notes

- This application is designed for educational purposes and demonstrates basic Flask and IMAP integration.
- Storing email credentials in environment variables or directly in the application is not secure for production environments. Consider using OAuth2 for Gmail access in production applications.
- Ensure you follow best practices for web application security, especially when handling sensitive information.



