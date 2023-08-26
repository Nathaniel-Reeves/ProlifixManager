# API Function Documentation

## Function: get_organizations()

This function retrieves information about organizations from a database. It supports several query parameters to filter and populate the response data.

### Endpoint

- Route: `'/organizations'`
- HTTP Methods: `GET`

### Query Parameters

- `org-id` (optional, integer): Filter organizations by a specific organization ID.
- `org-type` (optional, list): Filter organizations by type. Accepted values are `'client'`, `'supplier'`, and `'lab'`. Multiple values can be provided.
- `populate` (optional, list): Specify child resources to populate within each organization. Accepted values are `'facilities'`, `'sales-orders'`, `'purchase-orders'`, `'people'`, `'components'`, and `'products'`. Multiple values can be provided.

### Response

The function returns a JSON response containing the requested organizations' information. The response structure is as follows:

```json
{
  "organization_id": {
    "organization_id": <organization_id>,
    "date_entered": <date_entered>,
    "website_url": <website_url>,
    "vetted": <vetted>,
    "date_vetted": <date_vetted>,
    "risk_level": <risk_level>,
    "supplier": <supplier>,
    "client": <client>,
    "lab": <lab>,
    "other": <other>,
    "doc": <doc>,
    "notes": <notes>,
    "organization_name": <organization_name>,
    "facilities": <facilities>,
    "sales_orders": <sales_orders>,
    "purchase_orders": <purchase_orders>,
    "people": <people>,
    "components": <components>,
    "products": <products>
  },
  ...
}
```

- `<organization_id>` (integer): The ID of the organization.
- `<date_entered>` (string): The date the organization was entered.
- `<website_url>` (string): The URL of the organization's website.
- `<vetted>` (boolean): Indicates if the organization is vetted.
- `<date_vetted>` (string): The date the organization was vetted.
- `<risk_level>` (string): The risk level associated with the organization.
- `<supplier>` (boolean): Indicates if the organization is a supplier.
- `<client>` (boolean): Indicates if the organization is a client.
- `<lab>` (boolean): Indicates if the organization is a lab.
- `<other>` (boolean): Indicates if the organization has another type.
- `<doc>` (boolean): Indicates if the organization has documentation.
- `<notes>` (string): Additional notes about the organization.
- `<organization_name>` (string): The name of the organization.
- `<facilities>` (object, optional): Populated child resource containing information about facilities associated with the organization.
- `<sales_orders>` (object, optional): Populated child resource containing information about sales orders associated with the organization.
- `<purchase_orders>` (object, optional): Populated child resource containing information about purchase orders associated with the organization.
- `<people>` (object, optional): Populated child resource containing information about people associated with the organization.
- `<components>` (object, optional): Populated child resource containing information about components associated with the organization.
- `<products>` (object, optional): Populated child resource containing information about products associated with the organization.

If an error occurs during the execution of the function, an error message will be returned in the JSON response.

---


