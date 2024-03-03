import sqlite3

# Создаем или подключаемся к базе данных
conn = sqlite3.connect("web_links.db")
cursor = conn.cursor()

# Создаем таблицу для хранения ссылок
cursor.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY,
        url TEXT UNIQUE,
        search_count INTEGER DEFAULT 0
    )
""")
conn.commit()

def add_link(url):
    try:
        cursor.execute("INSERT INTO links (url) VALUES (?)", (url,))
        conn.commit()
        print(f"Ссылка {url} успешно добавлена в базу данных.")
    except sqlite3.IntegrityError:
        print(f"Ссылка {url} уже существует в базе данных.")

def search_links(query):
    cursor.execute("SELECT url FROM links WHERE url LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()
    if results:
        print("Результаты поиска:")
        for row in results:
            print(row[0])
    else:
        print("Ничего не найдено.")

def clear_database():
    cursor.execute("DELETE FROM links")
    conn.commit()
    print("База данных очищена.")

def run():
    while True:
        print("\nВыберите действие:")
        print("1. Добавить ссылку")
        print("2. Поиск ссылок")
        print("3. Очистить базу данных")
        print("4. Выйти")
        choice = input("Введите номер действия: ")

        if choice == "1":
            url = input("Введите ссылку: ")
            add_link(url)
        elif choice == "2":
            query = input("Введите поисковый запрос: ")
            search_links(query)
        elif choice == "3":
            clear_database()
        elif choice == "4":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    conn.close()

if __name__ == "__main__":
    run()
