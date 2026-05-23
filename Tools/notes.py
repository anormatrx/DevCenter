import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os, datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "notes.json"

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("الملاحظات")
        self.root.geometry("750x500")
        self.setup_theme()

        self.notes = self.load_notes()
        self.current_note = None

        self.setup_ui()
        self.setup_context_menu()
        self.bind_shortcuts()
        self.refresh_list()

    def setup_theme(self):
        self.bg = "#1e1e2e"
        self.fg = "#cdd6f4"
        self.accent = "#89b4fa"
        self.surface = "#313244"
        self.root.configure(bg=self.bg)

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.bg)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        left_frame = tk.Frame(main_frame, bg=self.bg, width=250)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(main_frame, bg=self.bg)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(left_frame, text="الملاحظات", bg=self.bg, fg=self.accent,
                 font=("Arial", 12, "bold")).pack(pady=(0, 5))

        self.search_entry = tk.Entry(left_frame, bg=self.surface, fg=self.fg,
                                      insertbackground=self.fg, relief=tk.FLAT, font=("Arial", 10))
        self.search_entry.pack(fill=tk.X, pady=(0, 5))
        self.search_entry.insert(0, "بحث...")
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0, tk.END) if self.search_entry.get() == "بحث..." else None)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_list())

        self.listbox = tk.Listbox(left_frame, bg=self.surface, fg=self.fg,
                                   selectbackground=self.accent, selectforeground=self.bg,
                                   relief=tk.FLAT, font=("Arial", 10), borderwidth=0, highlightthickness=0)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        btn_frame = tk.Frame(left_frame, bg=self.bg)
        btn_frame.pack(fill=tk.X, pady=(5, 0))

        btn_style = {"bg": self.surface, "fg": self.fg, "relief": tk.FLAT,
                     "padx": 8, "pady": 4, "cursor": "hand2", "font": ("Arial", 9)}
        tk.Button(btn_frame, text="+ جديد", command=self.new_note, **btn_style).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        tk.Button(btn_frame, text="حذف", command=self.delete_note, **btn_style).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        tk.Label(right_frame, text="العنوان", bg=self.bg, fg=self.accent,
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 2))

        self.title_entry = tk.Entry(right_frame, bg=self.surface, fg=self.fg,
                                     insertbackground=self.fg, relief=tk.FLAT, font=("Arial", 11))
        self.title_entry.pack(fill=tk.X, pady=(0, 8))

        tk.Label(right_frame, text="المحتوى", bg=self.bg, fg=self.accent,
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 2))

        self.text_area = tk.Text(right_frame, bg=self.surface, fg=self.fg,
                                  insertbackground=self.fg, relief=tk.FLAT,
                                  font=("Arial", 10), wrap=tk.WORD, borderwidth=0, highlightthickness=0,
                                  padx=8, pady=8)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.status_bar = tk.Label(right_frame, text="جاهز", bg=self.surface, fg=self.fg,
                                    anchor=tk.W, padx=8, font=("Arial", 8))
        self.status_bar.pack(fill=tk.X, pady=(4, 0))

        self.title_entry.bind("<KeyRelease>", lambda e: self.save_current())
        self.text_area.bind("<KeyRelease>", lambda e: self.save_current())

    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=self.surface, fg=self.fg,
                                     activebackground=self.accent, activeforeground=self.bg)
        self.context_menu.add_command(label="نسخ", command=self.copy_text, accelerator="Ctrl+C")
        self.context_menu.add_command(label="لصق", command=self.paste_text, accelerator="Ctrl+V")
        self.context_menu.add_command(label="قص", command=self.cut_text, accelerator="Ctrl+X")
        self.context_menu.add_separator()
        self.context_menu.add_command(label="تحديد الكل", command=self.select_all, accelerator="Ctrl+A")

        self.text_area.bind("<Button-3>", self.show_context_menu)
        self.title_entry.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def copy_text(self):
        try:
            self.root.clipboard_clear()
            text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_append(text)
        except tk.TclError:
            pass

    def paste_text(self):
        try:
            text = self.root.clipboard_get()
            focused = self.root.focus_get()
            if focused == self.text_area:
                self.text_area.insert(tk.INSERT, text)
            elif focused == self.title_entry:
                self.title_entry.insert(tk.INSERT, text)
        except tk.TclError:
            pass

    def cut_text(self):
        self.copy_text()
        try:
            self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass

    def select_all(self):
        focused = self.root.focus_get()
        if focused == self.text_area:
            self.text_area.tag_add(tk.SEL, "1.0", tk.END)
            self.text_area.mark_set(tk.INSERT, "1.0")
            self.text_area.see(tk.INSERT)
        elif focused == self.title_entry:
            self.title_entry.selection_range(0, tk.END)

    def bind_shortcuts(self):
        self.root.bind("<Control-c>", lambda e: self.copy_text())
        self.root.bind("<Control-v>", lambda e: self.paste_text())
        self.root.bind("<Control-x>", lambda e: self.cut_text())
        self.root.bind("<Control-a>", lambda e: self.select_all())
        self.root.bind("<Control-n>", lambda e: self.new_note())
        self.root.bind("<Delete>", lambda e: self.delete_note())

    def load_notes(self):
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, Exception):
                return []
        return []

    def save_notes(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, indent=2, ensure_ascii=False)
        self.status_bar.config(text=f"تم الحفظ - {len(self.notes)} ملاحظة")

    def refresh_list(self, filter_text=None):
        self.listbox.delete(0, tk.END)
        search = self.search_entry.get().strip().lower()
        if search == "بحث...":
            search = ""
        for note in self.notes:
            title = note.get("title", "") or ""
            content = note.get("content", "") or ""
            if not search or search in title.lower() or search in content.lower():
                display = title if title else "(بدون عنوان)"
                self.listbox.insert(tk.END, display)

    def on_select(self, event):
        self.save_current()
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            search = self.search_entry.get().strip().lower()
            if search == "بحث...":
                search = ""
            visible = [n for n in self.notes if not search or
                       search in (n.get("title", "") or "").lower() or
                       search in (n.get("content", "") or "").lower()]
            if idx < len(visible):
                note = visible[idx]
                self.current_note = note
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, note.get("title", ""))
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", note.get("content", ""))

    def new_note(self):
        note = {
            "id": datetime.datetime.now().isoformat(),
            "title": "ملاحظة جديدة",
            "content": "",
            "created": datetime.datetime.now().isoformat(),
            "updated": datetime.datetime.now().isoformat()
        }
        self.notes.append(note)
        self.save_notes()
        self.refresh_list()
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(tk.END)
        self.listbox.activate(tk.END)
        self.on_select(None)
        self.title_entry.selection_range(0, tk.END)
        self.title_entry.focus()

    def delete_note(self):
        if not self.current_note:
            return
        if messagebox.askyesno("تأكيد", "مسح هذي الملاحظة؟", parent=self.root):
            self.notes = [n for n in self.notes if n["id"] != self.current_note["id"]]
            self.current_note = None
            self.title_entry.delete(0, tk.END)
            self.text_area.delete("1.0", tk.END)
            self.save_notes()
            self.refresh_list()

    def save_current(self):
        if self.current_note:
            self.current_note["title"] = self.title_entry.get()
            self.current_note["content"] = self.text_area.get("1.0", tk.END).strip()
            self.current_note["updated"] = datetime.datetime.now().isoformat()
            self.save_notes()
            self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()