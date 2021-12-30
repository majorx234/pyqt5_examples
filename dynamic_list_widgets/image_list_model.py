from PyQt5.QtCore import Qt, QAbstractListModel

class ImageListModel(QAbstractListModel):
    def __init__(self, *args):
        super().__init__(*args)
        self.list = []

    def rowCount(self, parent=None, *args, **kwargs):
        if parent:
            return len(self.list)

    def data(self, index, role=None):
        return self.list[index.row()]

    def append(self, item):
        item.data_changed.connect(self.data_changed)
        self.list.append(item)
        new_index = self.createIndex(len(self.list), 0, item)
        self.dataChanged.emit(new_index, new_index, [Qt.EditRole])

    def pop(self, index):
        item = self.list.pop(index)
        i = min(index, len(self.list) - 1)
        new_index = self.createIndex(i, 0, self.list[i])
        self.dataChanged.emit(new_index, new_index, [Qt.EditRole])

    def get_last_item(self):
        # todo: tsten ob es überhaupt ein letztes Bild gibt
        index = len(self.list)-1
        last_item = self.list[index]
        # todo: hier eine Kopie erstellen
        return last_item 

    def clear(self):
        self.list = []

    def is_empty(self):
        return len(self.list)

    def data_changed(self, item):
        model_index = self.createIndex(self.list.index(item), 0, item)
        self.setData(model_index, item)

    def setData(self, model_index, data, role=Qt.EditRole):
        super().setData(model_index, data, role=role)
        self.dataChanged.emit(model_index, model_index, [role])    

