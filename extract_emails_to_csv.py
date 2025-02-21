import mailbox
import csv
import re
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime
from quopri import decodestring

# Version 2.3: Generalized for any business, standardized date format (DD/MM/YYYY), removed duplicates, cleaned email field

def decode_header_value(header):
    """Decodes a header value into a string."""
    if not header:
        return ""
    decoded_parts = decode_header(header)
    return "".join(
        [
            part.decode(charset or "utf-8", errors="replace") if isinstance(part, bytes) else part
            for part, charset in decoded_parts
        ]
    )

def decode_payload(message):
    """Extract and decode the email payload, handling multipart messages."""
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="replace")
    else:
        payload = message.get_payload(decode=True)
        if payload:
            charset = message.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="replace")
    return ""

def extract_customer_data(mbox_file, csv_file, contact_form_subjects):
    data = []
    unique_entries = set()

    # Open the MBOX file
    mbox = mailbox.mbox(mbox_file)

    for message in mbox:
        try:
            # Decode and extract the subject
            subject = decode_header_value(message["subject"]).strip()
            if not subject:
                print("Skipping message: Missing subject")
                continue  # Skip if subject is missing

            # Decode and extract the reply-to email
            reply_to_email = parseaddr(decode_header_value(message.get("reply-to")))[1]
            if not reply_to_email:
                reply_to_email = "Unknown Email"  # Default value if reply-to is missing

            # Remove mailto: and any other extraneous characters from email
            reply_to_email = re.sub(r"^(mailto:|<|>)", "", reply_to_email).strip()

            # Extract and decode the email body
            email_body = decode_payload(message)
            if not email_body:
                print("Skipping message: Empty email body")
                continue

            # Parse Interac e-Transfer emails
            interac_match = re.search(
                r"(?:sent you \$([0-9,]+\.\d{2}) .+? has been automatically deposited|\$([0-9,]+\.\d{2}) from ([\w\s]+))",
                email_body, re.IGNORECASE
            )
            
            if interac_match:
                amount = interac_match.group(1) or interac_match.group(2) or "0.00"
                customer_name = interac_match.group(3) or "Unknown Name"
                amount = amount.replace(',', '')  # Remove commas from numbers
                customer_name = re.sub(r"\s+and it has been automatically deposited$", "", customer_name.strip())

                # Extract date from email body
                date_match = re.search(
                    r"(?:sent you \$[0-9,]+\.\d{2} .+? on (\w+ \d{1,2}, \d{4}))|\b(\w+ \d{1,2}, \d{4})\b",
                    email_body
                )
                date_str = date_match.group(1) or date_match.group(2) if date_match else "Unknown Date"
                date_str = re.match(r"\w+ \d{1,2}, \d{4}", date_str).group(0) if re.match(r"\w+ \d{1,2}, \d{4}", date_str) else "Unknown Date"
            
            # Parse generic website contact form submissions
            elif any(form_subject in subject for form_subject in contact_form_subjects):
                name_match = re.search(r"First Name: (.+)", email_body)
                email_match = re.search(r"Email: (.+)", email_body)
                phone_match = re.search(r"Phone: (.+)", email_body)
                date_match = re.search(r"Event Date: (.+)", email_body)
                
                customer_name = name_match.group(1).strip() if name_match else "Unknown Name"
                reply_to_email = email_match.group(1).strip() if email_match else "Unknown Email"
                phone_number = phone_match.group(1).strip() if phone_match else "Unknown Phone"
                date_str = date_match.group(1).strip() if date_match else "Unknown Date"
                amount = "0.00"  # Contact forms do not contain dollar amounts
            
            else:
                print(f"Skipping message: Subject does not match pattern - {subject}")
                continue

            # Convert date string to a consistent format (DD/MM/YYYY)
            try:
                date = datetime.strptime(date_str, "%B %d, %Y").strftime("%d/%m/%Y")
            except ValueError:
                date = date_str  # If date parsing fails, keep the original string

            # Create unique entry key
            entry_key = (customer_name, reply_to_email, date, amount)
            if entry_key in unique_entries:
                continue  # Skip duplicates
            unique_entries.add(entry_key)

            # Append data to the list
            data.append(
                {
                    "Date": date,
                    "Customer Name": customer_name,
                    "Customer Email": reply_to_email,
                    "Amount Received": amount,
                }
            )

        except Exception as e:
            print(f"Error processing message: {e}")

    # Write data to CSV
    if data:
        with open(csv_file, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Date", "Customer Name", "Customer Email", "Amount Received"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully extracted to {csv_file}")
    else:
        print("No valid data was found in the MBOX file.")

def main():
    # Path to the MBOX file
    mbox_file = "path_to_your_mbox_file.mbox"  # Replace with the actual MBOX file path

    # Path to the output CSV file
    csv_file = "customers_for_quickbooks.csv"

    # Define general contact form subjects (replace with relevant ones for your business)
    contact_form_subjects = [
        "[Business Name] Contacts Form - new submission",
        "[Your Website] Contact Form Submission"
    ]

    # Extract data and write to CSV
    extract_customer_data(mbox_file, csv_file, contact_form_subjects)

if __name__ == "__main__":
    main()
