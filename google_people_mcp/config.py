import logging

SCOPES = [
    "https://www.googleapis.com/auth/contacts",  # 	See, edit, download, and permanently delete your contacts
    "https://www.googleapis.com/auth/contacts.other.readonly",  # 	See and download contact info automatically saved in your "Other contacts"
    "https://www.googleapis.com/auth/contacts.readonly",  # 	See and download your contacts
    "https://www.googleapis.com/auth/directory.readonly",  # 	See and download your organization's Google Workspace directory
    "https://www.googleapis.com/auth/user.addresses.read",  # 	View your street addresses
    "https://www.googleapis.com/auth/user.birthday.read",  # 	See and download your exact date of birth
    "https://www.googleapis.com/auth/user.emails.read",  # 	See and download all of your Google Account email addresses
    "https://www.googleapis.com/auth/user.gender.read",  # 	See your gender
    "https://www.googleapis.com/auth/user.organization.read",  # 	See your education, work history and org info
    "https://www.googleapis.com/auth/user.phonenumbers.read",  # 	See and download your personal phone numbers
    "https://www.googleapis.com/auth/userinfo.email",  # 	See your primary Google Account email address
    "https://www.googleapis.com/auth/userinfo.profile",  # 	See your personal info, including any personal info you've made publicly available
]


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
