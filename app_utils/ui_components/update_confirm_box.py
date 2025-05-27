from PyQt6.QtWidgets import QWidget
from qfluentwidgets import MessageBoxBase, TitleLabel, BodyLabel
import update # Make sure this import works, or adjust path if 'update.py' is not in root

class UpdateConfirmBox(MessageBoxBase):
    """
    更新确认框。

    :param parent: 父控件。
    :type parent: QWidget | None
    :param title: 标题。
    :type title: str
    :param content: 内容。
    :type content: str
    :param target: 目标控件。
    :type target: QWidget | None

    :raises: None

    :returns: None
    """

    def __init__(self, parent=None, app: bool = False):
        super().__init__(parent)
        self.app = app
        if self.app:
            self.title = "确实要更新 RandPicker？"
            self.content = (
                "将使用 RandPicker 更新助理更新 RandPicker。\n"
                "RandPicker 将会退出。请在操作前保存您的更改。\n"
                "如果更新助理没有打开，请先更新它。"
            )
        else:
            self.title = "确实要更新 RandPicker 更新助理？"
            self.content = (
                "将更新 RandPicker 更新助理。\n"
                "RandPicker 不会被关闭，但会暂时停止响应。正常情况下，停止响应不会超过 40 秒。\n"
                "如果停止响应的时间过长，请检查您的网络环境。"
            )

        self.titleLabel = TitleLabel(self.title, self)
        self.contentLabel = BodyLabel(self.content, self)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.contentLabel)

        self.yesButton.clicked.connect(self.update)

    def update(self):
        self.yesButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        if self.app:
            update.update_app()
        else:
            update.update_updater(parent=self)
        self.close()
