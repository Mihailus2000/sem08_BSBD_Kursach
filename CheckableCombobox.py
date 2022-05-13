from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox

class CheckableComboBox(QComboBox):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._changed = False
        self.view().pressed.connect(self.handleItemPressed)

    def setItemChecked(self, index, checked=False):
        item = self.model().item(index, self.modelColumn())  # QStandardItem object

        if checked:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)

        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self._changed = True

    def hidePopup(self):
        if not self._changed:
            super().hidePopup()
        self._changed = False

    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == Qt.Checked

    def resetBox(self):
        for indx in range(self.count()):
            item = self.model().item(indx, self.modelColumn())  # QStandardItem object
            item.setCheckState(Qt.Unchecked)

    def anyIsChecked(self):
        for indx in range(self.count()):
            item = self.model().item(indx, self.modelColumn())  # QStandardItem object
            if item.checkState() == Qt.Checked:
                return True

    def getBooleanArray(self):
        arr = []
        for indx in range(self.count()):
            item = self.model().item(indx, self.modelColumn())  # QStandardItem object
            if item.checkState() == Qt.Checked:
                arr.append(True)
            else:
                arr.append(False)
        return arr
