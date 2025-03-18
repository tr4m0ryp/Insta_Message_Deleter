# Insta_Message_Deleter
A Tool that allows you to bulk delete/unsend instagram message
Below is a sample README file that explains the script's functionality and usage:

## Overview

This Python script uses the [`instagrapi`](https://github.com/adw0rd/instagrapi) library to automatically delete your own messages from Instagram Direct Message (DM) threads. It supports secure login with 2FA and challenge resolution, pagination for retrieving messages, multiple deletion methods, and configurable speed settings to manage deletion pace and reduce the risk of rate limiting.

## Features

- **Secure Login**  
  - Utilizes a saved session file (`instagram_session.json`) for quick login.
  - Supports 2FA and Instagram's challenge verification process.
  
- **Message Retrieval**  
  - Automatically fetches up to 1000 messages per thread using pagination.
  - Filters messages to identify and delete only your own.

- **Message Deletion**  
  - Attempts to delete messages using several methods to ensure compatibility with different versions of `instagrapi`.
  - Includes a test mode that allows you to verify deletion on a single message before processing all messages.

- **Speed Settings**  
  - Offers three speed options:
    - **Normal**: 2-5 seconds delay between deletions.
    - **Fast**: 0.5-2 seconds delay between deletions.
    - **Turbo**: 0.2-0.7 seconds delay (with a higher risk of rate limiting).

- **Progress Reporting**  
  - Displays a progress bar along with statistics like success rate, messages per minute, and estimated time remaining.

- **Batch Processing**  
  - Processes selected chats in batches and offers the option to rescan until all your messages are deleted.

## Prerequisites

- Python 3.7 or higher.
- The `instagrapi` library.

### Installation

Install the required library using pip:

```bash
pip install instagrapi
```

## Usage Instructions

1. **Download the Script**  
   Save the Python script (e.g., `instagram_dm_deleter.py`) to your local machine.

2. **Run the Script**  
   Execute the script using Python:

   ```bash
   python instagram_dm_deleter.py
   ```

3. **Login Process**  
   - When prompted, enter your Instagram username and password.
   - If a session file (`instagram_session.json`) exists, the script will use it to log in.
   - If Instagram requires additional verification (via email or SMS), follow the on-screen instructions to complete the 2FA process.

4. **Select Chats**  
   - The script retrieves your DM threads and displays them with chat numbers, participant usernames, and last activity timestamps.
   - Enter the chat numbers you wish to process. You can use individual numbers (e.g., `0,3`) or ranges (e.g., `2-4`).

5. **Configure Speed Settings**  
   - Choose one of the three speed settings:
     - **Normal (1)**: 2-5 seconds delay between each deletion.
     - **Fast (2)**: 0.5-2 seconds delay.
     - **Turbo (3)**: 0.2-0.7 seconds delay (higher risk of rate limiting).

6. **Test Mode**  
   - Optionally, run a test mode to delete a single message from the selected chat to ensure the deletion process works as expected.

7. **Message Deletion**  
   - The script scans each selected chat for your messages and attempts to delete them.
   - A progress bar with real-time statistics is displayed during the deletion process.
   - After each batch, a summary is shown with the total number of messages processed, successes, and any errors encountered.

8. **Repeat Until Completion**  
   - You can choose whether to continue rescanning the chats until all your messages have been deleted.

## Important Notes

- **Rate Limiting**:  
  Be cautious with the Turbo speed setting as aggressive deletion may trigger Instagram's rate limiting.

- **Session Security**:  
  The script saves your session settings in `instagram_session.json` to simplify future logins. Ensure this file is kept secure.

- **Backup**:  
  Always back up important data. This tool is intended to delete your own messages and should be used with care.

## Troubleshooting

- **Login Issues**:  
  - Verify your username and password.
  - Follow the challenge verification steps if prompted.

- **Deletion Errors**:  
  - The script tries multiple methods for deletion. If errors persist, check for updates to `instagrapi` or review the error messages for more details.

## Disclaimer

This script is provided "as is" without any warranty. Use it at your own risk. The author is not responsible for any data loss or account issues that may arise from using this tool.

## License

Specify your license here (e.g., MIT License).

---

Feel free to modify the README to suit your project’s needs or add any additional instructions relevant to your usage scenario.
