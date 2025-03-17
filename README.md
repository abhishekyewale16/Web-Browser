## Overview
A lightweight web browser built with Python and PyQt5. This application provides essential browsing features with a clean interface.

## Features
- Standard navigation controls (back, forward, refresh, home)
- URL address bar with direct input
- Bookmarks toolbar with preset links
- Browsing history tracking and viewing
- File download support

## Technologies Used
- Python 3
- PyQt5
- SQLite3 for history storage

## Requirements
- Python 3.6+
- PyQt5
- PyQtWebEngine

## Installation
1. Clone the repository or download the source code
2. Install dependencies:
   ```
   pip install PyQt5 PyQtWebEngine
   ```
3. Run the application:
   ```
   python "Web Browser.py"
   ```

## Usage
- Navigate to websites by entering URLs in the address bar
- Use the navigation buttons to move back and forward through pages
- Access frequently visited sites through the bookmarks toolbar
- View your browsing history by clicking the "History" button

## Database
The application stores browsing history in an SQLite database named `browser_history.db`.
