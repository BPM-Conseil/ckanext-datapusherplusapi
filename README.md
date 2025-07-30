# CKAN Extension: Datapusher Plus API

CKAN extension that provides a REST API for submitting files to the datapusher plus service.

## Compatibility

- CKAN 2.9.x
- Python 3.7+

## Installation

1. Clone or copy the extension to your CKAN environment:
```bash
cd /usr/lib/ckan/default/src/
git clone https://github.com/your-org/ckanext-datapusherplusapi.git
```

2. Install the extension:
```bash
cd ckanext-datapusherplusapi
pip install -e .
```

3. Add `datapusherplusapi` to the plugins list in your CKAN configuration file:
```ini
ckan.plugins = ... datapusherplusapi
```

4. Restart CKAN

## Configuration

Add these parameters to your CKAN configuration file:

```ini
# Datapusher plus service URL (required)
ckanext.datapusher_plus.url = http://datapusher-plus:8000

# Request timeout in seconds (optional, default: 30)
ckanext.datapusher_plus.timeout = 30

# Maximum number of retries (optional, default: 3)
ckanext.datapusher_plus.max_retries = 3

# Maximum file size in MB (optional, default: 100)
ckanext.datapusher_plus.max_file_size = 100

# Enable detailed logging (optional, default: False)
ckanext.datapusher_plus.debug = True
```

## API Usage

### Submit a file to datapusher plus

**Endpoint:** `POST /api/3/action/datapusher_plus_submit`

**Parameters:**
- `resource_id` (required): CKAN resource ID
- `package_id` (optional): CKAN package ID
- `force` (optional): Force submission even if already in progress (default: false)

**Request example:**
```bash
curl -X POST "http://your-ckan-site/api/3/action/datapusher_plus_submit" \
  -H "Content-Type: application/json" \
  -H "Authorization: your-api-key" \
  -d '{
    "resource_id": "12345678-1234-1234-1234-123456789012",
    "force": false
  }'
```

**Success response:**
```json
{
  "success": true,
  "message": "File successfully submitted to datapusher plus",
  "job_id": "job-12345",
  "resource_id": "12345678-1234-1234-1234-123456789012"
}
```

**Error response:**
```json
{
  "success": false,
  "error": "Error description"
}
```

### Get processing status

**Endpoint:** `GET /api/3/action/datapusher_plus_status/{resource_id}`

**Request example:**
```bash
curl "http://your-ckan-site/api/3/action/datapusher_plus_status/12345678-1234-1234-1234-123456789012" \
  -H "Authorization: your-api-key"
```

**Response:**
```json
{
  "success": true,
  "resource_id": "12345678-1234-1234-1234-123456789012",
  "status": "submitted",
  "submitted": "2024-01-15T10:30:00",
  "resource_url": "http://example.com/data.csv"
}
```

## Supported file formats

By default, the following formats are supported:
- CSV
- TSV
- XLS
- XLSX
- ODS
- JSON
- XML

## Authentication

The API uses the standard CKAN authentication system. You must:
1. Be logged in as an authorized user
2. Or provide a valid API key in the `Authorization` header

## Error handling

The API returns standard HTTP error codes:
- `200`: Success
- `400`: Invalid parameters
- `403`: Unauthorized
- `404`: Resource not found
- `500`: Internal server error

## Development

### Tests

To run the tests:
```bash
pytest ckanext/datapusherplusapi/tests/
```

### Project structure

```
ckanext-datapusherplusapi/
├── ckanext/
│   └── datapusherplusapi/
│       ├── __init__.py
│       ├── plugin.py          # Main plugin
│       ├── views.py           # API endpoints
│       ├── config.py          # Configuration
│       ├── helpers.py         # Utility functions
│       └── tests/
│           ├── __init__.py
│           └── test_api.py    # Unit tests
├── setup.py
└── README.md
```

## Dependencies

- CKAN >= 2.9.0
- requests
- flask

## License

AGPL v3

## Support

To report bugs or request features, please create an issue on the project's GitHub repository.
