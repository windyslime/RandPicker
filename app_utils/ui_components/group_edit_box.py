from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QAbstractItemView, QGridLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, StrongBodyLabel, LineEdit, CaptionLabel, CheckBox, ListWidget
import conf
from .group_card import GroupCard # Added import for GroupCard
from loguru import logger

class GroupEditBox(MessageBoxBase):
    """
    编辑分组。

    :param parent: 父控件。
    :type parent: QWidget | None
    :param new: 是否是新建分组。
    :type new: bool
    :param name: 分组现在的名称 (修改分组)。
    :type name: str | None
    :param students: 所有学生的列表。
    :type students: list
    :param exist_students: 已在分组中的学生 (修改分组)。
    :type exist_students: list | None
    :param target: 要修改的布局或控件。新建分组需要 QGridLayout，修改分组需要 GroupCard。
    :type target: QWidget | None

    :raises: None

    :returns: None
    """

    def __init__(
        self,
        parent=None,
        new: bool = False,
        name: str = None,
        students: list = None,
        exist_students: list = None,
        target: QWidget | None = None,
    ):
        super().__init__(parent)
        self.target = target
        self.parent = parent
        self.name = name
        self.titleLabel = SubtitleLabel(
            text=f"{'添加' if new else '修改'}分组{' ' + name if name else ''}"
        )
        self.subtitleLabel_name = StrongBodyLabel(text="分组名称")
        self.nameLineEdit = LineEdit()
        self.captionLabel_name = CaptionLabel(text="名称不能为空。")
        self.subtitleLabel_stu = StrongBodyLabel(text="学生")
        self.stuList = ListWidget()

        self.nameLineEdit.setPlaceholderText("分组名称")
        if name:
            self.nameLineEdit.setText(name)

        self.stuList.setMinimumHeight(200)
        self.stuList.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.stuList.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        for student in students:
            checkbox = CheckBox(text=student)  # 创建复选框
            if exist_students is None:
                checkbox.setChecked(False)
            elif student in exist_students:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
            list_item = QListWidgetItem()  # 创建列表项

            # 将复选框与列表项关联起来
            self.stuList.addItem(list_item)
            self.stuList.setItemWidget(list_item, checkbox)

        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.subtitleLabel_name)
        self.viewLayout.addWidget(self.nameLineEdit)
        self.viewLayout.addWidget(self.captionLabel_name)
        self.viewLayout.addWidget(self.subtitleLabel_stu)
        self.viewLayout.addWidget(self.stuList)

        # 设置确认按钮操作
        self.yesButton.clicked.connect(lambda: self.save())

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(350)

    def save(self):
        if self.validate():
            stu = []
            stu_count = self.stuList.count()
            name = self.nameLineEdit.text()
            for i in range(stu_count):
                item = self.stuList.itemWidget(self.stuList.item(i))
                if item.isChecked():
                    stu.append(item.text())

            if isinstance(self.target, GroupCard):
                self.target.titleLabel.setText(name)
                self.target.stuList.clear()
                self.target.stuList.addItems(stu)

                logger.success(f"修改了分组 {self.name} -> {name} 的信息。")
            elif isinstance(self.target, QGridLayout):
                card = GroupCard(
                    title=name, students=stu, is_global=False, parent=self.parent
                )
                row = self.target.rowCount() - 1
                students = conf.stu.get_all_name()
                global_card = GroupCard(students=students) # Assuming GroupCard can be instantiated like this
                for column in range(1, 3):
                    if not self.target.itemAtPosition(row, column):
                        self.target.addWidget(card, row, column, 1, 1)
                        self.target.addWidget(
                            global_card, 0, 0, 1, self.target.columnCount()
                        )
                        logger.success(f"添加了新分组 {name}。")
                        return
                self.target.addWidget(card, row + 1, 0, 1, 1)
                self.target.addWidget(global_card, 0, 0, 1, self.target.columnCount())
                logger.success(f"添加了新分组 {name}。")
            else:
                return

    def validate(self) -> bool:
        if self.nameLineEdit.text() != "" and not self.nameLineEdit.text().isspace():
            return True
        self.captionLabel_name.setTextColor(QColor(255, 0, 0))
        return False
