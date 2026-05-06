import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("600x500")
        
        # Загрузка данных
        self.file_path = "books.json"
        self.books = self.load_data()

        # Контейнер для ввода данных
        input_frame = tk.Frame(root, padx=10, pady=10)
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(input_frame)
        self.title_entry.grid(row=0, column=1, sticky="we", padx=5)

        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.author_entry = tk.Entry(input_frame)
        self.author_entry.grid(row=1, column=1, sticky="we", padx=5)

        tk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky="w")
        self.genre_entry = tk.Entry(input_frame)
        self.genre_entry.grid(row=2, column=1, sticky="we", padx=5)

        tk.Label(input_frame, text="Страниц:").grid(row=3, column=0, sticky="w")
        self.pages_entry = tk.Entry(input_frame)
        self.pages_entry.grid(row=3, column=1, sticky="we", padx=5)

        self.add_btn = tk.Button(input_frame, text="Добавить книгу", command=self.add_book, bg="lightgreen")
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")

        # Контейнер для фильтров
        filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10)

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0)
        self.filter_genre_entry = tk.Entry(filter_frame)
        self.filter_genre_entry.grid(row=0, column=1, padx=5)

        self.filter_btn = tk.Button(filter_frame, text="Фильтровать", command=self.apply_filters)
        self.filter_btn.grid(row=0, column=2, padx=5)

        self.reset_btn = tk.Button(filter_frame, text="Сброс", command=self.reset_filters)
        self.reset_btn.grid(row=0, column=3, padx=5)

        self.pages_filter_btn = tk.Button(filter_frame, text="Книги > 200 стр.", command=self.filter_by_pages)
        self.pages_filter_btn.grid(row=1, column=0, columnspan=4, pady=5, sticky="we")

        # Таблица (Treeview)
        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страницы")
        
        self.tree.column("Title", width=150)
        self.tree.column("Author", width=150)
        self.tree.column("Genre", width=100)
        self.tree.column("Pages", width=80)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_table()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        # Проверка на пустые поля
        if not (title and author and genre and pages):
            messagebox.showwarning("Внимание", "Заполните все поля!")
            return

        # Проверка на число
        try:
            pages_int = int(pages)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages_int
        }

        self.books.append(new_book)
        self.save_data()
        self.update_table()
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def save_data(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить: {e}")

    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def update_table(self, data_list=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        source = data_list if data_list is not None else self.books
        for book in source:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filters(self):
        genre_query = self.filter_genre_entry.get().lower()
        filtered = [b for b in self.books if genre_query in b["genre"].lower()]
        self.update_table(filtered)

    def filter_by_pages(self):
        filtered = [b for b in self.books if b["pages"] > 200]
        self.update_table(filtered)

    def reset_filters(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()