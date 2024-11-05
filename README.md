# Email Reader and AI Processor

This Python project connects to an IMAP email account to read, classify, and process emails using OpenAI's GPT model. It also sends polite responses to non-spam emails and provides a graphical user interface (GUI) using Tkinter.

## Features
- **Read and Process Emails**: Connects to an IMAP server, reads the most recent emails, and classifies them as spam or not using AI.
- **Spam Detection**: Uses OpenAI to detect spam emails and deletes them automatically.
- **AI-Powered Responses**: Generates polite and professional email responses using OpenAI.
- **Email Deletion**: Deletes processed emails from the inbox.
- **User Interface**: A Tkinter-based GUI to view emails and AI-generated responses.

## Setup Instructions
1. Clone this repository to your local machine.
2. Install the required dependencies:

    Replace placeholders in the script:
        EMAIL_ACCOUNT: Your email address.
        PASSWORD: Your email password.
        IMAP_SERVER: Your email service's IMAP server.
        SMTP_SERVER: Your email service's SMTP server.
        openai.api_key: Your OpenAI API key.

Running the Application

    Run the script:

    The GUI will open, and you can process emails by clicking the "Read and Process Emails" button.

    The system is programed to delete emails after processing. 

Security Notice

    Do not share sensitive information like passwords or API keys. Use environment variables or secure key management for production deployments.
    This script uses placeholders for demonstration purposes. Ensure your credentials are secure.

Dependencies

    imaplib: For connecting to and reading from the IMAP server.
    email: For parsing email content.
    openai: For interacting with OpenAI's API.
    smtplib: For sending email responses.
    tkinter: For creating the GUI.

License

This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgments

    OpenAI for providing the GPT model used for spam detection and email responses.
    Tkinter for the GUI framework.
