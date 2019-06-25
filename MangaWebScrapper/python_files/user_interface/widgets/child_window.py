import tkinter as tk


class ChildWindow(tk.Toplevel):
    def __init__(self, title: str, resize: bool = True, geometry: str = None, destroy_on_exit: bool = True):

        super().__init__()

        self.is_viewable = False

        self.title(title)
        self.resizable(resize, resize)

        if geometry:
            self.geometry(geometry)
        
        if destroy_on_exit:
            self.protocol("WM_DELETE_WINDOW", self.destroy)
        else:
            self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def show_window(self):
        self.is_viewable = True
        self.deiconify()

    def hide_window(self):
        self.is_viewable = False
        self.withdraw()

    def center_in_root(self, w, h):
        master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
        master_w, master_h = self.master.winfo_width(), self.master.winfo_height()

        win_w, win_h = w, h

        center_x = master_x + (master_w // 2) - (win_w // 2)
        center_y = master_y + (master_h // 2) - (win_h // 2)

        self.geometry(f"{win_w}x{win_h}+{center_x}+{center_y}")