#!/usr/bin/env python3
"""
MCP Server for Google People API
Provides access to Google People operations through Model Context Protocol

Documentation referred : https://googleapis.github.io/google-api-python-client/docs/dyn/people_v1.html
"""

import json
import logging
import argparse
from typing import Dict

from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Google People API scopes
# https://developers.google.com/identity/protocols/oauth2/scopes#people
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("google-contacts-mcp-server")

# Create FastMCP instance
mcp = FastMCP("CL Google People MCP Server")

# Global service instance
_service = None


def _get_token_data(token_data: str) -> Dict:
    """Decode access token JSON string to dictionary"""
    try:
        token_data = json.loads(token_data)
        auth_data = {
            "token": token_data.get("token"),
            "refresh_token": token_data.get("refresh_token"),
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": token_data.get("client_id"),
            "client_secret": token_data.get("client_secret"),
            "scopes": token_data.get("scopes"),
        }
        return auth_data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode access token: {e}")
        return {}


def _get_service(token_data: str):
    """Create Google People service with provided access token"""
    auth_data = _get_token_data(token_data)
    logger.info("Creating Google People API service with provided access token")
    creds = Credentials(**auth_data)
    service = build("people", "v1", credentials=creds)
    logger.info("Google People API service created successfully")
    return service


# =======================================================================================
#                       MCP TOOLS START
# =======================================================================================


@mcp.tool(
    name="get_person",
    description="Get a person from Google Contacts",
)
def get_person(token_data: str, resource_name: str, person_fields: str) -> str:
    """
    Gets a person from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the person to retrieve, e.g., "people/me".
    :param person_fields: A comma-separated list of fields to retrieve, e.g., "names,emailAddresses".
    :return: A JSON string of the person.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.people()
            .get(resourceName=resource_name, personFields=person_fields)
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get person '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="list_connections",
    description="List connections from Google Contacts",
)
def list_connections(
    token_data: str,
    resource_name: str,
    person_fields: str,
    page_size: int = None,
    page_token: str = None,
) -> str:
    """
    Lists connections from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the person to retrieve connections for, e.g., "people/me".
    :param person_fields: A comma-separated list of fields to retrieve, e.g., "names,emailAddresses".
    :param page_size: The maximum number of connections to return.
    :param page_token: The page token from a previous list request.
    :return: A JSON string of the connections.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.people()
            .connections()
            .list(
                resourceName=resource_name,
                personFields=person_fields,
                pageSize=page_size,
                pageToken=page_token,
            )
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list connections for '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="create_contact",
    description="Create a contact in Google Contacts",
)
def create_contact(token_data: str, person: str) -> str:
    """
    Creates a contact in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param person: A JSON string representing the person to create.
    :return: A JSON string of the created person.
    """
    try:
        service = _get_service(token_data)
        person_dict = json.loads(person)
        response = service.people().createContact(body=person_dict).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create contact: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="update_contact",
    description="Update a contact in Google Contacts",
)
def update_contact(
    token_data: str, resource_name: str, update_person_fields: str, person: str
) -> str:
    """
    Updates a contact in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the person to update.
    :param update_person_fields: A comma-separated list of fields to update.
    :param person: A JSON string representing the updated person.
    :return: A JSON string of the updated person.
    """
    try:
        service = _get_service(token_data)
        person_dict = json.loads(person)
        response = (
            service.people()
            .updateContact(
                resourceName=resource_name,
                updatePersonFields=update_person_fields,
                body=person_dict,
            )
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to update contact '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="delete_contact",
    description="Delete a contact from Google Contacts",
)
def delete_contact(token_data: str, resource_name: str) -> str:
    """
    Deletes a contact from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the person to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.people().deleteContact(resourceName=resource_name).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete contact '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="search_contacts",
    description="Search for contacts in Google Contacts",
)
def search_contacts(token_data: str, query: str, read_mask: str) -> str:
    """
    Searches for contacts in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param query: The query to search for.
    :param read_mask: A comma-separated list of fields to retrieve, e.g., "names,emailAddresses".
    :return: A JSON string of the search results.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.people().searchContacts(query=query, readMask=read_mask).execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to search contacts with query '{query}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="list_contact_groups",
    description="List contact groups in Google Contacts",
)
def list_contact_groups(
    token_data: str, page_size: int = None, page_token: str = None
) -> str:
    """
    Lists contact groups in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param page_size: The maximum number of contact groups to return.
    :param page_token: The page token from a previous list request.
    :return: A JSON string of the contact groups.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.contactGroups()
            .list(pageSize=page_size, pageToken=page_token)
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list contact groups: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="get_contact_group",
    description="Get a contact group from Google Contacts",
)
def get_contact_group(token_data: str, resource_name: str) -> str:
    """
    Gets a contact group from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the contact group to retrieve.
    :return: A JSON string of the contact group.
    """
    try:
        service = _get_service(token_data)
        response = service.contactGroups().get(resourceName=resource_name).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get contact group '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="create_contact_group",
    description="Create a contact group in Google Contacts",
)
def create_contact_group(token_data: str, contact_group: str) -> str:
    """
    Creates a contact group in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param contact_group: A JSON string representing the contact group to create.
    :return: A JSON string of the created contact group.
    """
    try:
        service = _get_service(token_data)
        contact_group_dict = json.loads(contact_group)
        response = service.contactGroups().create(body=contact_group_dict).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create contact group: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="update_contact_group",
    description="Update a contact group in Google Contacts",
)
def update_contact_group(
    token_data: str, resource_name: str, contact_group: str
) -> str:
    """
    Updates a contact group in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the contact group to update.
    :param contact_group: A JSON string representing the updated contact group.
    :return: A JSON string of the updated contact group.
    """
    try:
        service = _get_service(token_data)
        contact_group_dict = json.loads(contact_group)
        response = (
            service.contactGroups()
            .update(resourceName=resource_name, body=contact_group_dict)
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to update contact group '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="delete_contact_group",
    description="Delete a contact group from Google Contacts",
)
def delete_contact_group(token_data: str, resource_name: str) -> str:
    """
    Deletes a contact group from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the contact group to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.contactGroups().delete(resourceName=resource_name).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete contact group '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="batch_get_contact_groups",
    description="Get multiple contact groups from Google Contacts",
)
def batch_get_contact_groups(token_data: str, resource_names: str) -> str:
    """
    Gets multiple contact groups from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_names: A comma-separated list of resource names of the contact groups to retrieve.
    :return: A JSON string of the contact groups.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.contactGroups()
            .batchGet(resourceNames=resource_names.split(","))
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to batch get contact groups: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="list_other_contacts",
    description="List other contacts in Google Contacts",
)
def list_other_contacts(
    token_data: str, read_mask: str, page_size: int = None, page_token: str = None
) -> str:
    """
    Lists other contacts in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param read_mask: A comma-separated list of fields to retrieve, e.g., "names,emailAddresses".
    :param page_size: The maximum number of other contacts to return.
    :param page_token: The page token from a previous list request.
    :return: A JSON string of the other contacts.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.otherContacts()
            .list(
                readMask=read_mask,
                pageSize=page_size,
                pageToken=page_token,
            )
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list other contacts: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="search_other_contacts",
    description="Search other contacts in Google Contacts",
)
def search_other_contacts(token_data: str, query: str, read_mask: str) -> str:
    """
    Searches other contacts in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param query: The query to search for.
    :param read_mask: A comma-separated list of fields to retrieve, e.g., "names,emailAddresses".
    :return: A JSON string of the search results.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.otherContacts().search(query=query, readMask=read_mask).execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to search other contacts with query '{query}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="copy_other_contact_to_my_contacts_group",
    description="Copy an other contact to my contacts group in Google Contacts",
)
def copy_other_contact_to_my_contacts_group(
    token_data: str, resource_name: str, copy_mask: str
) -> str:
    """
    Copies an other contact to my contacts group in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the other contact to copy.
    :param copy_mask: A comma-separated list of fields to copy.
    :return: A JSON string of the copied person.
    """
    try:
        service = _get_service(token_data)
        response = (
            service.otherContacts()
            .copyOtherContactToMyContactsGroup(
                resourceName=resource_name,
                body={"copyMask": copy_mask},
            )
            .execute()
        )
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to copy other contact '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


# =======================================================================================
#                       MCP TOOLS END
# =======================================================================================


# Function for parsing the cmd-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Google People MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        help="Transport method for MCP (Allowed Values: 'stdio', 'sse', or 'streamable-http')",
        default=None,
    )
    parser.add_argument("--host", help="Host to bind the server to", default=None)
    parser.add_argument(
        "--port", type=int, help="Port to bind the server to", default=None
    )
    return parser.parse_args()


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Google People MCP Server Starting")
    logger.info("=" * 60)

    args = parse_args()

    # Build kwargs for mcp.run() only with provided values
    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
        logger.info(f"Transport: {args.transport}")
    if args.host:
        run_kwargs["host"] = args.host
        logger.info(f"Host: {args.host}")
    if args.port:
        run_kwargs["port"] = args.port
        logger.info(f"Port: {args.port}")

    try:
        # Start the MCP server with optional transport/host/port
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}", exc_info=True)
        raise
