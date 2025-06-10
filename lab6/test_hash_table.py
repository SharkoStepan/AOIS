from unittest import TestCase
from Hash_Table import HashTable

class Test(TestCase):
    def test_hash_table_insert(self):
        hash_table = HashTable(size=20, base_address=0)
        hash_table.insert_in_table("Отрицание", "Отрицательная частица")
        assert hash_table.search_in_table("Отрицание") == "Отрицательная частица"

    def test_hash_table_search(self):
        hash_table = HashTable(size=20, base_address=0)
        hash_table.insert_in_table("Прилагательное", "Прилагательное описывает существительное")
        assert hash_table.search_in_table("Существительное") == None
        hash_table.insert_in_table("Прямое дополнение", "То, на что действует подлежащее в предложении")
        assert hash_table.search_in_table("Прямое дополнение") == "То, на что действует подлежащее в предложении"

    def test_hash_update_by_key(self):
        hash_table = HashTable(size=20, base_address=0)
        hash_table.insert_in_table("Отрицание", "Отрицательная частица")
        assert hash_table.search_in_table("Отрицание") == "Отрицательная частица"
        hash_table.update_by_key("Отрицание", "Языковое средство, используемое для выражения идеи о том, что некоторое положение дел не имеет места")
        assert hash_table.search_in_table("Отрицание") == "Языковое средство, используемое для выражения идеи о том, что некоторое положение дел не имеет места"

    def test_hash_delete_by_key(self):
        hash_table = HashTable(size=20, base_address=0)
        hash_table.insert_in_table("Отрицание", "Отрицательная частица")
        assert hash_table.delete_from_table("Глагол") == False
        assert hash_table.delete_from_table("Отрицание") == True

    def test_hash_delete_by_key_end(self):
        hash_table = HashTable(size=20, base_address=0)
        hash_table.insert_in_table("Прилагательное", "Прилагательное описывает существительное")
        hash_table.insert_in_table("Прямое дополнение", "То, на что действует подлежащее в предложении")
        assert hash_table.delete_from_table("Прямое дополнение") == True

    def test_hash_delete_by_key_mid(self):
        hash_table = HashTable(size=20, base_address=0)
        hash_table.insert_in_table("Прилагательное", "Прилагательное описывает существительное")
        hash_table.insert_in_table("Прямое дополнение", "То, на что действует подлежащее в предложении")
        hash_table.insert_in_table("Предлог","Слово, которое показывает роль части предложения, следующей за этим предлогом, во всём предложении")
        assert hash_table.delete_from_table("Прямое дополнение") == True