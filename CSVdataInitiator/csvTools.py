import csv
# SOURCE: https://docs.python.org/3/library/csv.html
import re
# https://www.geeksforgeeks.org/python-program-to-find-files-having-a-particular-extension-using-regex/
import os
import inspect


# TODO:
#  # Verify that CVS file is ok!
#   use only valuable fields/columns and create a clean file
#  Clean the data (upper names, Case UP....)

def get_message_and_contact():
    with open("listaClientes.csv", mode="r", newline='') as csv_fstream:
        csv_reader = csv.DictReader(csv_fstream)

        print(csv_reader)  # <csv.DictReader object at 0x7f0465ebdac0>
        line_count = 0
        output_Data = []
        headers = csv_reader.fieldnames  # ['Nome', 'Contacto', 'morada', 'codigo postal', 'operador'],
        for row in csv_reader:
            message= f"Caro {row['Nome']}\n" \
                     f"Adira hoje ao serviço XPTO da XPTO TELECOMUNICACOES, televisao, internet e telefone por apenas 30 Eu." \
                     f"Para aderir contactar Joao Lemos,"
            output_Data.append((row["Contacto"], message))

        print(output_Data)
        return output_Data


def generic_csv_reader(file_path):
    with open(file_path, mode="r", newline='') as csv_fstream:
        csv_reader = csv.DictReader(csv_fstream)
        #print(csv_reader)
        headers = csv_reader.fieldnames
        #print(headers)
        return headers


def search_headers(headers, patterns):
    if not headers:
        raise("Error we need a csv HEADERS's list")
    #print("HEADERS", headers)
    found = [] # OUTPUT LIST, WITH HEADERS THAT MATCH
    for header in headers:
        for pattern in patterns:
            #print("SEARCHING IN HEADER: ",header)
            find_this = re.compile(pattern, flags=re.IGNORECASE)
            match = find_this.search(header)
            # if match is found
            if match:
                # print("The file ending with .csv is:",file)
                print("[ FOUND HEADER ] - ", header)
                found.append(header)

    #print("TAMANHO ", len(found))
    if len(found) == 0:
        return False
    else:
        return found


def get_csv_file_paths(base=None):
    """
    This function search for csv files existing in folders.
    :param base: <string> path to start searching (recursive n depth) for csv files
    :return: <tuple> (<string> number of csv files in the list, <list> .csv file paths existinf in all
    folders inside base folder)
    """
    if base is None:
        base = "."  # project folder !
    if not isinstance(base, str):
        raise ValueError(f"Error in definition '{str(inspect.currentframe().f_code.co_name)}(base)'\n "
                         f"base parameter should be a <string>")
    tree = os.walk(base)
    files_paths_list = []  # TO STORE ALL THE .csv FILES
    for row in tree:
        current_folder = row[0]    # E.G. ['CvsNanoMade', 'CvsLibCalc']
        # folders = row[1]         # 'CvsNanoMade', 'CvsLibCalc']
        files = row[2]             # ["file1" ,"file2", "file3", "filen" ]

        #  # search given pattern in the line
        for file in files:
            match = re.search("\.csv$", file)
            # if match is found
            if match:
                #print("The file ending with .csv is:",file)
                files_paths_list.append(os.path.join(current_folder, file))
    number_of_files = len(files_paths_list)
    return number_of_files, files_paths_list


def read_csv_entries(file_name, headers):
    with open(file_name, mode="r", newline='') as csv_fstream:
        csv_reader = csv.DictReader(csv_fstream)
        count_rows = 0

        for row in csv_reader:
            for header in headers:
                #print(f"[ {header} ] - {row[header]}")
                #print("-------------------------------")
                continue
            count_rows = count_rows + 1
        print(f"[Numero de Total de Registos {count_rows} no ficheiro {file_name} ]")


if __name__ == '__main__':
    # contacts_messages = get_message_and_contact()
    # generic_cvs_reader()
    CSV_FILE_FOLDER = "CsvFiles"

    number_files, file_path_list = get_csv_file_paths(CSV_FILE_FOLDER)
    print(f"[ # TOTAL FILES ] {number_files}")
    for count, file_path in enumerate(file_path_list):
        print("=" * 120)
        print(f"[ {count + 1} ] - {file_path}")
        print(f"[ START PROCESSING FILE ] - {file_path}")
        print(f"[ START READING HEADERS ] - {file_path}")
        headers = generic_csv_reader(file_path)
        print(f"[ HEADERS AVAILABLE ] - {headers}")
        pattern_to_search = ["NoMe", "Contacto"]
        result = search_headers(headers, patterns=pattern_to_search)
        #generic_csv_reader_register_reader(file_path,result)
        read_csv_entries(file_name=file_path, headers=headers)


    def a_tests():
        headers = ['nome', 'idade ', 'morada ', 'codigo postal ', 'telefone', 'nif', 'operador',
                   'NOME', 'MORADA', 'CODIGO POSTAL', 'EMAIL', 'NIF', 'CONTACTO', "ULTIMO NOME" ]
        pattern_to_search = "NoMe"
        result = search_headers(headers, pattern=pattern_to_search)
        print(result)


    # def Interessante_Tabular_data():
    #     format_string = "{:<10}{:<8}{:<10}"
    #    print(format_string.format(*headers))
    #    for entry in some_data:
    #        print(format_string.format(*entry))
