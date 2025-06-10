import sys
from dataclasses import dataclass
from typing import Optional, Tuple

# Константы
TABLE_SIZE = 20
ALPHABET_SIZE = 33  # Размер русского алфавита
INITIAL_ADDRESS = 0
MAX_LINE_LENGTH = 150  # Ограничение длины строки
MAX_METHOD_LINES = 20  # Ограничение длины метода

# Русский алфавит для вычисления V
RUSSIAN_ALPHABET = {
    'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ё': 6, 'Ж': 7, 'З': 8, 'И': 9,
    'Й': 10, 'К': 11, 'Л': 12, 'М': 13, 'Н': 14, 'О': 15, 'П': 16, 'Р': 17, 'С': 18,
    'Т': 19, 'У': 20, 'Ф': 21, 'Х': 22, 'Ц': 23, 'Ч': 24, 'Ш': 25, 'Щ': 26, 'Ъ': 27,
    'Ы': 28, 'Ь': 29, 'Э': 30, 'Ю': 31, 'Я': 32
}


@dataclass
class HashTableEntry:
    key: Optional[str] = None
    collision_flag: bool = False  # C
    used_flag: bool = False  # U
    terminal_flag: bool = False  # T
    link_flag: bool = False  # L
    deleted_flag: bool = False  # D
    overflow_pointer: Optional[int] = None  # Po
    data: Optional[str] = None  # Pi


class GrammarHashTable:
    def __init__(self):
        self.size = TABLE_SIZE
        self.table = [HashTableEntry() for _ in range(self.size)]
        self.entry_count = 0

    def _calculate_key_value(self, key: str) -> int:
        if len(key) < 2:
            raise ValueError("Ключ должен содержать минимум 2 буквы")
        first_char_value = RUSSIAN_ALPHABET.get(key[0].upper(), 0)
        second_char_value = RUSSIAN_ALPHABET.get(key[1].upper(), 0)
        return first_char_value * ALPHABET_SIZE + second_char_value

    def _first_hash_function(self, key_value: int) -> int:
        return (key_value % self.size) + INITIAL_ADDRESS

    def _second_hash_function(self, key_value: int) -> int:
        return 1 + (key_value % (self.size - 1))

    def _find_slot(self, key: str, key_value: int) -> Tuple[int, bool]:
        hash1 = self._first_hash_function(key_value)
        hash2 = self._second_hash_function(key_value)
        i = 0
        while True:
            index = (hash1 + i * hash2) % self.size
            entry = self.table[index]
            if not entry.used_flag or entry.deleted_flag:
                return index, False
            if entry.key == key and not entry.deleted_flag:
                return index, True
            i += 1
            if i >= self.size:
                raise RuntimeError("Таблица заполнена")

    def insert(self, key: str, data: str) -> None:
        if self.entry_count >= self.size:
            raise RuntimeError("Таблица заполнена")
        key_value = self._calculate_key_value(key)
        index, key_exists = self._find_slot(key, key_value)
        if key_exists:
            raise ValueError(f"Ключ '{key}' уже существует")

        entry = self.table[index]
        entry.key = key
        entry.data = data
        entry.used_flag = True
        entry.terminal_flag = True
        entry.collision_flag = index != self._first_hash_function(key_value)

        if entry.collision_flag:
            prev_index = self._find_previous_in_chain(index, key_value)
            if prev_index is not None:
                self.table[prev_index].overflow_pointer = index
                self.table[prev_index].terminal_flag = False

        self.entry_count += 1

    def _find_previous_in_chain(self, target_index: int, key_value: int) -> Optional[int]:
        hash1 = self._first_hash_function(key_value)
        hash2 = self._second_hash_function(key_value)
        i = 0
        current_index = hash1
        while i < self.size:
            entry = self.table[current_index]
            if entry.used_flag and not entry.deleted_flag and entry.overflow_pointer == target_index:
                return current_index
            i += 1
            current_index = (hash1 + i * hash2) % self.size
        return None

    def search(self, key: str) -> Optional[str]:
        key_value = self._calculate_key_value(key)
        hash1 = self._first_hash_function(key_value)
        hash2 = self._second_hash_function(key_value)
        i = 0
        while i < self.size:
            index = (hash1 + i * hash2) % self.size
            entry = self.table[index]
            if not entry.used_flag or entry.deleted_flag:
                return None
            if entry.key == key and not entry.deleted_flag:
                return entry.data
            i += 1
        return None

    def delete(self, key: str) -> None:
        key_value = self._calculate_key_value(key)
        hash1 = self._first_hash_function(key_value)
        hash2 = self._second_hash_function(key_value)
        i = 0
        while i < self.size:
            index = (hash1 + i * hash2) % self.size
            entry = self.table[index]
            if not entry.used_flag:
                return
            if entry.key == key and not entry.deleted_flag:
                entry.deleted_flag = True
                self.entry_count -= 1
                if entry.terminal_flag:
                    entry.used_flag = False
                else:
                    next_index = entry.overflow_pointer
                    if next_index is not None:
                        next_entry = self.table[next_index]
                        entry.key = next_entry.key
                        entry.data = next_entry.data
                        entry.collision_flag = next_entry.collision_flag
                        entry.terminal_flag = next_entry.terminal_flag
                        entry.overflow_pointer = next_entry.overflow_pointer
                        next_entry.used_flag = False
                        next_entry.deleted_flag = True
                return
            i += 1

    def update(self, key: str, new_data: str) -> None:
        key_value = self._calculate_key_value(key)
        hash1 = self._first_hash_function(key_value)
        hash2 = self._second_hash_function(key_value)
        i = 0
        while i < self.size:
            index = (hash1 + i * hash2) % self.size
            entry = self.table[index]
            if not entry.used_flag or entry.deleted_flag:
                raise ValueError(f"Ключ '{key}' не найден")
            if entry.key == key and not entry.deleted_flag:
                entry.data = new_data
                return
            i += 1
        raise ValueError(f"Ключ '{key}' не найден")

    def get_fill_factor(self) -> float:
        return self.entry_count / self.size

    def display(self) -> None:
        print(f"Коэффициент заполнения: {self.get_fill_factor():.2%}")
        print("Содержимое хеш-таблицы:")
        print("| № | Ключ           | C | U | T | L | D | Po | Данные                     | V  | h  |")
        print("|---|----------------|---|---|---|---|---|----|---------------------------|----|----|")
        for i, entry in enumerate(self.table):
            if entry.used_flag and not entry.deleted_flag:
                key_value = self._calculate_key_value(entry.key)
                hash_value = self._first_hash_function(key_value)
                print(f"| {i:1} | {entry.key:<14} | {1 if entry.collision_flag else 0} | "
                      f"{1 if entry.used_flag else 0} | {1 if entry.terminal_flag else 0} | "
                      f"{1 if entry.link_flag else 0} | {1 if entry.deleted_flag else 0} | "
                      f"{entry.overflow_pointer if entry.overflow_pointer is not None else '-':>2} | "
                      f"{entry.data:<25} | {key_value:>2} | {hash_value:>2} |")


def main():
    hash_table = GrammarHashTable()
    entries = [
        ("Существительное", "Имя, обозначающее предмет"),
        ("Глагол", "Часть речи, действие"),
        ("Прилагательное", "Часть речи, признак"),
        ("Наречие", "Обстоятельство действия"),
        ("Местоимение", "Замена имени"),
        ("Предлог", "Связь слов в предложении"),
        ("Союз", "Связь частей предложения"),
        ("Частица", "Усиление или отрицание"),
        ("АртИкль", "Определитель существительного"),
        ("Синтаксис", "Структура предложения"),
        ("Морфология", "Изучение форм слов"),
        ("Фонетика", "Звуковая система языка")
    ]

    for key, data in entries:
        try:
            hash_table.insert(key, data)
        except ValueError as e:
            print(f"Ошибка: {e}")

    hash_table.display()

    print("\nПоиск 'Глагол':", hash_table.search("Глагол"))
    print("Поиск 'Пунктуация':", hash_table.search("Пунктуация"))

    hash_table.update("Существительное", "Часть речи, предмет")
    print("\nПосле обновления 'Существительное':")
    hash_table.display()

    hash_table.delete("Наречие")
    print("\nПосле удаления 'Наречие':")
    hash_table.display()


if __name__ == "__main__":
    main()