Email Extraction Script for QuickBooks Upload
"Whatever you do, work at it with all your heart, as working for the Lord, not for human masters." – Colossians 3:23

Overview
This script extracts customer data from an MBOX email file, processing Interac e-Transfer notifications and contact form submissions into a structured CSV file for QuickBooks import. It ensures clean data, removes duplicates, and formats dates consistently.

"But seek first the kingdom of God and His righteousness, and all these things will be added to you." – Matthew 6:33

Features
Parses Interac e-Transfer notifications to extract:
Customer Name
Email
Date of Transfer
Amount Received
Extracts contact form submissions from generic business contact forms, supporting:
"[Business Name] Contacts Form - new submission"
"[Your Website] Contact Form Submission"
Removes duplicate entries to ensure unique customer data.
Standardizes dates to the format DD/MM/YYYY.
Cleans up email formatting to remove unnecessary text.
"For every house is built by someone, but the builder of all things is God." – Hebrews 3:4

Installation
Prerequisites
Ensure you have Python 3 installed on your system.

Clone the Repository

bash
Copy
Edit
git clone https://github.com/yourusername/email-extraction.git
cd email-extraction
Run the Script

bash
Copy
Edit
python3 extract_emails_to_csv.py
Locate Output File
After running the script, a customers_for_quickbooks.csv file will be generated in the project directory.

"Commit your work to the Lord, and your plans will be established." – Proverbs 16:3

Configuration
Modify mbox_file path in extract_emails_to_csv.py to point to your MBOX file:

python
Copy
Edit
mbox_file = "path_to_your_mbox_file.mbox"
Customize the contact form subjects for your business by modifying:

python
Copy
Edit
contact_form_subjects = [
    "[Your Business Name] Contacts Form - new submission",
    "[Your Website] Contact Form Submission"
]
"Let the favor of the Lord our God be upon us, and establish the work of our hands upon us." – Psalm 90:17

Contributing
If you wish to improve this script, feel free to submit a pull request. May the work of your hands be blessed!

"Do not store up for yourselves treasures on earth, where moths and rust destroy, and where thieves break in and steal. But store up for yourselves treasures in heaven." – Matthew 6:19-20

License
This project is licensed under the MIT License.
"Freely you have received; freely give." – Matthew 10:8

Acknowledgments
This project is dedicated to God Almighty, who gives wisdom, strength, and purpose.

"In all your ways acknowledge Him, and He will make straight your paths." – Proverbs 3:6
