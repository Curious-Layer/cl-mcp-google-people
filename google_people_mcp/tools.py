import json
import logging

from fastmcp import FastMCP

from .schemas import JsonStringToolResponse, OAuthTokenData
from .service import get_service

logger = logging.getLogger("google-contacts-mcp-server")

class _ToolCollector:
    def __init__(self):
        self.items = []

    def tool(self, *args, **kwargs):
        def decorator(func):
            self.items.append((args, kwargs, func))
            return func

        return decorator


mcp = _ToolCollector()


def register_tools(real_mcp: FastMCP) -> None:
    for args, kwargs, func in mcp.items:
        real_mcp.tool(*args, **kwargs)(func)


#                       MCP TOOLS START


@mcp.tool(
    name="get_person",
    description="Get a person from Google Contacts",
)
def get_person(oauth_token: OAuthTokenData, resource_name: str, person_fields: str) -> JsonStringToolResponse:
    """
    Gets a person from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the person to retrieve, e.g., "people/me".
    :param person_fields: A comma-separated list of fields to retrieve, e.g., "names,emailAddresses".
    :return: A JSON string of the person.
    """
    try:
        service = get_service(oauth_token)
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
    oauth_token: OAuthTokenData,
    resource_name: str,
    person_fields: str,
    page_size: int = None,
    page_token: str = None,
) -> JsonStringToolResponse:
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
        service = get_service(oauth_token)
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
def create_contact(oauth_token: OAuthTokenData, person: str) -> JsonStringToolResponse:
    """
    Creates a contact in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param person: A JSON string representing the person to create.
    :return: A JSON string of the created person.
    """
    try:
        service = get_service(oauth_token)
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
    oauth_token: OAuthTokenData, resource_name: str, update_person_fields: str, person: str
) -> JsonStringToolResponse:
    """
    Updates a contact in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the person to update.
    :param update_person_fields: A comma-separated list of fields to update.
    :param person: A JSON string representing the updated person.
    :return: A JSON string of the updated person.
    """
    try:
        service = get_service(oauth_token)
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
def delete_contact(oauth_token: OAuthTokenData, resource_name: str) -> JsonStringToolResponse:
    """
    Deletes a contact from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the person to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service(oauth_token)
        response = service.people().deleteContact(resourceName=resource_name).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete contact '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="search_contacts",
    description="Search for contacts in Google Contacts",
)
def search_contacts(oauth_token: OAuthTokenData, query: str, read_mask: str) -> JsonStringToolResponse:
    """
    Searches for contacts in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param query: The query to search for.
    :param read_mask: A comma-separated list of fields to retrieve, e.g., "names,emailAddresses".
    :return: A JSON string of the search results.
    """
    try:
        service = get_service(oauth_token)
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
    oauth_token: OAuthTokenData, page_size: int = None, page_token: str = None
) -> JsonStringToolResponse:
    """
    Lists contact groups in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param page_size: The maximum number of contact groups to return.
    :param page_token: The page token from a previous list request.
    :return: A JSON string of the contact groups.
    """
    try:
        service = get_service(oauth_token)
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
def get_contact_group(oauth_token: OAuthTokenData, resource_name: str) -> JsonStringToolResponse:
    """
    Gets a contact group from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the contact group to retrieve.
    :return: A JSON string of the contact group.
    """
    try:
        service = get_service(oauth_token)
        response = service.contactGroups().get(resourceName=resource_name).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get contact group '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="create_contact_group",
    description="Create a contact group in Google Contacts",
)
def create_contact_group(oauth_token: OAuthTokenData, contact_group: str) -> JsonStringToolResponse:
    """
    Creates a contact group in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param contact_group: A JSON string representing the contact group to create.
    :return: A JSON string of the created contact group.
    """
    try:
        service = get_service(oauth_token)
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
    oauth_token: OAuthTokenData, resource_name: str, contact_group: str
) -> JsonStringToolResponse:
    """
    Updates a contact group in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the contact group to update.
    :param contact_group: A JSON string representing the updated contact group.
    :return: A JSON string of the updated contact group.
    """
    try:
        service = get_service(oauth_token)
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
def delete_contact_group(oauth_token: OAuthTokenData, resource_name: str) -> JsonStringToolResponse:
    """
    Deletes a contact group from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the contact group to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service(oauth_token)
        response = service.contactGroups().delete(resourceName=resource_name).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete contact group '{resource_name}': {e}")
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="batch_get_contact_groups",
    description="Get multiple contact groups from Google Contacts",
)
def batch_get_contact_groups(oauth_token: OAuthTokenData, resource_names: str) -> JsonStringToolResponse:
    """
    Gets multiple contact groups from Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_names: A comma-separated list of resource names of the contact groups to retrieve.
    :return: A JSON string of the contact groups.
    """
    try:
        service = get_service(oauth_token)
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
    oauth_token: OAuthTokenData, read_mask: str, page_size: int = None, page_token: str = None
) -> JsonStringToolResponse:
    """
    Lists other contacts in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param read_mask: A comma-separated list of fields to retrieve, e.g., "names,emailAddresses".
    :param page_size: The maximum number of other contacts to return.
    :param page_token: The page token from a previous list request.
    :return: A JSON string of the other contacts.
    """
    try:
        service = get_service(oauth_token)
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
def search_other_contacts(oauth_token: OAuthTokenData, query: str, read_mask: str) -> JsonStringToolResponse:
    """
    Searches other contacts in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param query: The query to search for.
    :param read_mask: A comma-separated list of fields to retrieve, e.g., "names,emailAddresses".
    :return: A JSON string of the search results.
    """
    try:
        service = get_service(oauth_token)
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
    oauth_token: OAuthTokenData, resource_name: str, copy_mask: str
) -> JsonStringToolResponse:
    """
    Copies an other contact to my contacts group in Google Contacts.

    :param token_data: The JSON string of the user's access token.
    :param resource_name: The resource name of the other contact to copy.
    :param copy_mask: A comma-separated list of fields to copy.
    :return: A JSON string of the copied person.
    """
    try:
        service = get_service(oauth_token)
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
