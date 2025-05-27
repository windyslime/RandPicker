from PyQt6.QtWidgets import QWidget, QButtonGroup, QListWidgetItem, QAbstractItemView
from qfluentwidgets import MessageBoxBase, SubtitleLabel, RadioButton, ListWidget, CheckBox
import conf

class GroupEnablePolicyBox(MessageBoxBase):
    """
    编辑分组启用。

    """

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.titleLabel = SubtitleLabel(text="编辑分组策略")

        self.btn_global = RadioButton(text="所有学生")
        self.btn_group = RadioButton(text="分组")

        self.group_btn_global = QButtonGroup()
        self.group_btn_global.addButton(self.btn_global, 0)
        self.group_btn_global.addButton(self.btn_group, 1)

        if conf.ini.get("Group", "global") == "true":
            self.btn_global.setChecked(True)
        else:
            self.btn_group.setChecked(True)

        self.yesButton.clicked.connect(lambda: self.save())

        self.groupList = ListWidget()
        self.groupList.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        enabled_group = conf.ini.get("Group", "group").split(", ")

        for group_num in range(len(conf.group.get_all())):
            group = conf.group.get_single(group_num)

            checkbox = CheckBox(text=group["name"])  # 创建复选框
            if enabled_group is None:
                checkbox.setChecked(False)
            elif str(group_num) in enabled_group:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

            list_item = QListWidgetItem()  # 创建列表项

            # 将复选框与列表项关联起来
            self.groupList.addItem(list_item)
            self.groupList.setItemWidget(list_item, checkbox)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.btn_global)
        self.viewLayout.addWidget(self.btn_group)
        self.viewLayout.addWidget(self.groupList)

    def save(self):
        count = self.groupList.count()
        enable_group = []
        for group in range(count):
            item = self.groupList.item(group)
            if item is None:
                continue
            widget = self.groupList.itemWidget(item)
            if not isinstance(widget, CheckBox):
                return
            if widget.isChecked():
                enable_group.append(group)

        conf.ini.write(
            "Group",
            "global",
            str(self.btn_global.isChecked()),
            "Group",
            "group",
            str(enable_group).replace("[", "").replace("]", ""),
        )
