from comparer import FileComparision


def test_file_compare():
    FileComparision.compare("old.txt", "new.txt", "test.json")


test_file_compare()
