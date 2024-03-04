import imaplib
import webbrowser
import re

def login_to_email(email, password):
    # Email credentials
    email_user = email
    email_pass = password

    # Email server settings (IMAP)
    imap_server = 'imap.outlook.com'  # Change based on the email provider
    port = 993  # IMAP port

    try:
        # Establish connection
        mail = imaplib.IMAP4_SSL(imap_server, port)

        # Login to email
        mail.login(email_user, email_pass)
        print("Login successful!")

        # Select the desired inbox
        mail.select('INBOX')

        # Search for emails from a specific email address
        search_criteria = '(FROM "<noreply@truthsocial.com>")'
        typ, data = mail.search(None, search_criteria)

        # Get the email IDs
        email_ids = data[0].split()

        # Open the first email
        if email_ids:
            email_id = email_ids[0]
            typ, data = mail.fetch(email_id, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = imaplib.IMAP4.parse_id(response_part[1])
                    for part in msg.walk():
                        if part.get_content_type() == 'text/html':
                            body = part.get_payload(decode=True).decode('utf-8')
                            # Extract links from the email body
                            links = re.findall(r'href="(https?://[^"]+)"', body)

                            # Find and open the link related to 'Confirm Your Email' button
                            for link in links:
                                if 'confirm' in link.lower() and 'email' in link.lower():
                                    webbrowser.open(link)
                                    break
        else:
            print("No emails found from the specified sender.")
    except Exception as e:
        print(f"Login failed. Error: {e}")

# Read email credentials from a text file
def read_email_credentials(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            email = lines[0].strip()
            password = lines[1].strip()
            return email, password
    except FileNotFoundError:
        print("File not found.")
        return None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

# Main function
if __name__ == "__main__":
    file_path = 'email_credentials.txt'  # Replace with your file path
    email, password = read_email_credentials(file_path)
    if email and password:
        login_to_email(email, password)
