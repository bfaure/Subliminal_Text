import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class tab_t:
	def __init__(self):
		self.filename="untitled" # filename
		self.tab_idx=0 # index of tab in QTabWidget
		self.text_editor_widget=None # the QTextEdit
		self.layout=None # the QVBoxLayout
		self.q_widget=None # the QWidget (parent of layout)
		self.parent=None # the overall QTabWidget

class main_window(QWidget):

	def __init__(self,parent=None):
		super(main_window,self).__init__()
		self.parent = parent
		self.children = []

		self.init_vars()
		self.init_ui()

	def init_vars(self):
		self.current_font_size = 12
		self.width = 1000
		self.height = 1200

		self.tabs=[]
		self.current_tab_index=0 # index in self.tabs list

		self.current_tab_filename = "untitled"

	def init_ui(self):

		self.resize(self.width,self.height)
		self.setWindowTitle("untitled - Subliminal Text")

		self.toolbar = QMenuBar(self)
		self.toolbar.setMinimumWidth(self.width)

		self.file_menu = self.toolbar.addMenu("File")
		self.edit_menu = self.toolbar.addMenu("Edit")
		self.selection_menu = self.toolbar.addMenu("Selection")
		self.find_menu = self.toolbar.addMenu("Find")
		self.view_menu = self.toolbar.addMenu("View")
		self.goto_menu = self.toolbar.addMenu("Goto")
		self.tools_menu = self.toolbar.addMenu("Tools")
		self.project_menu = self.toolbar.addMenu("Project")
		self.preferences_menu = self.toolbar.addMenu("Preferences")
		self.help_menu = self.toolbar.addMenu("Help")

		self.init_file_menu()
		self.init_preferences_menu()

		##################

		self.main_layout = QVBoxLayout(self)
		self.main_layout.addSpacing(22)
		self.main_tab_widget = QTabWidget()
		self.main_tab_widget.currentChanged.connect(self.current_tab_changed)
		self.main_layout.addWidget(self.main_tab_widget)

		self.first_tab_parent = QWidget()
		self.first_tab_layout = QVBoxLayout(self.first_tab_parent)

		self.main_tab_widget.addTab(self.first_tab_parent,"untitled")
		self.main_tab_widget.setMovable(True)
		#self.main_tab_widget.setStyleSheet('QTabBar { font-size: 12pt; font-family: Consolas; }')

		self.first_text_editor = QTextEdit()
		self.first_text_editor.setStyleSheet("font: 12pt \"Consolas\";")
		self.first_tab_layout.addWidget(self.first_text_editor)

		first_tab = tab_t()
		first_tab.text_editor_widget=self.first_text_editor
		first_tab.layout=self.first_tab_layout
		first_tab.q_widget=self.first_tab_parent 
		first_tab.parent=self.main_tab_widget

		self.tabs.append(first_tab)
		self.current_tab_index=0

		##################

		self.show()

	def current_tab_changed(self):
		# fires when the user changes the current tab
		self.current_tab_index = self.main_tab_widget.currentIndex()
		print "Current tab: "+str(self.current_tab_index)

	def init_file_menu(self):
		# adds all the elems to the File toolbar menu
		self.new_action = self.file_menu.addAction("New File",
			self.new_file,QKeySequence("Ctrl+N"))
		self.open_action = self.file_menu.addAction("Open File...",
			self.open_file,QKeySequence("Ctrl+O"))
		self.save_action = self.file_menu.addAction("Save",
			self.save,QKeySequence("Ctrl+S"))
		self.save_as_action = self.file_menu.addAction("Save As...",
			self.save_as)
		self.file_menu.addSeparator()
		self.close_tab_action = self.file_menu.addAction("Close File",
			self.close_current_tab,QKeySequence("Ctrl+W"))

	def close_current_tab(self):
		# closes the current tab
		# need to check if the current tab is unsaved here

		# check if there is any tab open
		if self.current_tab_index>=0:
			self.main_tab_widget.removeTab(self.current_tab_index)
			del self.tabs[self.current_tab_index]
			self.current_tab_index+=-1

	def get_current_filename(self):
		# returns the filename of the current tab
		return self.tabs[self.current_tab_index].filename

	def open_file(self,filename="untitled"):
		if filename=="untitled": filename = QFileDialog.getOpenFileName(self,"Open file")
		if filename=="": return

		# if there is a real file in the current tab
		if self.get_current_filename()!="untitled": self.open_new_tab()

		# put the text in the tab
		text=open(filename,"r").read()
		cur_tab = self.get_current_tab()
		cur_tab.text_editor_widget.setText(text)
		cur_tab.filename=filename
		self.update_ui()

	def get_current_tab(self):
		# returns the current tab_t struct
		return self.tabs[self.current_tab_index]

	def open_new_tab(self):
		# opens a new tab & loads in text from 'filename'
		print "open new tab"
		new_tab_parent = QWidget()
		new_tab_layout = QVBoxLayout(new_tab_parent)
		self.main_tab_widget.addTab(new_tab_parent,"untitled")
		new_text_editor = QTextEdit()
		new_text_editor.setStyleSheet("font: 12pt \"Consolas\";")
		new_tab_layout.addWidget(new_text_editor)

		new_tab=tab_t() 
		new_tab.tab_idx=len(self.tabs)
		new_tab.text_editor_widget=new_text_editor
		new_tab.layout=new_tab_layout
		new_tab.q_widget=new_tab_parent 
		new_tab.parent=self.main_tab_widget

		self.tabs.append(new_tab)
		self.current_tab_index=len(self.tabs)-1
		self.main_tab_widget.setCurrentIndex(self.current_tab_index)

	def new_file(self):
		print("new file")

	def save(self):
		# saves the file in the current tab
		if self.get_current_filename()=="untitled":
			self.save_as()
		else:
			f = open(self.get_current_filename(),"w")
			f.write(self.get_current_tab_text())
			f.close()

	def get_current_tab_text(self):
		# returns the plaintext of the current tab
		current_text_editor = self.get_current_tab().text_editor_widget
		return current_text_editor.toPlainText()

	def save_as(self):
		filename = QFileDialog.getSaveFileName(self,"Save as...")
		if filename=="": return 

		current_tab=self.get_current_tab()
		current_tab.filename=filename

		f = open(filename,"w")
		f.write(self.get_current_tab_text())
		f.close()
		self.update_ui()

	def update_ui(self):
		# updates the window title and tab title with current file name
		self.setWindowTitle(self.get_current_filename()+" - Subliminal Text")
		cur_tab_idx = self.main_tab_widget.currentIndex()
		fname_pretty = self.get_current_filename().split("/")[-1]
		self.main_tab_widget.setTabText(cur_tab_idx,fname_pretty)

	def init_preferences_menu(self):
		# adds all the elems to the Preferences toolbar menu
		self.increase_font_action = self.preferences_menu.addAction("Increase Font Size",
			self.increase_font_size,QKeySequence("Ctrl+="))
		self.decrease_font_action = self.preferences_menu.addAction("Decrease Font Size",
			self.decrease_font_size,QKeySequence("Ctrl+-"))

	def increase_font_size(self):
		# increases the displayed font size
		self.current_font_size+=4
		current_text_editor=self.get_current_tab().text_editor_widget
		cursor = current_text_editor.textCursor()
		current_text_editor.selectAll()
		current_text_editor.setFontPointSize(self.current_font_size)
		current_text_editor.setTextCursor(cursor)

	def decrease_font_size(self):
		# decreases the displayed font size
		self.current_font_size+=-4
		if self.current_font_size<=2: self.current_font_size=2
		current_text_editor=self.get_current_tab().text_editor_widget
		cursor = current_text_editor.textCursor()
		current_text_editor.selectAll()
		current_text_editor.setFontPointSize(self.current_font_size)
		current_text_editor.setTextCursor(cursor)

	def resizeEvent(self,e):
		# resize the toolbar to fit the new window width
		self.toolbar.setFixedWidth(e.size().width())

def main():

	app = QApplication(sys.argv)
	app_window = main_window()
	sys.exit(app.exec_())	


if __name__ == '__main__':
	main()