import sys, os, pygame, time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QFileDialog, QLabel, QHBoxLayout, QSlider, QPushButton)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon # Nueva importación para el icono
from pypresence import Presence

class MKDLPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        pygame.init()
        self.mixer = pygame.mixer
        self.mixer.init()
        
        # Discord Rich Presence
        self.client_id = "1468317452969709570"
        self.RPC = None
        self.init_discord()
        
        self.playlist = []
        self.current_idx = -1
        self.is_paused = False
        self.loop = False
        self.offset = 0
        self.is_seeking = False
        self.duration = 0

        self.init_ui()
        
        self.core_timer = QTimer(self)
        self.core_timer.timeout.connect(self.core_loop)
        self.core_timer.start(100)

    def init_discord(self):
        try:
            self.RPC = Presence(self.client_id)
            self.RPC.connect()
        except: self.RPC = None

    def update_discord(self, state="Listening"):
        if not self.RPC: return
        try:
            track = os.path.basename(self.playlist[self.current_idx])[:120] if self.playlist else "Idle"
            start_t = None
            if not self.is_paused and self.playlist:
                curr = (self.mixer.music.get_pos() / 1000) + self.offset
                start_t = time.time() - curr

            self.RPC.update(
                details=track,
                state=state,
                large_image="logo", # Debe llamarse así en el Discord Developer Portal
                large_text="mkdlplayer",
                start=start_t
            )
        except: pass

    def init_ui(self):
        self.setWindowTitle('mkdlplayer')
        self.setFixedSize(600, 240)
        
        # CARGAR LOGO LOCAL: Ajusta la ruta si tu carpeta se llama distinto
        icon_path = os.path.join("assets", "logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet("""
            QMainWindow { background-color: #0f0f0f; }
            QLabel { color: #eee; font-family: 'Segoe UI'; font-size: 14px; }
            QPushButton { 
                background: #1a1a1a; color: #aaa; border: 1px solid #333; 
                border-radius: 4px; padding: 5px; font-size: 10px; font-weight: bold;
            }
            QPushButton:hover { border-color: #5dbcd2; color: #fff; }
            #active { color: #5dbcd2; border-color: #5dbcd2; background: #0a1f24; }
            QSlider::groove:horizontal { height: 3px; background: #333; }
            QSlider::handle:horizontal { background: #fff; width: 10px; height: 10px; margin: -4px 0; border-radius: 5px; }
            QSlider::sub-page:horizontal { background: #5dbcd2; }
        """)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 20, 30, 20)

        self.lbl = QLabel("IDLE")
        self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        
        self.sld = QSlider(Qt.Orientation.Horizontal)
        self.sld.sliderPressed.connect(self.on_seek_start)
        self.sld.sliderReleased.connect(self.on_seek_end)

        ctrls = QHBoxLayout()
        self.btn_prev = QPushButton("PREV")
        self.btn_play = QPushButton("PLAY / PAUSE")
        self.btn_next = QPushButton("NEXT")
        self.btn_loop = QPushButton("REPEAT: OFF")

        self.btn_prev.clicked.connect(self.prev)
        self.btn_play.clicked.connect(self.play_pause)
        self.btn_next.clicked.connect(self.next)
        self.btn_loop.clicked.connect(self.toggle_loop)

        for b in [self.btn_prev, self.btn_play, self.btn_next, self.btn_loop]:
            ctrls.addWidget(b)

        bottom = QHBoxLayout()
        self.v_sld = QSlider(Qt.Orientation.Horizontal)
        self.v_sld.setRange(0, 100); self.v_sld.setValue(70); self.v_sld.setFixedWidth(80)
        self.v_sld.valueChanged.connect(lambda v: self.mixer.music.set_volume(v/100))
        
        b_file = QPushButton("FILE"); b_file.clicked.connect(self.open_f)
        b_fold = QPushButton("FOLDER"); b_fold.clicked.connect(self.open_d)

        bottom.addWidget(QLabel("VOL", styleSheet="font-size: 9px; color: #555;"))
        bottom.addWidget(self.v_sld)
        bottom.addStretch()
        bottom.addWidget(b_file); bottom.addWidget(b_fold)

        layout.addWidget(self.lbl); layout.addWidget(self.sld)
        layout.addLayout(ctrls); layout.addLayout(bottom)
        self.setCentralWidget(central)

    def core_loop(self):
        if not self.playlist or self.is_paused or self.is_seeking:
            return

        current_pos = (self.mixer.music.get_pos() / 1000) + self.offset
        
        if current_pos >= self.duration - 0.2:
            if self.loop: self.load_song(self.playlist[self.current_idx])
            else: self.next()
            return

        self.sld.blockSignals(True)
        self.sld.setValue(int(current_pos))
        self.sld.blockSignals(False)

    def load_song(self, path):
        try:
            self.mixer.music.load(path)
            snd = self.mixer.Sound(path)
            self.duration = snd.get_length()
            self.sld.setRange(0, int(self.duration))
            self.lbl.setText(os.path.basename(path)[:40])
            self.mixer.music.play()
            self.offset = 0
            self.is_paused = False
            self.update_discord()
        except: pass

    def on_seek_start(self):
        self.is_seeking = True

    def on_seek_end(self):
        if self.playlist:
            p = self.sld.value()
            self.offset = p
            self.mixer.music.play(start=p)
            QTimer.singleShot(150, lambda: setattr(self, 'is_seeking', False))
            self.update_discord()

    def open_f(self):
        f, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Audio (*.mp3 *.flac *.opus)")
        if f: self.playlist = [f]; self.current_idx = 0; self.load_song(f)

    def open_d(self):
        d = QFileDialog.getExistingDirectory(self, "Open Folder")
        if d:
            self.playlist = sorted([os.path.join(d, x) for x in os.listdir(d) if x.lower().endswith(('.mp3', '.flac', '.opus'))])
            if self.playlist: self.current_idx = 0; self.load_song(self.playlist[0])

    def play_pause(self):
        if not self.playlist: return
        if self.is_paused: 
            self.mixer.music.unpause()
            self.update_discord()
        else: 
            self.mixer.music.pause()
            self.update_discord(state="Paused")
        self.is_paused = not self.is_paused

    def toggle_loop(self):
        self.loop = not self.loop
        self.btn_loop.setText(f"REPEAT: {'ON' if self.loop else 'OFF'}")
        self.btn_loop.setObjectName("active" if self.loop else "")
        self.btn_loop.style().unpolish(self.btn_loop)
        self.btn_loop.style().polish(self.btn_loop)

    def next(self):
        if self.playlist:
            self.current_idx = (self.current_idx + 1) % len(self.playlist)
            self.load_song(self.playlist[self.current_idx])

    def prev(self):
        if self.playlist:
            self.current_idx = (self.current_idx - 1) % len(self.playlist)
            self.load_song(self.playlist[self.current_idx])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MKDLPlayer()
    ex.show()
    sys.exit(app.exec())