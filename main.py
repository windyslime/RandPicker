import sys
import random
from random import randint as rand

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QMouseEvent
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGraphicsDropShadowEffect, QSystemTrayIcon, QFrame
from qfluentwidgets import PushButton, SystemTrayMenu, FluentIcon as fIcon, Action
from loguru import logger

import conf
from settings import open_settings

# 适配高DPI缩放
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

excluded_number = [5, 6, 12, 31]


class Widget(QWidget):
    """
    主浮窗。
    """

    def __init__(self):
        super().__init__()
        self.m_Position = None
        self.p_Position = None
        self.r_Position = None
        self.init_ui()
        self.systemTrayIcon = SystemTrayIcon(self)
        self.systemTrayIcon.show()

    def init_ui(self):
        uic.loadUi("./ui/widget.ui", self)

        # 设置窗口无边框和透明背景
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        if sys.platform == 'darwin':
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.Widget
            )
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint |
                                Qt.WindowType.Tool)

        background = self.findChild(QFrame, 'backgnd')
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(28)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(6)
        shadow_effect.setColor(QColor(0, 0, 0, 75))
        background.setGraphicsEffect(shadow_effect)

        btn = self.findChild(PushButton, 'btn')
        btn.clicked.connect(lambda: self.pick())

        btn_clear = self.findChild(PushButton, 'btn_clear')
        btn_clear.clicked.connect(lambda: open_settings())

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.m_Position = event.globalPosition().toPoint() - self.pos()  # 获取鼠标相对窗口的位置
            self.p_Position = event.globalPosition().toPoint()  # 获取鼠标相对屏幕的位置
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.m_Position)  # 更改窗口位置
            event.accept()

    def pick(self):
        """
        随机选人。
        """
        num = rand(1, conf.get_students_num())
        while num in excluded_number:
            num = rand(1, conf.get_students_num())
        logger.info(f'随机数已生成。JSON 索引是 {num}。')
        student = conf.get(num)
        logger.info(f'已获取 JSON 索引是 {num} 的学生信息。{student}')
        name = self.findChild(QLabel, 'name')
        id_ = self.findChild(QLabel, 'id')
        if student['short_id'] < 10:
            num = f'0{student['short_id']}'
        else:
            num = f'{student["short_id"]}'
        name.setText(f'{num} {student['name']}')
        id_.setText(str(student['id']))

    def clear(self):
        name = self.findChild(QLabel, 'name')
        id_ = self.findChild(QLabel, 'id')
        name.setText('无结果')
        id_.setText('000000')
        logger.info('清除结果')


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())

        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action(fIcon.SETTING, '设置', triggered=lambda: open_settings()),
            Action(fIcon.CLOSE, '关闭', triggered=lambda: sys.exit()),
        ])
        self.setContextMenu(self.menu)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logger.info("RandPicker 启动。")
    widget = Widget()
    widget.show()
    widget.raise_()

    app.setQuitOnLastWindowClosed(False)

    sys.exit(app.exec())
