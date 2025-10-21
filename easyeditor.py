import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QFileDialog, QSizePolicy, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QFont, QColor
from PIL import Image, ImageEnhance

app = QApplication(sys.argv)
app.setStyle("Fusion")
win = QWidget()
win.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
win.setAttribute(Qt.WA_TranslucentBackground)
win.resize(820,560)
container = QFrame(win)
container.setObjectName("container")
container.setGeometry(10,10,800,540)
titlebar = QFrame(container)
titlebar.setObjectName("titlebar")
titlebar.setGeometry(0,0,800,48)
traffic = QFrame(titlebar)
traffic.setGeometry(12,8,72,32)
btn_close = QPushButton("", traffic)
btn_close.setGeometry(0,0,16,16)
btn_close.setObjectName("close")
btn_min = QPushButton("", traffic)
btn_min.setGeometry(22,0,16,16)
btn_min.setObjectName("min")
btn_max = QPushButton("", traffic)
btn_max.setGeometry(44,0,16,16)
btn_max.setObjectName("max")
title = QLabel("Easy Editor", titlebar)
title.setGeometry(100,6,400,36)
title.setObjectName("title")
left_col = QFrame(container)
left_col.setObjectName("left_col")
left_col.setGeometry(12,64,220,464)
btn_dir = QPushButton("Folder", left_col)
btn_dir.setGeometry(12,12,196,40)
file_list = QListWidget(left_col)
file_list.setGeometry(12,64,196,388)
right_col = QFrame(container)
right_col.setObjectName("right_col")
right_col.setGeometry(244,64,544,464)
image_holder = QLabel("Drop a folder and pick an image", right_col)
image_holder.setGeometry(12,12,520,380)
image_holder.setAlignment(Qt.AlignCenter)
image_holder.setObjectName("image_holder")
tools = QFrame(right_col)
tools.setGeometry(12,404,520,48)
btn_left = QPushButton("⟲", tools)
btn_left.setGeometry(6,6,72,36)
btn_right = QPushButton("⟳", tools)
btn_right.setGeometry(84,6,72,36)
btn_flip = QPushButton("⇋", tools)
btn_flip.setGeometry(162,6,72,36)
btn_sharp = QPushButton("✧", tools)
btn_sharp.setGeometry(240,6,144,36)
btn_bw = QPushButton("B/W", tools)
btn_bw.setGeometry(392,6,120,36)
shadow = QGraphicsDropShadowEffect()
shadow.setBlurRadius(28)
shadow.setOffset(0,8)
container.setGraphicsEffect(shadow)
app_font = QFont("Segoe UI",9)
app.setFont(app_font)
stylesheet = """
#container {background: rgba(255,255,255,230); border-radius:14px;}
#titlebar {background: transparent;}
#title {color:#333; font-weight:600; font-size:14px;}
#close {background: #ff5f57; border-radius:8px; border: none;}
#min {background: #ffbd2e; border-radius:8px; border: none;}
#max {background: #28c93a; border-radius:8px; border: none;}
QPushButton {background: rgba(255,255,255,200); border: 1px solid rgba(120,120,130,0.06); border-radius:10px; padding:6px 10px; font-weight:600;}
QPushButton:hover {background: rgba(255,255,255,240);}
QListWidget {background: rgba(250,250,252,200); border-radius:10px; padding:6px;}
QLabel#image_holder {background: linear-gradient(180deg, rgba(255,255,255,0.6), rgba(245,245,247,0.6)); border-radius:12px; color:#777; font-size:13px; border:1px solid rgba(120,120,130,0.04);}
#left_col { }
#right_col { }
"""
app.setStyleSheet(stylesheet)
workdir = ""
class ImageProcessor:
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified"
    def load(self, d, f):
        self.dir = d
        self.filename = f
        path = os.path.join(self.dir, self.filename)
        self.image = Image.open(path).convert("RGBA")
    def save_and_show(self):
        path = os.path.join(self.dir, self.save_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        dest = os.path.join(path, self.filename)
        rgb = self.image.convert("RGB")
        rgb.save(dest)
        self.show(dest)
    def show(self, path):
        pix = QPixmap(path)
        w = image_holder.width()
        h = image_holder.height()
        pix = pix.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_holder.setPixmap(pix)
    def bw(self):
        self.image = self.image.convert("L").convert("RGBA")
        self.save_and_show()
    def left(self):
        self.image = self.image.rotate(90, expand=True)
        self.save_and_show()
    def right(self):
        self.image = self.image.rotate(-90, expand=True)
        self.save_and_show()
    def flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_and_show()
    def sharp(self):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(2.0)
        self.save_and_show()
proc = ImageProcessor()
def choose_folder():
    global workdir
    d = QFileDialog.getExistingDirectory(None, "Select Folder", os.path.expanduser("~"))
    if d:
        workdir = d
        load_list()
def load_list():
    if not workdir:
        return
    files = [f for f in os.listdir(workdir) if f.lower().endswith((".jpg",".jpeg",".png",".bmp",".gif"))]
    file_list.clear()
    for f in files:
        file_list.addItem(f)
def show_selected():
    if file_list.currentRow() < 0:
        return
    fn = file_list.currentItem().text()
    proc.load(workdir, fn)
    image_holder.setText("")
    proc.show(os.path.join(workdir, fn))
def enable_buttons(flag):
    for b in (btn_left, btn_right, btn_flip, btn_sharp, btn_bw):
        b.setEnabled(flag)
file_list.currentRowChanged.connect(show_selected)
btn_dir.clicked.connect(choose_folder)
btn_bw.clicked.connect(lambda: safe_action(proc.bw))
btn_left.clicked.connect(lambda: safe_action(proc.left))
btn_right.clicked.connect(lambda: safe_action(proc.right))
btn_flip.clicked.connect(lambda: safe_action(proc.flip))
btn_sharp.clicked.connect(lambda: safe_action(proc.sharp))
def safe_action(fn):
    try:
        if proc.image:
            fn()
        else:
            pass
    except Exception:
        pass
def close_window():
    win.close()
def minimize_window():
    win.showMinimized()
def toggle_max():
    if win.isMaximized():
        win.showNormal()
    else:
        win.showMaximized()
btn_close.clicked.connect(close_window)
btn_min.clicked.connect(minimize_window)
btn_max.clicked.connect(toggle_max)
drag_pos = QPoint()
dragging = False
def mousePressEvent(e):
    global dragging, drag_pos
    if e.button() == Qt.LeftButton:
        if titlebar.geometry().contains(e.pos()):
            dragging = True
            drag_pos = e.globalPos() - win.frameGeometry().topLeft()
def mouseMoveEvent(e):
    global dragging, drag_pos
    if dragging:
        win.move(e.globalPos() - drag_pos)
def mouseReleaseEvent(e):
    global dragging
    dragging = False
win.mousePressEvent = mousePressEvent
win.mouseMoveEvent = mouseMoveEvent
win.mouseReleaseEvent = mouseReleaseEvent
win.show()
app.exec_()