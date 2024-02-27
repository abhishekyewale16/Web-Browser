import sys
from PyQt5.QtCore import QUrl, QDir, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QToolBar,
    QFileDialog, QLineEdit, QDialog, QVBoxLayout,
    QListWidget, QListWidgetItem, QLabel
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QUrl, QDir
import sqlite3
from datetime import datetime


DATABASE_FILE = 'browser_history.db'
TABLE_NAME = 'history'

class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com/'))
        self.browser.urlChanged.connect(self.update_AddressBar)
        self.browser.page().profile().downloadRequested.connect(self.download_requested)
        self.setCentralWidget(self.browser)

        self.status_bar = self.statusBar()

        self.navigation_bar = QToolBar('Navigation Toolbar')
        self.addToolBar(self.navigation_bar)

        history_button = QAction("History", self)
        history_button.setStatusTip("Show Browser History")
        history_button.triggered.connect(self.create_history_window)
        self.navigation_bar.addAction(history_button)

        back_button = QAction("Back", self)
        back_button.setStatusTip('Go to the previous page you visited')
        back_button.triggered.connect(self.browser.back)
        self.navigation_bar.addAction(back_button)

        refresh_button = QAction("Refresh", self)
        refresh_button.setStatusTip('Refresh this page')
        refresh_button.triggered.connect(self.browser.reload)
        self.navigation_bar.addAction(refresh_button)

        next_button = QAction("Next", self)
        next_button.setStatusTip('Go to the next page')
        next_button.triggered.connect(self.browser.forward)
        self.navigation_bar.addAction(next_button)

        home_button = QAction("Home", self)
        home_button.setStatusTip('Go to the home page (Google page)')
        home_button.triggered.connect(self.go_to_home)
        self.navigation_bar.addAction(home_button)

        self.navigation_bar.addSeparator()

        self.URLBar = QLineEdit()
        self.URLBar.returnPressed.connect(lambda: self.go_to_URL(QUrl(self.URLBar.text())))
        self.navigation_bar.addWidget(self.URLBar)

        self.addToolBarBreak()

        bookmarks_toolbar = QToolBar('Bookmarks', self)
        self.addToolBar(bookmarks_toolbar)

        KBPCollege = QAction("KBP College", self)
        KBPCollege.setStatusTip("Go to College Website website")
        KBPCollege.triggered.connect(lambda: self.go_to_URL(QUrl("https://kbpcollegevashi.edu.in")))
        bookmarks_toolbar.addAction(KBPCollege)

        facebook = QAction("Facebook", self)
        facebook.setStatusTip("Go to Facebook")
        facebook.triggered.connect(lambda: self.go_to_URL(QUrl("https://www.facebook.com")))
        bookmarks_toolbar.addAction(facebook)

        linkedin = QAction("LinkedIn", self)
        linkedin.setStatusTip("Go to LinkedIn")
        linkedin.triggered.connect(lambda: self.go_to_URL(QUrl("https://in.linkedin.com")))
        bookmarks_toolbar.addAction(linkedin)

        instagram = QAction("Instagram", self)
        instagram.setStatusTip("Go to Instagram")
        instagram.triggered.connect(lambda: self.go_to_URL(QUrl("https://www.instagram.com")))
        bookmarks_toolbar.addAction(instagram)

        twitter = QAction("Twitter", self)
        twitter.setStatusTip('Go to Twitter')
        twitter.triggered.connect(lambda: self.go_to_URL(QUrl("https://www.twitter.com")))
        bookmarks_toolbar.addAction(twitter)

        self.browser.setMaximumSize(1920, 1080)
        self.show()
        self.create_table()

    def create_history_window(self):
        history_window = HistoryWindow()
        history_window.exec_()

    def create_table(self):
        try:
            connection = sqlite3.connect(DATABASE_FILE)
            cursor = connection.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            connection.commit()
        except sqlite3.Error as e:
            print("SQLite error:", e)
        finally:
            connection.close()

    def insert_url_to_history(self, full_url):
        try:
            connection = sqlite3.connect(DATABASE_FILE)
            cursor = connection.cursor()

            # Get current timestamp in a specific format
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute(f'INSERT INTO {TABLE_NAME} (url, timestamp) VALUES (?, ?)', (full_url, timestamp))
            connection.commit()
        except sqlite3.Error as e:
            print("SQLite error:", e)
        finally:
            connection.close()

    def download_requested(self, download):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", QDir.currentPath(), "All Files (*)", options=options)
        if file_path:
            download.setPath(file_path)
            download.accept()

    def go_to_home(self):
        self.browser.setUrl(QUrl('https://www.google.com/'))

    def go_to_URL(self, url: QUrl):
        if url.scheme() == '':
            url.setScheme('https://')
        self.browser.setUrl(url)
        self.update_AddressBar(url)
        # Insert the full URL into the history table
        self.insert_url_to_history(url.toString())

    def update_AddressBar(self, url):
        self.URLBar.setText(url.toString())
        self.URLBar.setCursorPosition(0)
        # Insert the full URL into the history table
        self.insert_url_to_history(url.toString())


class HistoryWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super(HistoryWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Browser History")
        self.setMinimumSize(800, 600)

        self.history_list = QListWidget(self)
        self.history_list.setStyleSheet("font-size: 16px;")  # Adjust font size

        self.populate_history_list()

        layout = QVBoxLayout(self)
        layout.addWidget(self.history_list)
        self.setLayout(layout)

    def populate_history_list(self):
        try:
            # Establish a connection to the SQLite database
            connection = sqlite3.connect(DATABASE_FILE)
            cursor = connection.cursor()

            # Query distinct dates from the history table, ordered by timestamp in descending order
            cursor.execute(f'SELECT DISTINCT DATE(timestamp) FROM {TABLE_NAME} ORDER BY timestamp DESC')
            distinct_dates = cursor.fetchall()

            # Iterate through each distinct date
            for date_entry in distinct_dates:
                # Extract the date from the query result
                date = date_entry[0]

                # Create a QLabel for the date and set its font and size
                date_label = QLabel(f"\n{date}\n")
                date_label.setFont(QFont("Arial", 5, QFont.Bold))

                # Add an empty item to the history list
                self.history_list.addItem(QListWidgetItem())

                # Set the widget for the last added item in the history list to be the date label
                self.history_list.setItemWidget(self.history_list.item(self.history_list.count() - 1), date_label)

                # Query history entries for the current date, ordered by timestamp in descending order
                cursor.execute(f'SELECT * FROM {TABLE_NAME} WHERE DATE(timestamp) = ? ORDER BY timestamp DESC', (date,))
                history_data = cursor.fetchall()

                # Iterate through each history entry for the current date
                for entry in history_data:
                    # Extract URL and timestamp from the entry
                    url = entry[1]
                    timestamp = entry[2]

                    # Create a QListWidgetItem for the history entry and set its font and size
                    item = QListWidgetItem(f"{timestamp}: {url}")
                    item.setFont(QFont("Arial", 14))

                    # Add the history entry item to the history list
                    self.history_list.addItem(item)

        except sqlite3.Error as e:
            # Handle SQLite errors by printing the error message
            print("SQLite error:", e)

        finally:
            # Close the database connection in the 'finally' block to ensure it's closed even if an exception occurs
            connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName('Web Browser')

    window = Window()
    app.exec_()
