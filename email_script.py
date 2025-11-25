import smtplib
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD") 

# Email subject
SUBJECT = "ASU x {company}"

# GitHub signature image URLs
SIGNATURE_IMAGE_URL = "https://raw.githubusercontent.com/Jalqur/soda_assets/main/new_soda_logo.png"

# Attachment
ATTACHMENT_PATH = "SoDA_Sponsorship_Package.pdf" 

def create_html_email(first_name: str, company: str) -> str:
    html = f"""
    <html>
      <body>
        <p>Dear {first_name},</p>

        <p>My name is Yahia Alqurnawi, and I'm an Industry Relations Officer for the Software Developers Association (SoDA) at Arizona State University.</p>
        <p>SoDA is one of the largest and most active computer science organizations on campus. We host weekly events that bring together students passionate about software development, ranging from hands-on technical workshops to industry-led sessions. Past partners include companies like Amazon, Goldman Sachs, State Farm, and PayPal.</p>
        <p>We'd love to welcome your team from <strong>{company}</strong> to one of our Tuesday sessions this semester, which begin at 7:30 in the evening and typically run for about an hour. These sessions offer a great opportunity to connect with ASU's top software talent.</p>
        <p>I've attached our sponsorship packet for 2025–2026, which outlines opportunities to support and collaborate with SoDA throughout the year.</p>
        <p>If this sounds like a good fit, we'd be happy to coordinate further or answer any questions. We'd also be glad to schedule a Zoom meeting to discuss things in more detail if that's preferred.</p>

        <br/>
        <p>Warm regards,</p>
        <p>Yahia Alqurnawi<br>
        Officer, Industry Relations<br>
        The Software Developers Association at ASU<br>
        <img src="{SIGNATURE_IMAGE_URL}" alt="Signature Image" style="height:25px;"><br>
        <a href="mailto:asu@thesoda.io">Email</a> | <a href="https://www.linkedin.com/in/yahia-alqurnawi/">LinkedIn</a>
        </p>
      </body>
    </html>
    """
    return html

def extract_first_name(full_name: str) -> str:
    return full_name.strip().split()[0] if full_name.strip() else ""

def read_recipients_from_csv(csv_file_path: str) -> List[Dict[str, str]]:
    recipients = []

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                if 'Name' in row and 'Company' in row and 'Email Address' in row:
                    recipients.append({
                        'name': row['Name'],
                        'company': row['Company'],
                        'email': row['Email Address']
                    })
                else:
                    print(f"Warning: CSV must have 'Name', 'Company', and 'Email Address' columns")
                    break

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")

    return recipients

def send_email(recipient_email: str, recipient_name: str, company: str) -> bool:
    try:
        # Extract first name
        first_name = extract_first_name(recipient_name)

        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = SUBJECT.format(company=company)
        message["From"] = f"ASU SoDA <{SENDER_EMAIL}>"
        message["To"] = recipient_email

        # Create HTML email body
        html_body = create_html_email(first_name, company)
        html_part = MIMEText(html_body, "html")
        message.attach(html_part)

        # Attach PDF file
        if os.path.exists(ATTACHMENT_PATH):
            with open(ATTACHMENT_PATH, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(ATTACHMENT_PATH)}",
                )
                message.attach(part)
        else:
            print(f"Warning: Attachment file '{ATTACHMENT_PATH}' not found. Sending email without attachment.")

        # Connect to Gmail SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS encryption
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)

        print(f" Email sent successfully to {recipient_name} ({recipient_email})")
        return True

    except Exception as e:
        print(f" Failed to send email to {recipient_name} ({recipient_email}): {str(e)}")
        return False

def send_bulk_emails(csv_file_path: str):
    # Validate configuration
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Error: Please configure SENDER_EMAIL and SENDER_PASSWORD in the script")
        return

    if not ATTACHMENT_PATH:
        print("Error: Please configure ATTACHMENT_PATH in the script")
        return

    # Read recipients
    recipients = read_recipients_from_csv(csv_file_path)

    if not recipients:
        print("No recipients found in CSV file")
        return

    print(f"\nPreparing to send {len(recipients)} emails...\n")

    # Send emails
    successful = 0
    failed = 0

    for recipient in recipients:
        if send_email(recipient['email'], recipient['name'], recipient['company']):
            successful += 1
        else:
            failed += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"Email Campaign Summary:")
    print(f"{'='*50}")
    print(f"Total: {len(recipients)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    # Path to your CSV file
    CSV_FILE = "test.csv"  # Change this to your CSV file path

    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file '{CSV_FILE}' not found")
        print("\nPlease create a CSV file with the following format:")
        print("name,email")
        print("John Doe,john.doe@example.com")
        print("Jane Smith,jane.smith@example.com")
    else:
        send_bulk_emails(CSV_FILE)
