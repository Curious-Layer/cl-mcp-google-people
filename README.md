# Google People MCP Server

This project is a server that lets you manage your Google Contacts using simple commands. MCP stands for "Model Context Protocol," which is a special kind of server that makes it easy to interact with APIs like the Google People API.

## What it does

This server provides a set of "tools" that you can use to do things like:
*   Create, read, update, and delete your contacts.
*   Organize contacts into groups.
*   Search for contacts.
*   Manage "Other Contacts" that Google has automatically saved.

## Setup

### 1. Install the requirements
First, you need to install the necessary libraries. You can do this by running the following command in your terminal:
```bash
pip install -r requirements.txt
```

### 2. Authentication
To use this server, you need to give it permission to access your Google Account. This is done using a special token. The server expects this token to be provided when you use a tool that requires it.

## How to run the server
You can start the server by running the following command in your terminal:
```bash
python server.py
```
You can also specify the transport, host, and port if needed.

## Available Tools

Here are the tools you can use with this server:

### Contacts
These tools help you manage your individual contacts.

*   **`get_person`**: Gets information about a specific person in your contacts.
*   **`list_connections`**: Lists all of your contacts.
*   **`create_contact`**: Creates a new contact.
*   **`update_contact`**: Updates an existing contact's information.
*   **`delete_contact`**: Deletes a contact.
*   **`search_contacts`**: Searches for contacts that match a query.

### Contact Groups
These tools are for organizing your contacts into groups.

*   **`list_contact_groups`**: Lists all of your contact groups.
*   **`get_contact_group`**: Gets information about a specific contact group.
*   **`create_contact_group`**: Creates a new contact group.
*   **`update_contact_group`**: Updates an existing contact group.
*   **`delete_contact_group`**: Deletes a contact group.
*   **`batch_get_contact_groups`**: Gets information about multiple contact groups at once.

### Other Contacts
"Other contacts" are people you've interacted with on Google services that are saved automatically. These tools help you manage them.

*   **`list_other_contacts`**: Lists all of your "Other contacts".
*   **`search_other_contacts`**: Searches through your "Other contacts".
*   **`copy_other_contact_to_my_contacts_group`**: Copies a contact from "Other contacts" to your main contacts list.
