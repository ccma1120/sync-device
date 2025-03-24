# Device List Sync

This repository automatically syncs device lists from IAR's website and maintains a history of changes.

## Files
- `device-iar.txt`: Current list of supported devices
- `compare-iar.txt`: Comparison showing latest changes
- `sync-iar.py`: Python script that performs the sync

## Automation
The sync process runs automatically every day at midnight UTC through GitHub Actions. You can also trigger it manually from the Actions tab.

## Requirements
- Python 3.x
- `requests`
- `beautifulsoup4`

To install dependencies:
```bash
pip install requests beautifulsoup4
```