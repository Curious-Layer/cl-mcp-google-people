**Search, manage, and organize your Google Contacts with AI.**

A Model Context Protocol (MCP) server that exposes Google People API for reading, creating, updating, and deleting contacts and contact groups.


## Overview

The Google People MCP Server provides full Google Contacts management capabilities:

- Create, read, update, delete, and search personal contacts
- Manage contact groups — list, create, update, or delete them
- Access and promote "Other Contacts" auto-saved by Google services

Perfect for:

- Looking up contact details and email addresses via AI assistants
- Automating contact list maintenance and group organization
- Copying frequently-interacted contacts from "Other Contacts" into your main list


## Tools

<details>
<summary><code>get_person</code> — Get a person from Google Contacts</summary>

Fetches a contact by resource name, returning only the fields specified.

**Inputs:**
```
- `resource_name`  (string, required) — Resource name of the person (e.g. "people/me" or "people/c12345")
- `person_fields`  (string, required) — Comma-separated list of fields to return (e.g. "names,emailAddresses,phoneNumbers")
```

**Output:**

```json
{
  "resourceName": "people/c12345",
  "names": [{ "displayName": "Jane Doe" }],
  "emailAddresses": [{ "value": "jane@example.com" }]
}
```

</details>


<details>
<summary><code>list_connections</code> — List connections from Google Contacts</summary>

Returns a paginated list of the authenticated user's contacts.

**Inputs:**
```
- `resource_name`  (string,  required) — Resource name of the person to list connections for (use "people/me" for the authenticated user)
- `person_fields`  (string,  required) — Comma-separated list of fields to return (e.g. "names,emailAddresses")
- `page_size`      (integer, optional) — Maximum number of connections to return
- `page_token`     (string,  optional) — Page token from a previous list request for pagination
```

**Output:**

```json
{
  "connections": [{ "resourceName": "people/c12345", "names": [...] }],
  "nextPageToken": "...",
  "totalItems": 42
}
```

</details>


<details>
<summary><code>create_contact</code> — Create a contact in Google Contacts</summary>

Creates a new contact from a JSON person object.

**Inputs:**
```
- `person`  (string, required) — JSON string representing the person to create (e.g. '{"names":[{"givenName":"Jane","familyName":"Doe"}],"emailAddresses":[{"value":"jane@example.com"}]}')
```

**Output:**

```json
{
  "resourceName": "people/c12345",
  "names": [{ "displayName": "Jane Doe" }]
}
```

</details>


<details>
<summary><code>update_contact</code> — Update a contact in Google Contacts</summary>

Updates specific fields of an existing contact.

**Inputs:**
```
- `resource_name`        (string, required) — Resource name of the contact to update (e.g. "people/c12345")
- `update_person_fields` (string, required) — Comma-separated list of fields being updated (e.g. "names,emailAddresses")
- `person`               (string, required) — JSON string with the updated person data
```

**Output:**

```json
{
  "resourceName": "people/c12345",
  "names": [{ "displayName": "Jane Smith" }]
}
```

</details>


<details>
<summary><code>delete_contact</code> — Delete a contact from Google Contacts</summary>

Permanently deletes a contact by resource name.

**Inputs:**
```
- `resource_name`  (string, required) — Resource name of the contact to delete (e.g. "people/c12345")
```

**Output:**

```json
{}
```

</details>


<details>
<summary><code>search_contacts</code> — Search for contacts in Google Contacts</summary>

Searches across the user's contacts using a text query.

**Inputs:**
```
- `query`      (string, required) — Text to search for (matches names, emails, phone numbers, etc.)
- `read_mask`  (string, required) — Comma-separated list of fields to return in results (e.g. "names,emailAddresses")
```

**Output:**

```json
{
  "results": [
    { "person": { "resourceName": "people/c12345", "names": [...] } }
  ]
}
```

</details>


<details>
<summary><code>list_contact_groups</code> — List contact groups in Google Contacts</summary>

Returns all contact groups belonging to the authenticated user.

**Inputs:**
```
- `page_size`   (integer, optional) — Maximum number of groups to return
- `page_token`  (string,  optional) — Page token from a previous list request for pagination
```

**Output:**

```json
{
  "contactGroups": [{ "resourceName": "contactGroups/myContacts", "name": "myContacts" }],
  "nextPageToken": "..."
}
```

</details>


<details>
<summary><code>get_contact_group</code> — Get a contact group from Google Contacts</summary>

Fetches a single contact group by resource name.

**Inputs:**
```
- `resource_name`  (string, required) — Resource name of the contact group (e.g. "contactGroups/abc123")
```

**Output:**

```json
{
  "resourceName": "contactGroups/abc123",
  "name": "Coworkers",
  "memberCount": 5
}
```

</details>


<details>
<summary><code>create_contact_group</code> — Create a contact group in Google Contacts</summary>

Creates a new contact group from a JSON contact group object.

**Inputs:**
```
- `contact_group`  (string, required) — JSON string representing the group to create (e.g. '{"contactGroup":{"name":"Team"}}')
```

**Output:**

```json
{
  "resourceName": "contactGroups/abc123",
  "name": "Team"
}
```

</details>


<details>
<summary><code>update_contact_group</code> — Update a contact group in Google Contacts</summary>

Updates the name or metadata of an existing contact group.

**Inputs:**
```
- `resource_name`   (string, required) — Resource name of the group to update (e.g. "contactGroups/abc123")
- `contact_group`   (string, required) — JSON string with the updated contact group data
```

**Output:**

```json
{
  "resourceName": "contactGroups/abc123",
  "name": "Updated Team"
}
```

</details>


<details>
<summary><code>delete_contact_group</code> — Delete a contact group from Google Contacts</summary>

Permanently deletes a contact group by resource name.

**Inputs:**
```
- `resource_name`  (string, required) — Resource name of the group to delete (e.g. "contactGroups/abc123")
```

**Output:**

```json
{}
```

</details>


<details>
<summary><code>batch_get_contact_groups</code> — Get multiple contact groups at once</summary>

Fetches details for multiple contact groups in a single request.

**Inputs:**
```
- `resource_names`  (string, required) — Comma-separated list of contact group resource names (e.g. "contactGroups/abc,contactGroups/def")
```

**Output:**

```json
{
  "responses": [
    { "contactGroup": { "resourceName": "contactGroups/abc", "name": "Team" } }
  ]
}
```

</details>


<details>
<summary><code>list_other_contacts</code> — List other contacts in Google Contacts</summary>

Returns "Other Contacts" — people automatically saved by Google from interactions (emails, calls, etc.).

**Inputs:**
```
- `read_mask`   (string,  required) — Comma-separated list of fields to return (e.g. "names,emailAddresses")
- `page_size`   (integer, optional) — Maximum number of contacts to return
- `page_token`  (string,  optional) — Page token from a previous list request for pagination
```

**Output:**

```json
{
  "otherContacts": [{ "resourceName": "otherContacts/c99999", "names": [...] }],
  "nextPageToken": "..."
}
```

</details>


<details>
<summary><code>search_other_contacts</code> — Search other contacts in Google Contacts</summary>

Searches the "Other Contacts" list using a text query.

**Inputs:**
```
- `query`      (string, required) — Text to search for
- `read_mask`  (string, required) — Comma-separated list of fields to return in results
```

**Output:**

```json
{
  "results": [
    { "person": { "resourceName": "otherContacts/c99999", "names": [...] } }
  ]
}
```

</details>


<details>
<summary><code>copy_other_contact_to_my_contacts_group</code> — Copy an other contact to My Contacts</summary>

Promotes a contact from "Other Contacts" into the user's main "My Contacts" group.

**Inputs:**
```
- `resource_name`  (string, required) — Resource name of the other contact to copy (e.g. "otherContacts/c99999")
- `copy_mask`      (string, required) — Comma-separated list of fields to copy (e.g. "names,emailAddresses,phoneNumbers")
```

**Output:**

```json
{
  "resourceName": "people/c12345",
  "names": [{ "displayName": "Jane Doe" }]
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Common Parameters</strong></summary>

- `resource_name` — Identifies a specific person or group. Formats:
  - `"people/me"` — the authenticated user
  - `"people/c{id}"` — a specific contact
  - `"contactGroups/{id}"` — a contact group
  - `"otherContacts/c{id}"` — an other contact
- `page_size` — Caps the number of items returned per request. If omitted the API applies its own default limit.
- `page_token` — Opaque token returned in a previous response's `nextPageToken` field. Pass it to retrieve the next page of results.

</details>

<details>
<summary><strong>Field Mask Formats</strong></summary>

**person_fields / read_mask** — comma-separated, no spaces:

```
names,emailAddresses,phoneNumbers,addresses,organizations,birthdays,photos
```

**update_person_fields** — must list every field you are changing:

```
names,emailAddresses
```

**copy_mask** — fields to carry over when promoting an other contact:

```
names,emailAddresses,phoneNumbers
```

**Person JSON structure example:**

```json
{
  "names": [{ "givenName": "Jane", "familyName": "Doe" }],
  "emailAddresses": [{ "value": "jane@example.com" }],
  "phoneNumbers": [{ "value": "+1-555-0100" }]
}
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** OAuth token not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check your credential is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Google account linked to your MewCP credential
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Google account via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending (especially `person` and `contact_group` parameters)
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Google People API Error</strong></summary>

- **Cause:** Upstream Google People API returned an error
- **Solution:**
  1. Check Google Workspace service status at [Google Status Dashboard](https://www.google.com/appsstatus)
  2. Verify your Google account has the required Contacts permissions (scope: `contacts`, `contacts.readonly`)
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Google People API Documentation](https://developers.google.com/people/api/rest)** — Official API reference
- **[Google People API Reference](https://developers.google.com/people/api/rest/v1/people)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
