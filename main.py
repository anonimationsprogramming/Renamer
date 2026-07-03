import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path


class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk File Renamer")
        self.root.geometry("800x500")

        self.folder = None
        self.files = []

        # Top buttons
        top_frame = tk.Frame(root)
        top_frame.pack(fill="x", pady=5)

        tk.Button(top_frame, text="Select Folder", command=self.select_folder).pack(side="left", padx=5)
        tk.Button(top_frame, text="Rename Files", command=self.rename_files).pack(side="left", padx=5)

        # Table (Treeview)
        self.tree = ttk.Treeview(root, columns=("original", "new", "preview"), show="headings")

        self.tree.heading("original", text="Original Name")
        self.tree.heading("new", text="New Name")
        self.tree.heading("preview", text="Preview")

        self.tree.column("original", width=250)
        self.tree.column("new", width=250)
        self.tree.column("preview", width=250)

        self.tree.pack(fill="both", expand=True)

        # Bind double click to edit
        self.tree.bind("<Double-1>", self.edit_cell)



    def select_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.folder = Path(folder)
        self.files = [f for f in self.folder.iterdir() if f.is_file()]

        self.load_table()


    def load_table(self):
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        for file in self.files:
            name = file.name

            self.tree.insert(
                "",
                "end",
                values=(name, name, name)
            )


    def edit_cell(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if not item:
            return

        x, y, width, height = self.tree.bbox(item, column)

        value = self.tree.set(item, column)

        entry = tk.Entry(self.root)
        entry.place(x=x, y=y+25, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit(event):
            self.tree.set(item, column, entry.get())

            # update preview automatically
            original = self.tree.set(item, "original")
            new = self.tree.set(item, "new")
            self.tree.set(item, "preview", new)

            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())


    def rename_files(self):
        for i, item in enumerate(self.tree.get_children()):
            original, new, _ = self.tree.item(item)["values"]

            old_path = self.folder / original
            new_path = self.folder / new

            if old_path.exists() and original != new:
                old_path.rename(new_path)

        self.load_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()

