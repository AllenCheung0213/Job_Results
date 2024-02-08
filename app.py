from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
import logging
from datetime import datetime, timedelta
import csv
import imaplib
import email
from email.utils import parsedate_to_datetime
import re

app = Flask(__name__)
# Securely load the secret key from an environment variable
app.secret_key = os.getenv('SECRET_KEY', 'default_fallback_secret_key')

# Basic logging setup with improved format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load email credentials securely from environment variables
EMAIL = os.getenv('MY_EMAIL')
PASSWORD = os.getenv('MY_PASSWORD')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        return redirect(url_for('fetch_emails'))
    return render_template('login.html')

@app.route('/fetch_emails')
def fetch_emails():
    if 'email' not in session or 'password' not in session:
        flash('Please login to view this page.')
        return redirect(url_for('login'))
    
    email_address = session['email']
    password = session['password']
    
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(email_address, password)
        applications = list(process_emails(imap))  # Convert generator to list
        write_csv(applications)
        flash("Emails processed and saved to CSV successfully.")
    except Exception as e:
        flash(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")
    finally:
        imap.logout()
    
    return redirect(url_for('show_results'))

@app.route('/show_results')
def show_results():
    # Read data from CSV file to display
    applications = []
    try:
        with open('jobs.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                applications.append(row)
    except FileNotFoundError:
        flash('No results found. Please fetch emails first.')
    except Exception as e:
        flash(f'An error occurred while reading the CSV: {e}')
        logging.error(f'An error occurred while reading the CSV: {e}')
    
    return render_template('results.html', applications=applications)

# Extract details function remains the same
def extract_details(email_body):
    job_title_search = re.search('Job Title: (.+)', email_body)
    position_title_search = re.search('Position Title: (.+)', email_body)
    
    job_title = job_title_search.group(1) if job_title_search else "Unknown"
    position_title = position_title_search.group(1) if position_title_search else "Unknown"
    
    # Example for extracting decision, adapt the pattern to fit your email format
    decision_search = re.search('Decision: (.+)', email_body)
    decision = decision_search.group(1) if decision_search else "Pending"
    
    return job_title, position_title, decision


# Improved process_emails function with better error handling and logging
def process_emails(imap):
    try:
        imap.select('"[Gmail]/All Mail"')
        since_date = (datetime.now() - timedelta(days=365)).strftime('%d-%b-%Y')
        result, data = imap.search(None, f'(SINCE {since_date}) SUBJECT "Application Confirmation"')
        
        if result == "OK":
            for num in data[0].split():
                result, data = imap.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                email_msg = email.message_from_bytes(raw_email)
                
                if email_msg.is_multipart():
                    for part in email_msg.walk():
                        if part.get_content_type() == "text/plain":
                            payload = part.get_payload(decode=True).decode()
                            yield extract_details(payload)
                else:
                    payload = email_msg.get_payload(decode=True).decode()
                    yield extract_details(payload)
    except Exception as e:
        logging.error(f"Failed to process emails: {e}")
        raise


# Optimized write_csv function for better performance and error handling
def write_csv(applications):
    try:
        with open('jobs.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Job Title", "Position Title", "Decision", "Date Applied"])
            for app in applications:
                writer.writerow(app)
    except IOError as e:
        logging.error(f"Failed to write to CSV: {e}")
        raise  # Re-raise exception for upstream error handling


if __name__ == '__main__':
    # Load configuration from environment variables for production readiness
    app.run(host=os.getenv('FLASK_HOST', '127.0.0.1'), port=int(os.getenv('FLASK_PORT', 5000)), debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
