from PyQt5 import QtWidgets, QtCore, QtGui


class HorizontalScanWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.position = 0  # Posisi awal scan
        self.direction = 1  # 1 untuk kanan, -1 untuk kiri
        self.completed_mode = False  # Mode untuk scanning selesai
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_animation)

    def start_animation(self):
        """Start the scanning animation."""
        self.completed_mode = False  # Reset ke mode scanning biasa
        self.position = 0  # Reset posisi animasi
        self.timer.start(30)  # Animasi berjalan dengan interval 30ms

    def stop_animation(self, completed=False):
        """Stop the scanning animation."""
        self.completed_mode = completed  # Aktifkan mode "Scanning Completed" jika selesai
        self.timer.stop()  # Hentikan timer animasi
        self.update()  # Repaint untuk menggambar ulang dengan atau tanpa animasi

    def update_animation(self):
        """Update posisi untuk animasi horizontal."""
        if not self.completed_mode:
            self.position += 5 * self.direction
            if self.position >= self.width() or self.position <= 0:
                self.direction *= -1  # Balik arah jika mencapai tepi
        self.update()  # Trigger repaint untuk menggambar ulang

    def paintEvent(self, event):
        """Draw the horizontal scanning animation."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Background box
        painter.setBrush(QtGui.QColor(30, 30, 30))  # Warna latar belakang box
        painter.drawRect(self.rect())

        if self.completed_mode:
            # Tulis teks "Scanning Completed"
            painter.setPen(QtGui.QPen(QtGui.QColor(37, 211, 102)))
            font = QtGui.QFont("Arial", 16, QtGui.QFont.Bold)
            painter.setFont(font)
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Scanning Completed")
        else:
            # Draw scanning animation
            gradient = QtGui.QLinearGradient(0, 0, self.width(), 0)
            gradient.setColorAt(0.0, QtGui.QColor(37, 211, 102, 0))  # Transparan
            gradient.setColorAt(0.5, QtGui.QColor(37, 211, 102, 150))  # Hijau terang
            gradient.setColorAt(1.0, QtGui.QColor(37, 211, 102, 0))  # Transparan
            painter.setBrush(QtGui.QBrush(gradient))
            painter.setPen(QtCore.Qt.NoPen)
            scan_width = self.width() // 4
            painter.drawRect(self.position - scan_width // 2, 0, scan_width, self.height())
