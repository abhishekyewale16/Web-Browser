import sys
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *

class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com/'))
        self.browser.urlChanged.connect(self.update_AddressBar)
        self.browser.page().profile().downloadRequested.connect(self.download_requested)  # Connect the download_requested method
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

        pythongeeks = QAction("KBP College", self)
        pythongeeks.setStatusTip("Go to PythonGeeks website")
        pythongeeks.triggered.connect(lambda: self.go_to_URL(QUrl("https://kbpcollegevashi.edu.in")))
        bookmarks_toolbar.addAction(pythongeeks)

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

    def update_AddressBar(self, url):
        self.URLBar.setText(url.toString())
        self.URLBar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName('Web Browser')

window = Window()
app.exec_()
