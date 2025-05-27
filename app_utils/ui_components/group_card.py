from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QListWidget, QAbstractItemView
from qfluentwidgets import CardWidget, SubtitleLabel, TransparentDropDownToolButton, RoundMenu, Action, FluentIcon as fIcon, ListWidget
import conf
from .group_edit_box import GroupEditBox

class GroupCard(CardWidget):  # 分组卡片
    """
    一个表示学生分组的小部件，包含标题、学生列表和管理选项。

    该类继承自 `CardWidget`，提供了一个用于管理学生分组的用户界面。它包括一个标题、学生姓名列表以及一个菜单，
    菜单中包含编辑分组、删除分组和撤销删除的操作。该小部件设计用于需要管理学生分组的大型应用程序中。

    :param title: 分组名称，默认为 '所有学生'。
    :type title: str
    :param students: 分组内的学生姓名列表，默认为 ['未知学生']。
    :type students: list
    :param parent: 父窗口部件，默认为 None。
    :type parent: QWidget | None
    :param is_global: 是否是全局分组（所有学生），默认为 True。
    :type is_global: bool
    """

    def __init__(
        self,
        title: str = "所有学生",
        students: list = None,
        parent: QWidget | None = None,
        is_global: bool = True,
    ):
        super().__init__(parent)
        if students is None:
            students = ["未知学生"]
        self.exist_students = students
        self.title = title
        self.parent = parent
        self.isDeleted = False

        self.setMinimumHeight(250)

        self.titleLabel = SubtitleLabel(title, self)
        self.moreButton = TransparentDropDownToolButton(fIcon.MORE, self)
        self.moreMenu = RoundMenu(parent=self.moreButton)
        self.stuList = ListWidget(self)

        self.hBoxLayout_Title = QHBoxLayout()
        self.vBoxLayout = QVBoxLayout(self)

        if is_global:
            self.moreButton.setEnabled(False)

        self.action_del = Action(
            fIcon.DELETE, f"删除分组 {title}", triggered=lambda: self.del_group()
        )
        self.action_undo_del = Action(
            fIcon.CANCEL,
            f"撤销删除分组 {title}",
            triggered=lambda: self.undo_del_group(),
        )
        self.action_undo_del.setEnabled(False)

        self.moreMenu.addActions(
            [
                Action(
                    fIcon.EDIT, "添加或删除学生", triggered=lambda: self.set_group()
                ),
                self.action_del,
                self.action_undo_del,
            ]
        )
        self.moreButton.setMenu(self.moreMenu)

        self.stuList.addItems(students)
        self.stuList.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.stuList.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # 内容
        self.vBoxLayout.setContentsMargins(6, 6, 6, 6)
        self.vBoxLayout.setSpacing(3)
        self.vBoxLayout.addLayout(self.hBoxLayout_Title)
        self.vBoxLayout.addWidget(self.stuList)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # 标题栏
        self.hBoxLayout_Title.setSpacing(12)
        self.hBoxLayout_Title.setContentsMargins(12, 8, 12, 6)
        # self.hBoxLayout_Title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout_Title.addWidget(
            self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter
        )
        self.hBoxLayout_Title.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

    def set_group(self):
        students = conf.stu.get_all_name()
        stu_count = self.stuList.count()
        self.exist_students = []
        for i in range(stu_count):
            item = self.stuList.item(i)
            self.exist_students.append(item.text())
        w = GroupEditBox(
            parent=self.parent,
            name=self.title,
            students=students,
            exist_students=self.exist_students,
            target=self,
        )
        w.exec()

    def del_group(self):
        self.action_del.setEnabled(False)
        self.action_undo_del.setEnabled(True)

        self.titleLabel.setText(self.title + " (删除)")
        self.isDeleted = True

    def undo_del_group(self):
        self.action_del.setEnabled(True)
        self.action_undo_del.setEnabled(False)

        self.titleLabel.setText(self.title)
        self.isDeleted = False
