#!/usr/bin/env python3
"""
YouTube Authentication Script
Run this first to authenticate and generate token.json before using the MCP server
"""

from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# YouTube API scopes
# SCOPES = [
#     "https://www.googleapis.com/auth/contacts",  # 	See, edit, download, and permanently delete your contacts
#     "https://www.googleapis.com/auth/contacts.other.readonly",  # 	See and download contact info automatically saved in your "Other contacts"
#     "https://www.googleapis.com/auth/contacts.readonly",  # 	See and download your contacts
#     "https://www.googleapis.com/auth/directory.readonly",  # 	See and download your organization's Google Workspace directory
#     "https://www.googleapis.com/auth/user.addresses.read",  # 	View your street addresses
#     "https://www.googleapis.com/auth/user.birthday.read",  # 	See and download your exact date of birth
#     "https://www.googleapis.com/auth/user.emails.read",  # 	See and download all of your Google Account email addresses
#     "https://www.googleapis.com/auth/user.gender.read",  # 	See your gender
#     "https://www.googleapis.com/auth/user.organization.read",  # 	See your education, work history and org info
#     "https://www.googleapis.com/auth/user.phonenumbers.read",  # 	See and download your personal phone numbers
#     "https://www.googleapis.com/auth/userinfo.email",  # 	See your primary Google Account email address
#     "https://www.googleapis.com/auth/userinfo.profile",  # 	See your personal info, including any personal info you've made publicly available
# ]
# Use minimal scopes
SCOPES = [
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",  # Add this to prevent warning
]


def authenticate():
    """Authenticate with YouTube API"""
    token_path = Path("token.json")
    secret_path = Path("secret.json")

    if not secret_path.exists():
        print("❌ Error: secret.json not found!")
        print("Please ensure your OAuth credentials file is in the current directory.")
        return False

    creds = None

    # Check if we already have valid credentials
    if token_path.exists():
        print("📄 Found existing token.json")
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            try:
                creds.refresh(Request())
                print("✅ Token refreshed successfully!")
            except Exception as e:
                print(f"❌ Failed to refresh token: {e}")
                print("🔐 Starting new authentication flow...")
                creds = None

        if not creds:
            print("🔐 Starting OAuth authentication...")
            print("📱 A browser window will open for you to authenticate.")
            print(
                "   Please log in with your Google account and grant YouTube permissions."
            )

            flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
            creds = flow.run_local_server(port=8889)
            print("✅ Authentication successful!")

        # Save the credentials for future use
        with open(token_path, "w") as token:
            token.write(creds.to_json())
        print(f"💾 Credentials saved to {token_path}")
    else:
        print("✅ Valid credentials already exist!")

    print("\n🎉 Authentication complete!")
    print("You can now use the YouTube MCP server with your MCP client.")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("YouTube MCP Server - Authentication")
    print("=" * 60)
    print()

    success = authenticate()

    if not success:
        exit(1)
