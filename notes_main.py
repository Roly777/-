#начни тут создавать приложение с умными заметками
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QListWidget,QTextEdit,QLineEdit,QLabel
from PyQt5.QtCore import Qt
import pickle

class DataBase():
    def __init__(self,filename):
        self.filename = filename +".bin"
        self.data = {}
        try:
            self.open()
        except FileNotFoundError:
            self.save()
    def open(self):
        with open(self.filename,mode="rb") as file:
            self.data = pickle.load(file)
    def save(self):
        with open(self.filename,mode="wb") as file:
            pickle.dump(self.data,file)
    def add_data(self,note_name,note_text,note_tags):
        self.data[note_name] = [note_text,note_tags]
        self.save()
    def remove_data(self,note_name):
        if note_name not in self.data:
            return
        del self.data[note_name]
        self.save()

class Selection():
    def __init__(self):
        self.current_note = None
        self.current_tag = None

selection = Selection()

base = DataBase("data")

app = QApplication([])

screen = QWidget()
screen.setWindowTitle("Умные заметки")
screen.resize(800,600)
screen.show()

mainline = QHBoxLayout()
first_line = QVBoxLayout()
second_line = QVBoxLayout()
third_line = QHBoxLayout()
fourth_line = QHBoxLayout()
screen.setLayout(mainline)

mainline.addLayout(first_line)
mainline.addLayout(second_line)

note_name = QLineEdit()
note_name.setPlaceholderText("Введите название заметки...")

tag_name = QLineEdit()
tag_name.setPlaceholderText("Введите тег...")

large_field = QTextEdit()
large_field.setPlaceholderText("Введите текст")

note_label = QLabel("Список заметок")
note_field = QListWidget()

tag_label = QLabel("Список тегов")
tag_field = QListWidget()

create_note = QPushButton("Создать заметку")
delete_note = QPushButton("Удалить заметку")
save_note = QPushButton("Сохранить заметку")

add_to_note = QPushButton("Добавить к заметке")
remove_from_note = QPushButton("Открепить от заметки")

find_note = QPushButton("Искать заметки по тегу")

third_line.addWidget(create_note)
third_line.addWidget(delete_note)

fourth_line.addWidget(add_to_note)
fourth_line.addWidget(remove_from_note)

first_line.addWidget(note_name)
first_line.addWidget(large_field)
second_line.addWidget(note_label)
second_line.addWidget(note_field)
second_line.addLayout(third_line)
second_line.addWidget(save_note)
second_line.addWidget(tag_label)
second_line.addWidget(tag_field)
second_line.addWidget(tag_name)
second_line.addLayout(fourth_line)
second_line.addWidget(find_note)

def update_note_list(tag=None):
    note_field.clear()
    for notename in base.data:
        if tag == None:
            note_field.addItem(notename)
        else:
            if tag in base.data[notename][1]:
                note_field.addItem(notename)

def update_tag_list():
    tag_field.clear()
    tags = []
    for k,v in base.data.items():
        for tag1 in v[1]:
            if tag1 in tags:
                continue
            else:
                tags.append(tag1)
    for tag2 in tags:
        tag_field.addItem(tag2)

update_note_list()
update_tag_list()

def create_note_f():
    name = note_name.text()
    text = large_field.toPlainText()
    tags = tag_name.text().replace(",","").split()
    base.add_data(name,text,tags)
    update_note_list()

def delete_note_f():
    name = selection.current_note
    if name == None:
        return
    base.remove_data(name)
    update_note_list()

def save_note_f():
    if selection.current_note == None:
        create_note_f()
    else:
        temp_name = selection.current_note
        temp_text = base.data[temp_name][0]
        temp_tags = base.data[temp_name][1]
        if temp_name != note_name.text():
            base.remove_data(temp_name)
        create_note_f()

def add_tag():
    if selection.current_note == None:
        return
    else:
        base.data[selection.current_note][1].append(tag_name.text())
        update_tag_list()

def remove_tag():
    if selection.current_note == None:
        return
    else:
        if tag_name.text() in base.data[selection.current_note][1]:
            base.data[selection.current_note][1].remove(tag_name.text())
        update_tag_list()

def find_note_f():
    for k,v in base.data.items():
        if selection.current_tag in v[1]:
            update_note_list(selection.current_tag)
            

def change_current_note(item):
    selection.current_note = item.text()
    note_name.setText(selection.current_note)
    large_field.setText(base.data[selection.current_note][0])
    tag_name.setText(", ".join(base.data[selection.current_note][1]))
    update_note_list()
    selection.current_tag = None
def change_current_tag(item):
    selection.current_tag = item.text()
    tag_name.setText(item.text())


note_field.itemClicked.connect(change_current_note)
tag_field.itemClicked.connect(change_current_tag)

create_note.clicked.connect(create_note_f)
delete_note.clicked.connect(delete_note_f)
save_note.clicked.connect(save_note_f)

add_to_note.clicked.connect(add_tag)
remove_from_note.clicked.connect(remove_tag)
find_note.clicked.connect(find_note_f)

app.exec_()