import csv
from data_initiator import Headers
from data_initiator import create_lists, list_to_data_dict
from os import path
# The csv module implements classes to read and write tabular data in CSV format


def create_and_ingest_data_into_cvs(entries_number):
    filename = "clients_"+ str(entries_number) +".csv"
    file_path = path.join("CsvFiles", filename)
    data = create_lists(entries_number)
    entries = list_to_data_dict(data)

    with open(file_path, mode="w", newline='', ) as cvs_fstream:
        field_names = [Headers.NOME.value, Headers.MORADA.value, Headers.CP.value,
                       Headers.EMAIL.value, Headers.NIF.value, Headers.CONTACTO.value]

        writer = csv.DictWriter(cvs_fstream, field_names)
        writer.writeheader()
        for entrie in entries:
            writer.writerow(entrie)


if __name__ == "__main__":
    ENTRIES_NUMBER = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2000, 5000, 10000]
    for entrie in ENTRIES_NUMBER:
        create_and_ingest_data_into_cvs(entrie)