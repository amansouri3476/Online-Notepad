import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import notelyConnection
import output  # put testUI.py in the same dir as this code
from notelyClasses import NotelyNote, NotelyFolder
from functools import partial

reminderIsSet = False
category_type = 'Uncategorized'
reminder_dateTime = None
deckName = None

scrollareabuttons_decks = []
scrollareabuttons_2_noteNames = []

# noinspection PyPep8Naming
class TestWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(TestWindow, self).__init__()
        self.ui = output.Ui_MainWindow()  # in this and next line you say that you will use all widgets from testUI
        # over self.ui
        self.ui.setupUi(self)
        # so, when you say self.ui.myButton ,that is pushButton in testUI that has name myButton
        # ################################################################################################## #
        self.ui.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
        self.ui.scrollAreaWidgetContents_2.setLayout(QtWidgets.QVBoxLayout())

        # Connections for buttons

        # Edit and Update buttons being hide
        self.ui.page_newnote_edit_button.hide()
        self.ui.page_newnote_update_button.hide()

        # Back Buttons
        self.ui.back_login_page.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.back_register_page.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.back_newnote_page.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        # self.ui.back_deck_page.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        # self.ui.back_show_note_page.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5))

        # Login/Signup page connections
        self.ui.login_button.clicked.connect(self.open_login_page)
        self.ui.signup_button.clicked.connect(self.open_signup_page)
        self.ui.sign_in_button.clicked.connect(self.authenticate)
        self.ui.register_button.clicked.connect(self.register)

        # Main menu page connections
        self.ui.view_deck_button.clicked.connect(self.view_decks)
        self.ui.new_deck_create_button.clicked.connect(self.popup_deck_name_entry)
        self.ui.create_deck_done_button.clicked.connect(self.add_new_deck)
        self.ui.instant_note_create_button.clicked.connect(self.create_new_note)
        self.ui.view_uncategorized_notes_button.clicked.connect(self.view_uncategorized_deck)

        # Creat/Edit New Note page connections
        self.ui.page_newnote_save_button.clicked.connect(self.save_note)
        self.ui.page_newnote_reminder_button.clicked.connect(self.setup_reminder)
        self.ui.dateTime_edit_done_button.clicked.connect(self.set_reminder)

        self.ui.logout_button.clicked.connect(self.logout)
        self.ui.quit_button.clicked.connect(self.exit)

    def exit(self):
        sys.exit()

    def logout(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        notelyConnection.logout_user()

    def open_login_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def open_signup_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def open_mainMenu_page(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.new_deck_name_label.hide()
        self.ui.new_deck_name_textEdit.hide()
        self.ui.create_deck_done_button.hide()

    def authenticate(self):
        username = self.ui.username_text.toPlainText()
        password = self.ui.password_text.toPlainText()
        print(self.ui.username_text.toPlainText())
        print(self.ui.password_text.toPlainText())
        # API
        t, message, code = notelyConnection.login_user(username, password)
        if not t:
            sys.exit()
        else:
            self.open_mainMenu_page()

    def register(self):
        print(self.ui.username_text_register.toPlainText())
        print(self.ui.password_text_register.toPlainText())
        name = self.ui.name_text_register.toPlainText()
        lastname = self.ui.lastname_text_register.toPlainText()
        email = self.ui.email_text_register.toPlainText()
        username = self.ui.username_text_register.toPlainText()
        password = self.ui.password_text_register.toPlainText()
        print(name, lastname, email, username, password)
        # API
        t, message, code = notelyConnection.signup_user(username, password, email, name, lastname)
        if not t:
            sys.exit()
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

    def create_new_note(self, category):
        global category_type
        if category:
            category_type = category
        else:
            category_type = 'Uncategorized'
        self.ui.stackedWidget.setCurrentIndex(4)
        self.ui.reminder_dateTime_edit.hide()
        self.ui.dateTime_edit_done_button.hide()

    def setup_reminder(self):
        self.ui.reminder_dateTime_edit.show()
        self.ui.dateTime_edit_done_button.show()

    def set_reminder(self):
        global reminder_dateTime
        global reminderIsSet
        reminderIsSet = True
        reminder_dateTime = self.ui.reminder_dateTime_edit.dateTime().toPyDateTime()
        self.ui.reminder_dateTime_edit.hide()
        self.ui.dateTime_edit_done_button.hide()

    def view_decks(self):
        global scrollareabuttons_2_noteNames
        global scrollareabuttons_decks
        if len(scrollareabuttons_2_noteNames):
            for button in scrollareabuttons_2_noteNames:
                button.deleteLater()
            scrollareabuttons_2_noteNames = []
        if len(scrollareabuttons_decks):
            for button in scrollareabuttons_decks:
                button.deleteLater()
            scrollareabuttons_decks = []
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.label.setText('My Decks')
        # successful,message,htmlcode = api_view_deck()
        successful, message, code = notelyConnection.get_folder_list_user()
        if successful:
            print(message)
            if not message:
                print('no decks available')
            else:
                for category in message:
                    print(category)
                    palette = QtGui.QPalette()
                    font = QtGui.QFont()
                    font.setFamily("Edwardian Script ITC")
                    font.setPointSize(24)
                    self.ui.button = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
                    self.ui.button.setFont(font)
                    # self.ui.button.setGeometry(QtCore.QRect(750, 160 + 150 * message.index(category), 241, 121))
                    self.ui.button.setGeometry(QtCore.QRect(50, 20 + 140 * message.index(category), 241, 121))
                    self.ui.button.setPalette(palette)
                    self.ui.button.setStyleSheet("background-color: rgb(0, 0, 0, 0);")
                    self.ui.button.setObjectName(category)
                    _translate = QtCore.QCoreApplication.translate
                    self.ui.button.show()
                    self.ui.button.setText(_translate("MainWindow", category))
                    scrollareabuttons_decks.append(self.ui.button)
                    self.ui.button.clicked.connect(partial(self.show_category_notes, category))
                self.ui.scrollAreaWidgetContents.setMinimumHeight(20 + 140 * len(message))

            print('##########################################################')

            self.ui.back_deck_page.clicked.connect(partial(self.deck_page_back))

    def deck_page_back(self):
        self.ui.stackedWidget.setCurrentIndex(3)

        self.ui.back_deck_page.disconnect()

    def view_uncategorized_deck(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        global scrollareabuttons_2_noteNames
        global scrollareabuttons_decks
        if len(scrollareabuttons_2_noteNames):
            for button in scrollareabuttons_2_noteNames:
                button.deleteLater()
            scrollareabuttons_2_noteNames = []
        if len(scrollareabuttons_decks):
            for button in scrollareabuttons_decks:
                button.deleteLater()
            scrollareabuttons_decks = []
        # successful,message,htmlcode = api_view_deck()
        self.ui.label.setText('Previous Notes')
        successful, message, code = notelyConnection.get_folder_content_user('Uncategorized')
        if successful:
            print(message.list_notes)
            if not message.list_notes:
                print('no uncategotized notes available')
            else:
                for note_name in message.list_notes:
                    print(note_name)
                    palette = QtGui.QPalette()
                    font = QtGui.QFont()
                    font.setFamily("Edwardian Script ITC")
                    font.setPointSize(24)
                    self.ui.button = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
                    self.ui.button.setFont(font)
                    # self.ui.button.setGeometry(QtCore.QRect(750, 160 + 150 * message.list_notes.index(note), 241, 121))
                    self.ui.button.setGeometry(QtCore.QRect(50, 20 + 140 * message.list_notes.index(note_name), 241, 121))
                    self.ui.button.setPalette(palette)
                    self.ui.button.setStyleSheet("background-color: rgb(0, 0, 0, 0);")
                    self.ui.button.setObjectName(note_name)
                    _translate = QtCore.QCoreApplication.translate
                    self.ui.button.show()
                    self.ui.button.setText(_translate("MainWindow", note_name))
                    scrollareabuttons_decks.append(self.ui.button)
                    true, note, code = notelyConnection.get_note_user(note_name, 'Uncategorized')
                    self.ui.button.clicked.connect(partial(self.show_note, note.name, note.data, 'Uncategorized'))

                self.ui.scrollAreaWidgetContents.setMinimumHeight(20 + 140 * len(message.list_notes))

            print('##########################################################')
            print(message.list_notes)

            self.ui.back_deck_page.clicked.connect(self.deck_page_back)

    def delete_deck_notes(self, category):
        notelyConnection.delete_folder_user(category)
        self.view_decks()

    def show_category_notes(self, category_name):
        self.ui.page_newnote_newnote_button.show()
        global category_type
        global scrollareabuttons_2_noteNames
        if len(scrollareabuttons_2_noteNames):
            for button in scrollareabuttons_2_noteNames:
                button.deleteLater()
            scrollareabuttons_2_noteNames = []

        category_type = category_name
        print("show_category_notes successfully started")
        print(category_name)
        self.ui.stackedWidget.setCurrentIndex(7)
        self.ui.label_2.setText(category_name)
        self.ui.page_newnote_shownote_textedit.hide()
        # palette = QtGui.QPalette()
        # font = QtGui.QFont()
        # font.setFamily("Edwardian Script ITC")
        # font.setPointSize(54)
        # self.ui.categoryLabel = QtWidgets.QLabel(self.ui.page_6)
        # self.ui.categoryLabel.setFont(font)
        # self.ui.categoryLabel.setGeometry(QtCore.QRect(230, 90, 400, 200))
        # self.ui.categoryLabel.setPalette(palette)
        # self.ui.categoryLabel.setStyleSheet("background-color: rgb(0, 0, 0, 0);")
        # self.ui.categoryLabel.setObjectName(category_name)
        # _translate = QtCore.QCoreApplication.translate
        # self.ui.categoryLabel.show()
        # self.ui.categoryLabel.setText(_translate("MainWindow", category_name))

        # New Note button
        self.ui.page_newnote_newnote_button.clicked.connect(partial(self.create_new_note, category_name))
        # Delete Note button
        self.ui.page_newnote_delete_button_2.disconnect()
        self.ui.page_newnote_delete_button_2.clicked.connect(partial(self.delete_deck_notes, category_name))

        successful, message, code = notelyConnection.get_folder_content_user(category_name)
        print("liiiiiiiiist")
        print(message.list_notes)
        if successful:
            for noteName in message.list_notes:
                print(noteName)
                # button = QtWidgets.QPushButton(category)
                palette = QtGui.QPalette()
                font = QtGui.QFont()
                font.setFamily("Edwardian Script ITC")
                font.setPointSize(24)
                self.ui.button = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents_2)
                self.ui.button.setFont(font)
                # self.ui.button.setGeometry(QtCore.QRect(760, 160 + 120 * message.list_notes.index(noteName), 241, 121))
                self.ui.button.setGeometry(QtCore.QRect(70, 20 + 140 * message.list_notes.index(noteName), 241, 121))
                self.ui.button.setPalette(palette)
                self.ui.button.setStyleSheet("background-color: rgb(0, 0, 0, 0);")
                self.ui.button.setObjectName(noteName)
                self.ui.button.show()
                _translate = QtCore.QCoreApplication.translate
                self.ui.button.setText(_translate("MainWindow", noteName))
                scrollareabuttons_2_noteNames.append(self.ui.button)
                succ, note, code = notelyConnection.get_note_user(noteName, category_name)
                self.ui.button.clicked.connect(partial(self.show_note, noteName, note.data, category_name))

            self.ui.scrollAreaWidgetContents_2.setMinimumHeight(20 + 140 * len(message.list_notes))
            self.ui.back_show_note_page.clicked.connect(partial(self.show_notes_page_back))

    def show_notes_page_back(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.label.setText('My Decks')
        global scrollareabuttons_2_noteNames
        if len(scrollareabuttons_2_noteNames):
            for button in scrollareabuttons_2_noteNames:
                button.deleteLater()
            scrollareabuttons_2_noteNames = []
        self.ui.back_show_note_page.disconnect()

    def show_note(self, noteName, noteContent, category):
        global scrollareabuttons_2_noteNames
        if len(scrollareabuttons_2_noteNames):
            for button in scrollareabuttons_2_noteNames:
                button.deleteLater()
            scrollareabuttons_2_noteNames = []
        self.ui.stackedWidget.setCurrentIndex(7)
        self.ui.label_2.setText(noteName)
        print("clicked")
        self.ui.page_newnote_shownote_textedit.insertPlainText(noteContent)
        self.ui.page_newnote_shownote_textedit.setDisabled(True)
        self.ui.page_newnote_shownote_textedit.show()

        self.ui.page_newnote_newnote_button.hide()
        self.ui.page_newnote_edit_button.show()

        self.ui.reminder_dateTime_edit.hide()
        self.ui.dateTime_edit_done_button.hide()

        # Edit Button connection
        self.ui.page_newnote_edit_button.clicked.connect(partial(self.edit_note, noteName, category))

        # Delete Note button
        self.ui.page_newnote_delete_button_2.disconnect()
        self.ui.page_newnote_delete_button_2.clicked.connect(partial(self.delete_note, category, noteName))

        # Back Button
        self.ui.back_show_note_page.disconnect()
        if category == 'Uncategorized':
            self.ui.back_show_note_page.clicked.connect(partial(self.view_uncategorized_deck))
            self.ui.back_deck_page.disconnect()

        else:
            self.ui.back_show_note_page.clicked.connect(partial(self.show_category_notes, category))

    def edit_note(self, noteName, category):
        self.ui.page_newnote_shownote_textedit.setDisabled(False)
        # self.ui.page_newnote_note_textedit.hide()
        self.ui.page_newnote_edit_button.hide()
        self.ui.page_newnote_update_button.show()

        # Old note notelyNote
        true, oldNotelyNote, code = notelyConnection.get_note_user(noteName, category)

        # Update Button connection
        self.ui.page_newnote_update_button.clicked.connect(partial(self.update_note, noteName, category, oldNotelyNote))

    def update_note(self, noteName, category, oldNotelyNote):
        newNotelyNote = NotelyNote(noteName, category, self.ui.page_newnote_shownote_textedit.toPlainText(),
                                   oldNotelyNote.reminder)
        notelyConnection.update_note_user(newNotelyNote, oldNotelyNote)

        self.ui.page_newnote_update_button.hide()
        self.ui.page_newnote_newnote_button.show()
        self.ui.page_newnote_delete_button_2.show()
        self.show_category_notes(category)

        self.ui.page_newnote_shownote_textedit.clear()

    def delete_note(self, category, noteName):
        notelyConnection.delete_note_user(noteName, category)
        self.show_category_notes(category)

    def save_note(self):
        global category_type, reminder_dateTime, reminderIsSet
        print('hello')
        name = self.ui.note_name_text_edit.toPlainText()
        content = self.ui.page_newnote_note_textedit.toPlainText()
        print(name, '\t' + content)
        print(reminderIsSet)
        if reminderIsSet:
            print('There is a reminder')
            notelyNote = NotelyNote(name, category_type, content, reminder_dateTime)
            notelyConnection.add_note_user(notelyNote)
            print(notelyNote.folder_name)
            category_type = 'Uncategorized'
            print(notelyNote.folder_name)
            reminderIsSet = False
            self.open_mainMenu_page()

            # Clearance of textEdit
            self.ui.note_name_text_edit.clear()
            self.ui.page_newnote_note_textedit.clear()

        else:
            print('no reminder')
            notelyNote = NotelyNote(name, category_type, content)
            notelyConnection.add_note_user(notelyNote)
            category_type = 'Uncategorized'
            reminder_dateTime = None
            self.open_mainMenu_page()

            # Clearance of textEdit
            self.ui.note_name_text_edit.clear()
            self.ui.page_newnote_note_textedit.clear()

    def popup_deck_name_entry(self):
        self.ui.new_deck_name_label.show()
        self.ui.new_deck_name_textEdit.show()
        self.ui.create_deck_done_button.show()

        self.ui.new_deck_name_textEdit.clear()

    def add_new_deck(self):
        deckName = self.ui.new_deck_name_textEdit.toPlainText()
        noteFolder = NotelyFolder(deckName, [])
        notelyConnection.add_folder_user(noteFolder)

        self.ui.new_deck_name_label.hide()
        self.ui.new_deck_name_textEdit.hide()
        self.ui.create_deck_done_button.hide()

        self.view_decks()


if __name__ == '__main__':
    notelyConnection.initialize()
    app = QtWidgets.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())
