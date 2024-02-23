# Web Browser (Hist)
import sys
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
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

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.navigation_bar = QToolBar('Navigation Toolbar')
        self.addToolBar(self.navigation_bar)

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

        self.browser.maximumSize()
        self.show()
        self.create_table()
    
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

app = QApplication(sys.argv)
app.setApplicationName('Web Browser')

window = Window()
app.exec_()
