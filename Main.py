import imaplib
import email
from email.header import decode_header
import openai
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Placeholders for sensitive information
EMAIL_ACCOUNT = "your_email@example.com"
PASSWORD = "your_password"  # Use your email password here
IMAP_SERVER = "imap.yourserver.com"
SMTP_SERVER = "smtp.yourserver.com"
SMTP_PORT = 465  # SMTP port for SSL
openai.api_key = "your_openai_api_key"

# Connect to IMAP server and read emails
def read_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select("inbox")
    status, messages = mail.search(None, "ALL")
    
    if status != "OK":
        print("No messages found!")
        return []

    email_ids = messages[0].split()
    emails = []

    for email_id in email_ids[-5:]:  # Read the 5 most recent emails
        try:
            email_id = email_id.decode()  # Ensure the email ID is a string
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                print(f"Failed to fetch email with ID {email_id}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    body = ""
                    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    if is_spam_ai(subject, from_, body):
                        delete_email(mail, email_id)
                    else:
                        ai_response = process_email_with_ai(subject, from_, body)
                        send_email_response(from_, subject, ai_response)  # Send the email response
                        emails.append((subject, from_, body, ai_response, date_time))
                        delete_email(mail, email_id)  # Delete the email after processing
        except Exception as e:
            print(f"Error processing email ID {email_id}: {e}")

    mail.logout()
    return emails

# AI-based spam detection
def is_spam_ai(subject, sender, body):
    messages = [
        {"role": "system", "content": "You are an AI that helps classify emails as spam or not."},
        {"role": "user", "content": f"Subject: {subject}\nFrom: {sender}\nBody: {body}\nIs this email spam? Please respond with 'Yes' or 'No'."}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=10
    )
    classification = response['choices'][0]['message']['content'].strip().lower()
    return classification == "yes"

# AI processing
def process_email_with_ai(subject, sender, body):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional email assistant. Respond politely and professionally to emails, "
                "acknowledge the sender's message, and express gratitude if appropriate. "
                "Avoid making any commitments or agreements in your response."
            )
        },
        {
            "role": "user",
            "content": f"Subject: {subject}\nFrom: {sender}\nBody: {body}\nGenerate a polite and neutral response."
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# Send an email response
def send_email_response(to_address, subject, body):
    msg = MIMEText(body)
    msg['From'] = EMAIL_ACCOUNT
    msg['To'] = to_address
    msg['Subject'] = f"Re: {subject}"

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ACCOUNT, PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully to {to_address}")
    except Exception as e:
        print(f"Failed to send email to {to_address}: {e}")

# Delete an email
def delete_email(mail, email_id):
    mail.store(email_id, '+FLAGS', '\\Deleted')
    mail.expunge()

# Function to create the GUI
def create_gui():
    # Set up the main window
    window = tk.Tk()
    window.title("Email Reader and AI Processor")
    window.geometry("900x700")
    window.configure(bg="#f0f0f0")

    # Frame for the TreeView
    frame = tk.Frame(window, bg="#f0f0f0")
    frame.pack(pady=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("Subject", "From", "Date/Time"), show="headings", height=15)
    tree.heading("Subject", text="Subject")
    tree.heading("From", text="From")
    tree.heading("Date/Time", text="Date/Time")
    tree.column("Subject", width=300)
    tree.column("From", width=200)
    tree.column("Date/Time", width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    # Details box
    details_label = tk.Label(window, text="Email Details and AI Response:", bg="#f0f0f0", font=("Helvetica", 12))
    details_label.pack(pady=5)
    details = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=15)
    details.pack(fill=tk.BOTH, expand=True, padx=10)

    def show_email_details(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            subject, sender, date_time = item["values"]
            # Display the email details
            details.delete(1.0, tk.END)
            details.insert(tk.END, f"Subject: {subject}\nFrom: {sender}\nDate/Time: {date_time}\n\nAI Response:\n")

    def process_emails():
        try:
            emails = read_emails()
            for subject, sender, body, ai_response, date_time in emails:
                tree.insert("", tk.END, values=(subject, sender, date_time))
                details.insert(tk.END, f"{ai_response}\n\n")
            messagebox.showinfo("Success", "Emails have been processed and responses sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Button to process emails
    process_button = tk.Button(window, text="Read and Process Emails", command=process_emails, bg="#4CAF50", fg="white", font=("Helvetica", 10))
    process_button.pack(pady=10)

    window.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
