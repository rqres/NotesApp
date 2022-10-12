import os
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

notes = []
current_note_index = 0


class Note:
    def __init__(self, is_new=True, filename=''):
        if is_new:
            global current_note_index
            current_note_index += 1
            self.file_path = 'notes/note' + str(current_note_index)
            self.date_added = datetime.now()
            self.id = current_note_index
        else:
            self.file_path = 'notes/' + filename
            self.date_added = os.path.getmtime(filename=self.file_path)
            self.id = int(filename.replace('note', ''))

        notes.append(self)

    @staticmethod
    def find_note_files():
        last_file_index = 0
        if not os.path.isdir('notes'):
            os.mkdir('notes')

        for file in os.listdir('notes/'):
            Note(is_new=False, filename=file)
            index = int(file.replace('note', ''))
            if index > last_file_index:
                last_file_index = index

        return last_file_index

    @staticmethod
    def get_note_object_by_id(index):
        for note in notes:
            if note.id == index:
                return note
        return None

    @staticmethod
    def find_note_label_by_text(lst, text):
        for item in lst:
            if item.text == text:
                return item

        return None


class MyTestApp(App):
    def __init__(self):
        super().__init__()
        self.text_input = TextInput()
        self.list_of_notes_box = BoxLayout(orientation="vertical", size_hint=(.3, 1))
        print(current_note_index)
        self.current_note = Note.get_note_object_by_id(current_note_index)
        if self.current_note is not None:
            with open(self.current_note.file_path, 'r') as f:
                self.text_input.text = f.read()
                f.close()

    def build(self):
        main_layout = BoxLayout(orientation="vertical")

        menu_box = BoxLayout(spacing=30, size_hint=(1, .05))
        save_button = Button(text="Save", on_press=self.save_note)
        delete_button = Button(text="Delete", on_press=self.delete_note)
        sample_button1 = Button(text="New", on_press=self.create_new_note)
        sample_button2 = Button(text="sample")
        menu_box.add_widget(sample_button1)
        menu_box.add_widget(sample_button2)
        menu_box.add_widget(delete_button)
        menu_box.add_widget(save_button)

        split_layout = BoxLayout(spacing=10, size_hint=(1, .95))

        for note in notes:
            btn = Button(text=note.file_path, on_press=self.open_note)
            self.list_of_notes_box.add_widget(btn)
            # print(lb.text)

        # print("children" + str(self.list_of_notes_box.children[0].text))

        split_layout.add_widget(self.list_of_notes_box)
        split_layout.add_widget(self.text_input)

        main_layout.add_widget(menu_box)
        main_layout.add_widget(split_layout)

        return main_layout

    def save_note(self, instance):
        print(self.text_input.text)
        with open(self.current_note.file_path, 'w') as f:
            f.write(self.text_input.text)
            f.close()

    def create_new_note(self, instance):
        self.text_input.text = ''
        self.current_note = Note()
        try:
            with open(self.current_note.file_path, 'x') as f:
                print(self.current_note.file_path + ": new note created !")
                f.close()
            self.list_of_notes_box.add_widget(Button(text=self.current_note.file_path, on_press=self.open_note))
        except FileExistsError:
            print("This file already exists, cannot create new one")

    def delete_note(self, instance):
        global current_note_index
        target = 'notes/note' + str(current_note_index)
        if os.path.isfile(target):
            os.remove(target)
            notes.remove(Note.get_note_object_by_id(current_note_index))
            current_note_index -= 1
            self.current_note = Note.get_note_object_by_id(current_note_index)
            self.list_of_notes_box.remove_widget(Note.find_note_label_by_text(self.list_of_notes_box.children, target))
            if self.current_note is not None:
                with open(self.current_note.file_path, 'r') as f:
                    self.text_input.text = f.read()
                    f.close()
            else:
                self.text_input.text = ''
            print(target + " successfully deleted!")
        else:
            print("The file " + target + " does not exist")

    def open_note(self, instance):
        pass


if __name__ == '__main__':
    current_note_index = Note.find_note_files()
    MyTestApp().run()
