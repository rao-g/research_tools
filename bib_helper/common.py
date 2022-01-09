import bibtexparser


def read_bib_file(file_path: str):
    """
    Method to read the bibtex file and return a list of bib entries
    :param file_path:
    :return:
    """
    with open(file_path, 'r', errors='ignore') as f:
        bib_database = bibtexparser.load(f)
    return bib_database


def get_data_from_db(bib_db, key):
    """
    Method to get list of items from db
    :param bib_db: bib db
    :param key: key to be extracted
    :return:
    """
    return_list = []
    for each in bib_db.entries:
        return_list.append(each.get(key, None))
    return return_list


def write_bib_file(file_path: str, bib_db):
    """
    Method to read the bibtex file and return a list of bib entries
    :param bib_db: bib database
    :param file_path:
    :return:
    """
    with open(file_path, 'w') as bibtex_file:
        bibtexparser.dump(bib_db, bibtex_file)
