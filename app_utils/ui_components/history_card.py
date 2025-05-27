from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import CardWidget, IconWidget, BodyLabel, CaptionLabel, FluentIcon as fIcon

class HistoryCard(CardWidget):
    def __init__(self, mode: int, student: dict, time: datetime, parent=None):
        super().__init__(parent=parent)
        self.mode = mode
        self.student = student
        self.time = time
        self.parent = parent

        self.iconWidget = IconWidget(fIcon.ROBOT if mode == 0 else fIcon.PEOPLE, self)
        self.titleLabel = BodyLabel(
            f"{self.student['name']} {self.student['id']}", self
        )
        self.contentLabel = CaptionLabel(str(self.time), self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(32, 32)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)
