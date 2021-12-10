
import sys
from enum import Enum
from random import choice, choices
from json import dumps

class ExtractNames(object):
    #  SOURCE: https://www.dn.pt/DNMultimedia/DOCS+PDFS/2013/Nomes%202013%20M%20(at%C3%A9%2020%20dez.).pdf
    def __init__(self):
        pass

    def get_names(self):
        with open("base_f_name-txt", "r") as fstream_in:
            data = fstream_in.readlines()
        with open("Nomes/nomesFemininos.data", "a") as fstream_out:
            fstream_out.write(f"{len(data)}\n")
            for name in data:
                fstream_out.write(name.split(" ")[0])
                fstream_out.write("\n")

    def get_masculinos(self):
        with open("base_f_name-txt", "r") as fstream_in:
            data = fstream_in.readlines()

        with open("Nomes/nomesMasculinos.data", "a") as fstream_out:
            count = 0
            final_list = []
            for name in data:
                print(name.split(" ")[0])
                name =  name.split(" ")[0]
                # Folha1
                # Página 10
                if "Folha" in name or"Página" in name:
                    continue
                final_list.append(name)

            fstream_out.write(f"{len(final_list)}\n")
            for name in final_list:
                print(name)
                fstream_out.write(name)
                fstream_out.write("\n")

    def get_apelidos(self):
        with open("base_f_name-txt", "r") as fstream_in:
            data = fstream_in.readlines()

        with open("Nomes/apelidos.data", "a") as fstream_out:
            fstream_out.write(f"{len(data)}\n")
            for name in data:
                name = name.split("\t")[1]
                fstream_out.write(name)
                fstream_out.write("\n")

############################################
# BEGIN SECTION TO CREATE A LIST WITH NAMES
#


def load_data_from_file(file_path):
    try:
        with open(file_path, "rt") as fstream:
            fstream.readline()
            data = fstream.readlines()
            data = [name.split("\n")[0] for name in data]
            return data
    except OSError as error:
        sys.exit(f"Error, while attempting to open/ read file {file_path}\n ERROR: {error}")


def init_random_name(genero, qt1, qt2 ):
    """
    Rule: 1 or 2 names
          1,2 ,3,4 Last names
    :param genero:
    :return:
    """
    FEM_NAME_FILE = "Nomes/nomesFemininos.data"
    MAS_NAME_FILE = "Nomes/nomesMasculinos.data"
    LAST_NAME_FILE = "Nomes/apelidos.data"

    if not isinstance(qt1, int):
        raise ValueError("qt1 <int> number of first names. between 1 and 2")
    if not isinstance(qt2, int):
        raise ValueError("qt1 <int> number of first names. between 1 and 2")

    if qt1 <= 0 or qt1 > 2:
        qt1 = 1
    if qt2 <= 0 or qt2 > 4:
        qt2 = 1

    if genero is None:
        raise ValueError("genero is None")
    if genero == "MAS":
        masc_names_lst = load_data_from_file(MAS_NAME_FILE)
        first_names = choices(masc_names_lst, weights=None, k=qt1)
    elif genero == "FEM":
        fem_names_lst = load_data_from_file(FEM_NAME_FILE)
        first_names = choices(fem_names_lst, weights=None, k=qt1)
    else:
        raise ValueError("ERROR: wrong 'genero'::: e.g. genero=MAS or genero=FEM")

    last_names_lst = load_data_from_file(LAST_NAME_FILE)
    last_names = choices(last_names_lst,weights=None, k=qt2)
    #print(first_names)
    #print(last_names)
    first_names.extend(last_names)
    return  first_names


def init_list_random_names(qt=None):
    if qt is None:
        if not isinstance(qt, int):
            raise ValueError("qt is <int> number of names to be generated")
    output_data_lst = []
    rnd_numbers_first_name = [1, 2]
    rnd_numbers_last_name = [1, 2, 3, 4]
    rnd_genero = ["MAS", "FEM"]

    for count in range(1, qt + 1):
        output_data_lst.append(init_random_name(choice(rnd_genero),
                                                choice(rnd_numbers_first_name),
                                                choice(rnd_numbers_last_name))
                               )
    output_data_lst = [" ".join(names) for names in output_data_lst]
    return output_data_lst

########################
# CREATE FAKE PHONES
#

def init_phone_numbers(operator=None):
    """ Retrun a portuguse phone number (9 digits)"""
    operators = [91, 92, 93, 96]
    if operator is None:
        operator = choice(operators)
    if not isinstance(operator, int):
        operator = choice(operators)
    if operator not in operators:
        operator = choice(operators)
    numbers = [0, 1, 2 , 3, 4, 5, 6, 7, 8, 9]
    sufix = choices(numbers, weights=None, k=7)
    s_sufix= ""
    for number in sufix:
        s_sufix = s_sufix + str(number)
    phone_number = str(operator) + s_sufix
    return phone_number

def init_list_phone_numbers(qt):
    output_lst = []
    for _ in range(1, qt + 1):
        output_lst.append(init_phone_numbers())
    return output_lst


######## RUAS
def init_moradas(nomes_ruas=None, qt=1):
    if nomes_ruas is None:
        nomes_ruas = "Nomes/ruasAvenidas.data"
    if qt is None or qt < 0:
        qt = 1

    try:
        data_ruas = load_data_from_file(nomes_ruas)
    except Exception as error:
        print(error)

    #print(data_ruas)
    numbers = [x for x in range(1, 1000)]
    moradas_data_list = []
    codigos_postais_list = []
    for i in range(1, qt + 1):
            rua = choice(data_ruas) + " " + "Nº" + str(choice(numbers))
            moradas_data_list.append(rua)

            codigo4 = choices([x for x in range(1,10)], weights=None, k=4)
            codigo3 = choices([x for x in range(0, 10)], weights=None, k=3)

            def convert_to_String(lst):
                out_data_str = ""
                for number in lst:
                    out_data_str = out_data_str + str(number)
                return out_data_str
            codigo4 = convert_to_String(codigo4)
            codigo3 = convert_to_String(codigo3)
            codigo_postal = codigo4 + "-" + codigo3
            codigos_postais_list.append(codigo_postal)
    return moradas_data_list, codigos_postais_list

##### init NIFS
def init_nif(qt):
    """
    This function returns a list with strings of nif
        E.G.  for qt==10:
                ['528067159', '659523614', '430802591', '613239453', '633494480', '395340626',
                '541431308', '222882980', '525084423', '211574555']
    :param qt: <int>len of the list (# nifs)
    :return: <list> a list with nif number
    """
    def init_one_nif():
        """
        This function return a string with 9 digits (NIF) (NOT REAL ONES)
        :return:
        """
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        nif = str(choice([2, 3, 4, 5, 6, 7]))
        for i in range(8):
            nif = nif + str(choice(numbers))
        return nif

    nif_list = []
    for i in range(qt):
        nif_list.append(init_one_nif())
    return nif_list


##### EMAILS

def init_emails(first_name, last_name):
    domains = ["outlook.pt", "outlook.com", "hotmail.com", "gmail.com", "isec.pt", "mundo.pt", "trabalho.pt"]
    data_out = []
    email= (first_name + "." + last_name + "@" + str(choice(domains)))
    return email

def create_lists(number_of_registries):
    """
    TO USE THIS CALL THE FUNCTION
        create_lists(NUMBER_OF_ENTRIES)
     IT WILL OUTPUT A LIST of tuples LIKE THE ONE BELOW:
        [('Thaís Campos  Torres ', 'Travessa da Amorosa Nº88', '2872-249', '929825936', '758533636'),
        ('Janaína Liliana Machado ', 'Bairro do Cerco do Porto Nº387', '8135-221', '936398282', '456384516'),
        ('Filipe Soares ', 'Bairro do Bom Sucesso Nº100', '9492-291', '924346548', '496186021')]

    number_of_registries <int> length of the list
    return: <list>
    """


    nifs = init_nif(number_of_registries)
    #print(nifs)

    ruas, cp = init_moradas(None, number_of_registries)
    #for count, rua in enumerate(ruas):
    #    print(ruas[count], cp[count])

    phones = init_list_phone_numbers(number_of_registries)
    #print(phones)

    # CALL to CREATE A LIST WITH NAMES
    names = init_list_random_names(number_of_registries)

    emails = []
    for index in range(number_of_registries):
        name = names[index].split(" ")
        emails.append(init_emails(name[0], name[-1]))

    final = []
    for i in range(number_of_registries):
        final.append((names[i], ruas[i], cp[i], phones[i], nifs[i], emails[i]))
    return final


class Headers(Enum):
    NOME= "NOME"
    MORADA= "MORADA"
    CP = "CODIGO POSTAL"
    CONTACTO= "CONTACTO"
    NIF = "NIF"
    EMAIL="EMAIL"

def list_to_data_dict(data_list_to_convert):
    """
     # input
    # [('Thaís Campos  Torres ', 'Travessa da Amorosa Nº88', '2872-249', '929825936', '758533636'), ..., ..., ]

    # return <list> list with dictionaries
                            [{
                                "NOME": "Thaís Campos  Torres ",
                                "MORADA": "Travessa da Amorosa Nº88",
                                "CODIGO POSTAL": "2872-249",
                                "CONTACTO": "929825936",
                                "NIF": "758533636"
                            },
                            ...,
                            ...
                            ]
    :param data_list_to_convert:
    :return:
    """
    data = []
    for index, row in enumerate(data_list_to_convert):
        data.append(
            {
            Headers.NOME.value: row[0],
            Headers.MORADA.value: row[1],
            Headers.CP.value: row[2],
            Headers.CONTACTO.value: row[3],
            Headers.NIF.value: row[4],
            Headers.EMAIL.value: row[5],
            }
        )
    return data


if __name__ == "__main__":

    NUMBER_OF_ENTRIES = 50
    entries = create_lists(NUMBER_OF_ENTRIES)
    for e in entries:
        print(e)
    data = list_to_data_dict(entries)
    print("---")
    print(data)
    for element in data:
          print(dumps(element, indent=4))
    #



