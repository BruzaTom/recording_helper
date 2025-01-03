import os
import shutil
import ast
import tkinter as tk
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

buttonGrey = '#444444'
lableBlue = 'darkblue'
dataBoxbg = lableBlue
lightBlue = '#B0C4DE'
green = '#66CD00'
pink = '#EE1289'

root = tk.Tk()
root.title("Directory Observer")
root.configure(bg=lableBlue)
root.geometry("675x700")
entry = tk.Entry(root)



class RecordingHandler(FileSystemEventHandler):
    def __init__(self, folder, queue):
        self.folder = folder
        self.queue = queue

    def on_created(self, event):
        if not event.is_directory:
            self.queue.put(event.src_path)

class App:
    def __init__(self):
        self.path = self.getLst('path.txt')[0]
        self.path2 = self.getLst('path.txt')[1]
        self.queue = Queue()
        self.setup_ui()
        #print(self.path)

    def setup_ui(self):
        forget_all(root)
        makeLable('\n\n\n\nObserving files in\n\n{}\n'.format(self.path), 18)
        makeLable('Destination path set to\n\n{}\n'.format(self.path2), 18)
        makeButton('Observe New', self.changePath)
        makeButton('New Destination', self.changePath2)

        root.after(100, self.process_queue)

    def process_queue(self):
        if not self.queue.empty():
            file_path = self.queue.get()
            self.show_options(file_path)
        root.after(100, self.process_queue)

    def show_options(self, file_path):
        forget_all(root)
        file_name = file_path.split('\\')[-1]
        makeLable(f"\n\nDo you want to keep or delete\n\n{file_name}?\n", 18)
        makeButton('Delete', lambda: self.delete(file_path))
        makeButton('Keep', lambda: self.keep(file_path))
        makeButton('Rename', lambda: self.rename(file_path))
        makeButton('Move to Destination', lambda: self.move(file_path))
        root.lift()  # Bring the window to the top
        root.attributes("-topmost", True)
        root.attributes("-topmost", False)
        root.focus_force()

    def rename(self, file_path):
        forget_all(root)
        makeLable(f'\n\n\n\nEnter New File Name\n', 18)
        entry = tk.Entry(root)
        entry.pack()
        lst = file_path.split('\\')
        def rename_path():
            name = r"{}".format(entry.get())
            old = lst[-1].split('.')[0]
            ext = lst[-1].split('.')[1]
            lst[-1] = lst[-1].replace(old, ' ' + name + '.' + ext)
            os.rename(file_path, ('\\').join(lst))
            self.setup_ui()
        def to_dest():
            name = r"{}".format(entry.get())
            old = lst[-1].split('.')[0]
            ext = lst[-1].split('.')[1]
            lst[-1] = lst[-1].replace(old, ' ' + name + '.' + ext)
            new_file = ('\\').join(lst)
            os.rename(file_path, new_file)
            shutil.move(new_file, self.path2)
            self.setup_ui()
        makeButton('Save', rename_path)
        makeButton('Save to Destination', to_dest)

    def move(self, file_path):
        forget_all(root)
        shutil.move(file_path, self.path2)
        self.setup_ui()

    def delete(self, file_path):
        forget_all(root)
        os.remove(file_path)
        self.setup_ui()

    def keep(self, file_path):
        forget_all(root)
        self.setup_ui()

    def changePath(self):
        lst = []
        forget_all(root)
        makeLable(f'\n\n\n\nEnter New Path\n', 18)
        
        entry = tk.Entry(root)
        entry.pack()
        
        def get_path():
            path = r"{}".format(entry.get())
            path = path.replace('"', '')
            lst = [path, self.path2]
            self.updateFile(lst, 'path.txt')
            self.path = self.getLst('path.txt')[0]
            #self.setup_ui()
            self.sorry()
        
        makeButton('Submit', get_path)

    def changePath2(self):
        forget_all(root)
        makeLable(f'\n\n\n\nEnter New Destination Path\n', 18)
        
        entry = tk.Entry(root)
        entry.pack()
        
        def get_path():
            path = r"{}".format(entry.get())
            path = path.replace('"', '')
            lst = [self.path, path]
            self.updateFile(lst, 'path.txt')
            self.path2 = self.getLst('path.txt')[1]
            #self.setup_ui()
            self.sorry()
        
        makeButton('Submit', get_path)

    def sorry(self):
        forget_all(root)
        makeLable(f'\n\n\n\nChanges have been made.\nplease close and restart app\n working on solution..', 18)

    def updateFile(self, Lst, file):
        with open(file, "w") as f:
            f.write(str(Lst))

    def getLst(self, file):
        with open(file) as f:
            data = f.read()
        return ast.literal_eval(data)

def start_observer(folder_to_watch, queue):
    event_handler = RecordingHandler(folder_to_watch, queue)
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=False)
    observer.start()
    return observer

def makeLable(string, size):
    return tk.Label(root, text=string, fg='#66CD00', bg=lableBlue, font=("Arial", size, "bold")).pack()

def makeButton(name, func):
    return tk.Button(
        root,
        text=name,
        command=func,
        fg='#66CD00', bg=lableBlue,
        height=3, width=16,
        font=("Arial", 12, "bold")
    ).pack()

def forget_all(parent):
    for widget in parent.winfo_children():
        widget.pack_forget()

def main():
    user = App()
    folder_to_watch = user.path
    observer = start_observer(folder_to_watch, user.queue)
    root.mainloop()

if __name__ == "__main__":
    main()
