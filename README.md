# Network Adapter Manager

A GUI application for Windows 11 that allows you to view and manage network adapter configurations.

## Features

- List all network adapters
- View current IP configuration (IP address, subnet mask, gateway)
- Switch between DHCP and static IP configuration
- Apply network configuration changes
- Real-time refresh of adapter information

## Requirements

- Windows 11
- Python 3.7 or higher

## Quick Start

### Option 1 (Easiest):
Simply double-click either:
- `run_app.bat` - Batch script version
- `run_app.ps1` - PowerShell script version

These scripts will:
1. Request administrator privileges (required for network changes)
2. Set up a virtual environment automatically if it doesn't exist
3. Install required dependencies
4. Launch the application

### Option 2 (Manual Setup):

1. Clone or download this repository
2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # For PowerShell
# OR
.\venv\Scripts\activate.bat  # For Command Prompt
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application (as administrator):
```bash
python network_manager.py
```

## Using the Application

1. Select a network adapter from the list
2. The current IP configuration will be displayed
3. To use DHCP:
   - Check the "Use DHCP" checkbox
   - Click "Apply Changes"
4. To set a static IP:
   - Uncheck the "Use DHCP" checkbox
   - Enter the IP address, subnet mask, and gateway
   - Click "Apply Changes"
5. Use the "Refresh" button to update the adapter list and information

## Note

- Changing network settings requires administrator privileges
- Invalid IP configurations may cause network connectivity issues
- Always double-check your settings before applying changes

## Standalone Executable

A compiled standalone executable is available in the [Releases](../../releases) section. The executable:
- Requires no installation or Python environment
- Works on Windows 7 and later
- Includes all necessary dependencies
- Automatically requests administrator privileges
- Features a custom application icon

To use the standalone version:
1. Download `NetworkManager.exe` from the latest release
2. Double-click to run (will request administrator privileges)
3. No installation needed! 