from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLineEdit,
    QMessageBox,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QWidget,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QIcon
import threading
import logging
from animation.horizontal_scan_widget import HorizontalScanWidget
from guiscan.wafscan import waf_scanning
from guiscan.portscan import port_scanning
from guiscan.subscan import SubdomainScanner
from guiscan.scandir import DirectoryScanner

# Configure logging
logging.basicConfig(
    filename="application.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S1C0N: Advanced Recon & Enumeration Tools")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #121212; color: #EDEDED;")
        self.setWindowIcon(QIcon("elang.png"))
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # URL Input
        self.add_url_input()

        # Tab Widget for Scanning Outputs
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(
            """
            QTabWidget::pane { border: 1px solid #25D366; }
            QTabBar::tab { background: #121212; color: #EDEDED; padding: 10px; }
            QTabBar::tab:selected { background: #25d366; color: #121212; }
            QTabBar::tab:hover { background: #25D366; color: #121212; border: 2px solid #121212}           
            """
        )
        self.main_layout.addWidget(self.tab_widget)

        # Define Tabs for Each Feature
        self.tabs = {
            "🔐 WAF Scanning": {"function": waf_scanning, "tab": None, "columns": ["Target", "Status", "WAF Name"]},
            "🌐 Port Scanning": {"function": port_scanning, "tab": None, "columns": ["Port", "Service", "State"]},
            "🌍 Subdomain Scanning": {"function": None, "tab": None, "columns": ["Subdomain", "Type Panel", "Ports"]},
            "📂 Directory Scanning": {"function": None, "tab": None, "columns": ["Status", "Directory"]},
        }

        self.add_home_tab()
        self.create_feature_description_tab()
        # Create a Tab for Each Feature
        for feature_name in self.tabs:
            self.create_feature_tab(feature_name)

        # Add Log Tab
        self.create_log_tab()

        # Subdomain Scanner Setup
        self.subdomain_scanner = SubdomainScanner()
        self.subdomain_scanner.update_signal.connect(self.update_table_subdomains)
        self.subdomain_scanner.error_signal.connect(self.show_error_message)

        # Directory Scanner Setup
        self.directory_scanner = DirectoryScanner()
        self.directory_scanner.update_signal.connect(self.update_table_directory)
        self.directory_scanner.error_signal.connect(self.show_error_message)
        
    def add_home_tab(self):
        """ Add Home Tab """
        home_tab = QWidget()
        home_layout = QVBoxLayout(home_tab)
        home_layout.addStretch(1)        

        # Logo
        logo = QLabel()
        pixmap = QPixmap("sicon.png")  
        logo.setPixmap(pixmap.scaled(700, 700, Qt.KeepAspectRatio)) 
        logo.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(logo)

        # Subjudul
        subjudul = QLabel("Reconnaissance & Enumerations Tool")
        subjudul.setAlignment(Qt.AlignCenter)
        subjudul.setStyleSheet("font-size: 32px; color: #25D366; font-weight: bold; margin-top: 10px;")
        home_layout.addWidget(subjudul)
        home_layout.addStretch(1)
        # Disclaimer
        disclaimer_text = """
        <p style="font-size: 14px; font-style: italic; color: green;">
        Disclaimer : This Application is intended for educational and demonstration purposes only.Using<br> this tool for 
	scanning or enumeration without explicit permission from the system or network owner<br> may violate 
	applicable laws. The user is fully responsible for any actions taken using this application.
        </p>
        """
        disclaimer = QLabel(disclaimer_text, home_tab)
        disclaimer.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(disclaimer)
        home_layout.addStretch(1)
       
        self.tab_widget.addTab(home_tab, "🏠 Beranda")

    def create_feature_description_tab(self):
        """ Create a tab with explanations for each feature. """
        description_tab = QWidget()
        layout = QVBoxLayout(description_tab)
        
        # Title Label
        title_label = QLabel("Feature Explanations - S1C0N Tools")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: #25D366; font-weight: bold; margin-top:30px; margin-bottom: 30px")
        layout.addWidget(title_label)
        
        # WAF Scanning Explanation
        waf_description = QLabel("""
            <h3>🔐 WAF Scanning</h3>
            WAF Scanning is used to detect the presence of a Web Application Firewall on the target site. 
            This tool helps to determine if the web application is protected by a WAF that may block attacks.
            The scan will look for active WAF names and provide further details about the protection in place.
        """)
        waf_description.setWordWrap(True)
        waf_description.setStyleSheet("font-size: 14px; color: #EDEDED;")
        layout.addWidget(waf_description)

        # Port Scanning Explanation
        port_description = QLabel("""
            <h3>🌐 Port Scanning</h3>
            Port Scanning is used to scan for open ports on the server or web application. 
            Open ports can provide important information about the services running on the server.
            This scan identifies open ports, their status, and the services running on those ports.
        """)
        port_description.setWordWrap(True)
        port_description.setStyleSheet("font-size: 14px; color: #EDEDED;")
        layout.addWidget(port_description)

        # Subdomain Scanning Explanation
        subdomain_description = QLabel("""
            <h3>🌍 Subdomain Scanning</h3>
            Subdomain Scanning is used to discover subdomains associated with the main domain. 
            Subdomains can reveal various services and additional areas within the domain that may serve as entry points for attacks.
            This scan looks for subdomains linked to the target domain and identifies open ports associated with each subdomain.
        """)
        subdomain_description.setWordWrap(True)
        subdomain_description.setStyleSheet("font-size: 14px; color: #EDEDED;")
        layout.addWidget(subdomain_description)

        # Directory Scanning Explanation
        directory_description = QLabel("""
            <h3>📂 Directory Scanning</h3>
            Directory Scanning is used to scan for directories and files available on a web application. 
            Many websites have exposed files and directories that can be exploited by attackers.
            This scan helps identify accessible directories and look for potential data leaks.
        """)
        directory_description.setWordWrap(True)
        directory_description.setStyleSheet("font-size: 14px; color: #EDEDED;")
        layout.addWidget(directory_description)
        layout.addStretch(1)
        
        self.tab_widget.addTab(description_tab, "ℹ️ Description")
    def add_url_input(self):
        """Add URL input field and button."""
        url_layout = QHBoxLayout()
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter the target URL...")
        self.url_entry.setStyleSheet(
            "background-color: #282D35; color: #25D366; padding: 10px; font-size: 14px; border: 2px solid #25D366; border-radius: 5px;"
        )
        url_layout.addWidget(self.url_entry)

        self.scan_all_button = QPushButton("Scan All")
        self.scan_all_button.setStyleSheet(
            """
            QPushButton {
                background-color: #25D366;
                color: #121212;
                font-weight: bold;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1DB954;
                color: #FFFFFF;
            }
            """
        )
        url_layout.addWidget(self.scan_all_button)
        self.scan_all_button.clicked.connect(self.scan_all)

        self.main_layout.addLayout(url_layout)

    def create_feature_tab(self, feature_name):
        """Create a tab for a specific feature."""
        tab = QtWidgets.QWidget()
        layout = QVBoxLayout(tab)

        # Status Label
        status_label = QLabel(f"Status: Idle")
        status_label.setStyleSheet("font-size: 14px; color: #25D366;")
        layout.addWidget(status_label)

        # Horizontal Scanning Animation Widget
        scan_widget = HorizontalScanWidget()
        scan_widget.setMinimumHeight(50)
        layout.addWidget(scan_widget)

        # Table for Results
        result_table = QTableWidget()
        result_table.setColumnCount(len(self.tabs[feature_name]["columns"]))
        result_table.setHorizontalHeaderLabels(self.tabs[feature_name]["columns"])
        result_table.setStyleSheet(
            """
            QTableWidget {
                background-color: #1E1E1E;
                color: #EDEDED;
                border: 2px solid #25D366;
            }
            QHeaderView::section {
                background-color: #121212;
                color: #EDEDED;
                border: 1px solid #25D366;
            }
            QTableWidget::item {
                text-align: center;
            }
            """
        )
        layout.addWidget(result_table)

        # Start Scan Button
        start_button = QPushButton(f"Start {feature_name}")
        start_button.setStyleSheet(
            """
            QPushButton {
                background-color: #25D366;
                color: #121212;
                font-weight: bold;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1DB954;
                color: #FFFFFF;
            }
            """
        )
        if feature_name == "🌍 Subdomain Scanning":
            start_button.clicked.connect(
                lambda: self.start_subdomain_scan(status_label, result_table)
            )
        elif feature_name == "📂 Directory Scanning":
            start_button.clicked.connect(
                lambda: self.start_directory_scan(status_label, result_table)
            )
        else:
            start_button.clicked.connect(
                lambda: self.start_scan(feature_name, status_label, result_table)
            )
        layout.addWidget(start_button)

        self.tabs[feature_name]["tab"] = {
            "status_label": status_label,
            "scan_widget": scan_widget,
            "result_table": result_table,
        }
        self.tab_widget.addTab(tab, feature_name)

    def create_log_tab(self):
        """Create a tab to display logs."""
        log_tab = QtWidgets.QWidget()
        layout = QVBoxLayout(log_tab)

        self.log_textbox = QTextEdit()
        self.log_textbox.setReadOnly(True)
        self.log_textbox.setStyleSheet(
            """
            QTextEdit {
                background-color: #1E1E1E;
                color: #EDEDED;
                border: 2px solid #25D366;
                font-family: Consolas, monospace;
                font-size: 20px;
            }
            """
        )
        layout.addWidget(self.log_textbox)

        self.tab_widget.addTab(log_tab, "📜 Log")

    def add_log_entry(self, message):
        """Add an entry to the log file and GUI."""
        logging.info(message)
        QtCore.QMetaObject.invokeMethod(
            self.log_textbox, "append", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, message)
        )

    def start_scan(self, feature_name, status_label, result_table):
        url = self.url_entry.text().strip()
        if not url:
            self.add_log_entry("Error: No URL entered.")
            QMessageBox.critical(self, "Error", "Please enter a valid URL.")
            return

        scan_function = self.tabs[feature_name]["function"]
        scan_widget = self.tabs[feature_name]["tab"]["scan_widget"]
        scan_widget.start_animation()
        status_label.setText(f"Status: Scanning {feature_name}...")
        self.add_log_entry(f"Started scanning {feature_name} for URL: {url}")

        threading.Thread(
            target=self.run_scan,
            args=(feature_name, url, scan_function, status_label),
            daemon=True,
        ).start()

    def run_scan(self, feature_name, url, scan_function, status_label):
        scan_widget = self.tabs[feature_name]["tab"]["scan_widget"]
        try:
            result = scan_function(url)
            self.update_table(feature_name, result)
            status_label.setText(f"Status: Completed {feature_name}")
            self.add_log_entry(f"Completed scanning {feature_name} for URL: {url}")
        except Exception as e:
            status_label.setText(f"Error: {e}")
            self.add_log_entry(f"Error scanning {feature_name} for URL {url}: {e}")
        finally:
            scan_widget.stop_animation(completed=True)

    def start_subdomain_scan(self, status_label, result_table):
        """Start subdomain scanning."""
        url = self.url_entry.text().strip()
        if not url:
            self.add_log_entry("Error: No URL entered for Subdomain Scanning.")
            QMessageBox.critical(self, "Error", "Please enter a valid URL.")
            return

        scan_widget = self.tabs["🌍 Subdomain Scanning"]["tab"]["scan_widget"]
        # Mulai animasi scanning
        scan_widget.start_animation()

        status_label.setText("Status: Scanning Subdomains...")
        self.add_log_entry(f"Started scanning 🌍 Subdomain Scanning for URL: {url}")


        def run_subdomain_scan():
            try:
                # Jalankan scanning subdomain
                self.subdomain_scanner.subdo_scanning(url)
                status_label.setText("Status: Completed Subdomain Scanning")
                self.add_log_entry(f"Completed scanning 🌍 Subdomain Scanning for URL: {url}")
            except Exception as e:
                status_label.setText(f"Error: {e}")
                self.add_log_entry(f"Error during Subdomain Scanning for URL {url}: {e}")
            finally:
                # Hentikan animasi scanning
                scan_widget.stop_animation(completed=True)             

        threading.Thread(
            target=self.subdomain_scanner.subdo_scanning,
            args=(url,),
            daemon=True,
        ).start()

    def start_directory_scan(self, status_label, result_table):
        """Mulai scan direktori."""
        url = self.url_entry.text().strip()
        if not url:
            QMessageBox.critical(self, "Error", "Please enter a valid URL.")
            self.add_log_entry("Error: No URL entered for Directory Scanning.")
            return

        # Ambil widget animasi dari tab
        scan_widget = self.tabs["📂 Directory Scanning"]["tab"]["scan_widget"]   
        # Mulai animasi scanning
        scan_widget.start_animation()

        status_label.setText("Status: Scanning Directories...")
        self.add_log_entry(f"Started scanning 📂 Directory Scanning for URL: {url}")

        def run_directory_scan():
            try:
                # Jalankan scanning direktori
                self.directory_scanner.scan_dir(url)
                status_label.setText("Status: Completed Directory Scanning")
                self.add_log_entry(f"Completed scanning 📂 Directory Scanning for URL: {url}")
            except Exception as e:
                status_label.setText(f"Error: {e}")
                self.add_log_entry(f"Error during Directory Scanning for URL {url}: {e}")
            finally:
                # Hentikan animasi scanning
                scan_wdidget.stop_animation(completed=True)

        threading.Thread(
            target=self.directory_scanner.scan_dir,
            args=(url,),
            daemon=True,
        ).start()


    def update_table(self, feature_name, result):
        """Update the table with the results."""
        tab = self.tabs[feature_name]["tab"]
        table = tab["result_table"]

        table.setRowCount(0)  
        for row_data in result:
            row_position = table.rowCount()
            table.insertRow(row_position)
            for col, value in enumerate(row_data.values()):
                cell = QTableWidgetItem(str(value))
                cell.setTextAlignment(QtCore.Qt.AlignCenter) 
                table.setItem(row_position, col, cell)

    def update_table_subdomains(self, data):
        """Update the subdomain scanning table."""
        tab = self.tabs["🌍 Subdomain Scanning"]["tab"]
        table = tab["result_table"]

        row_position = table.rowCount()
        table.insertRow(row_position)

        # Add Subdomain, Type Panel, and Ports columns
        table.setItem(row_position, 0, QTableWidgetItem(data["Subdomain"]))
        table.setItem(row_position, 1, QTableWidgetItem(data["Type"]))
        table.setItem(row_position, 2, QTableWidgetItem(data["Ports"]))

        # Center-align all data
        for col in range(3):
            item = table.item(row_position, col)
            if item:
                item.setTextAlignment(QtCore.Qt.AlignCenter)

    def update_table_directory(self, data):
        """Perbarui tabel hasil scan direktori."""
        tab = self.tabs["📂 Directory Scanning"]["tab"]
        table = tab["result_table"]

        row_position = table.rowCount()
        table.insertRow(row_position)

        table.setItem(row_position, 0, QTableWidgetItem(str(data["Status"])))
        table.setItem(row_position, 1, QTableWidgetItem(data["Directory"]))

    
        for col in range(2):
            item = table.item(row_position, col)
            if item:
                item.setTextAlignment(QtCore.Qt.AlignCenter)


    def scan_all(self):
        """Start scanning all features sequentially."""
        for feature_name in self.tabs:
            if feature_name == "🌍 Subdomain Scanning":
                self.start_subdomain_scan(
                    self.tabs[feature_name]["tab"]["status_label"],
                    self.tabs[feature_name]["tab"]["result_table"],
                )
            elif feature_name == "📂 Directory Scanning":
                self.start_directory_scan(
                    self.tabs[feature_name]["tab"]["status_label"],
                    self.tabs[feature_name]["tab"]["result_table"],
                )    
            else:
                self.start_scan(
                    feature_name,
                    self.tabs[feature_name]["tab"]["status_label"],
                    self.tabs[feature_name]["tab"]["result_table"],
                )

    def show_error_message(self, message):
        """Display error messages in a dialog."""
        QMessageBox.critical(self, "Error", message)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ScannerApp()
    window.show()
    sys.exit(app.exec_())
