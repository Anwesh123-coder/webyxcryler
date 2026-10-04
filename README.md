# Update Termux environment repositories
pkg update && pkg upgrade -y

# Install the Python environment and pre-compiled XML parsers
pkg install python python-lxml -y

# Install the remaining web connection and parsing libraries
pip install requests beautifulsoup4
