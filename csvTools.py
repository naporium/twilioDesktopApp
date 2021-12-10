import csv
import re
import jinja2
from tkinter import *
import math
from tkinter import ttk
import os
import mimetypes


def readTemplate(template_name, nome=None, morada=None,):
    if nome is None:
        nome= "Dude"
    if template_name is None:
        raise ValueError("we need a jinja 2 template")

    #template_name = "helloWorld.j2"

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("MessageTemplates"))
    t = env.get_template(template_name)
    #print(t.render(nome=nome))
    return str(t.render(nome=nome, morada=morada))



def readTemplate1(template_name, kwargs):
    if template_name is None:
        raise ValueError("we need a jinja 2 template")

    #template_name = "helloWorld.j2"

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("MessageTemplates"))
    t = env.get_template(template_name)
    #print(t.render(nome=nome))
    return str(t.render(**kwargs))


def getMessageAndContact():
    with open("listaClientes.csv", mode="r", newline='') as csv_fstream:
        csv_reader = csv.DictReader(csv_fstream)

        print(csv_reader)  # <csv.DictReader object at 0x7f0465ebdac0>
        line_count = 0
        output_Data = []
        headers = csv_reader.fieldnames  # ['Nome', 'Contacto', 'morada', 'codigo postal', 'operador'],

        # TODO MODIFY THIS FUNCTION
        for row in csv_reader:
            message= f"Caro {row['Nome']}\n" \
                     f"Adira hoje ao serviço XPTO da XPTO TELECOMUNICACOES, televisao, internet e telefone por apenas 30 Eu." \
                     f"Para aderir contactar Joao Lemos,"
            output_Data.append((row["Contacto"], message))

        print(output_Data)
        return output_Data

# def isContact_valid(contact):
#     pattern = "92|3|6\d{7}"
#     find_this = re.compile(pattern, flags=re.IGNORECASE)
#     match = find_this.search(contact)
#     # if match is found
#     if match:
#         #match_[pattern] = header
#         #found.append(match_)
#         pass

def isContact_valid(contact):
    """
    TODO testar isto!
    :param contact:
    :return:
    """
    pattern = "9(1|2|3|6)\d*"
    find_this = re.compile(pattern, flags=re.IGNORECASE)
    match = find_this.search(contact)
    # if match is found
    if match:
        match.group()
        if len(match.group()) != 9:
            return False
        #print(match)
        #print(match.group())
        return match.group()
    else:
        return False


def add_country_number(phone_number, country=None):
    countries = {"PT": "+351"}

    if phone_number is None or not isinstance(phone_number, str):
        raise ValueError("wrong phone number. Phone number should be a string")
    if country is None:
        return countries["PT"] + str(phone_number)
    else:
        for key, value in countries.items():
            if country != key:
                raise ValueError("Country not Found. Please add a valid Country")
        return countries["PT"] + str(phone_number)


def contruct_messages( csv_file, template_name, recompiled_searced_headers, csv_contact_header):
    # [ recompiled_searced_headers ] :[{'CsvHeader': 'NOME', 'template_var': 'nome'}]
    # [ recompiled_searced_headers ] :{'nome': 'NOME'}
    print("###############################")
    print(csv_file)
    print(template_name)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("MessageTemplates"))
    t = env.get_template(template_name)

    with open(csv_file, mode="r", newline='') as csv_fstream:
        csv_reader = csv.DictReader(csv_fstream)
        line_count = 0
        output_Data = []
        headers = csv_reader.fieldnames  # E.G. ['Nome', 'Contacto', 'morada', 'codigo postal', 'operador'],

        final_argument_dict = {}
        for row in csv_reader:
            if recompiled_searced_headers is False:
                # THIS BLOCK IS FOR TEMPLATES THAT DONT HAVE VARIABLES
                message = str(t.render())  # render template message withou variables
                contact = row[csv_contact_header]  # contact = '912328382'
                # VALIDATE NUMBER , AND ADD +351
                result_number = isContact_valid(contact=row[csv_contact_header])
                if result_number is not False:
                    final_number = add_country_number(result_number)
                    output_Data.append((message, final_number, len(message), math.ceil(abs(len(message) / 160))))
                    # output_Data = [('Olá Nuno,  \nA mensagem foi processada pela API TWILLIO!\n', '+351917056887', 56, 1)]
                    #final_argument_dict = {}  # clean dictionary on reLOOP
                else:
                    # TODO
                    #  Since phone number is not valid and should not be appended to the final list ,
                    #  we should LOG this csv entry to file
                    continue

            else:
                # THIS BLOCK IS FOR TEMPLATES THAT HAVE VARIABLES
                for k, value in recompiled_searced_headers.items():
                    print(recompiled_searced_headers)
                    final_argument_dict[k] = row[value]  # exemplo: {"nome": "luis", "contacto": "912202020"}
                message = str(t.render(**final_argument_dict))
                # output_Data = [<message>, <phone_number>, <number of chars in message>, <segment>]
                # TODO:
                #  Segment , and number of chars should be processed in different fucntion
                #  E.G. One that handle with Twilio API CALLS
                contact = row[csv_contact_header]

                # VALIDATE NUMBER , AND ADD +351
                result_number = isContact_valid(contact=row[csv_contact_header])
                if result_number is not False:
                    final_number = add_country_number(result_number)
                    output_Data.append((message, final_number, len(message), math.ceil(abs(len(message)/160))))
                    #output_Data.append((message, row[csv_contact_header], len(message), math.ceil(abs(len(message)/160))))
                    final_argument_dict = {}  # clean dictionary on reLOOP
                else:
                    # TODO
                    #  Since phone number is not valid and should not be appended to the final list ,
                    #  we should LOG this csv entry to file
                    continue

        for element in output_Data:
            print(element)
        return output_Data


def isAnyHeader_inJinjaTemplate(headers, template_vars):
    """
            This function check if jinja2  template matches a CSV file data.
            It will compare headers and vars found in files, and check if any match.
            return tupple of pairs match ((header, var), (header, var), ..., )
            It will return <None> otherwise
    :param headers: <list> csv headers
    :param template_vars: <list> vars found in jinja2 template
    :return: <tuple> if match <None> if not match
    """
    data_out = []
    for header in headers:
        for var in template_vars:
            if var == header:
                data_out.append((var, header))
    return data_out


def getHeaders(file_path):
    """
    Tries to read a csv file, and find export csv headers
    :param file_path:
    :return: <list> csv headers
    """
    with open(file_path, mode="r", newline='') as csv_fstream:
        csv_reader = csv.DictReader(csv_fstream)
        #print(csv_reader)
        headers = csv_reader.fieldnames
        #print(headers)
        return headers


def searchHeaders(headers, patterns):
    if not headers:
        raise("Error we need a csv HEADERS's list")
    #print("HEADERS", headers)
    found = [] # OUTPUT LIST, WITH HEADERS THAT MATCH
    match_ = {}
    for header in headers:
        for pattern in patterns:
            #print("SEARCHING IN HEADER: ",header)
            find_this = re.compile(pattern, flags=re.IGNORECASE)
            match = find_this.search(header)
            # if match is found
            if match:
                match_[pattern] = header
                found.append(match_)

    #print("TAMANHO ", len(found))
    if len(found) == 0:
        return False
    else:
        return match_
        # return found


def isContact_var_CsvHeaders(headers):
    """
    Validate that contact field is in messages template vars list
    :param vars:
    :return:
    """
    # is_contact_present = [<re.Match object; span=(0, 8), match='CONTACTO'>]We have found:  ['contact''] in CSV HEADERS. We will use the number to send message
    found = []
    for header in headers:
        find_this = re.compile("contacto", flags=re.IGNORECASE)
        match = find_this.search(header)
        if match:
            found.append((header,match))
    if len(found) == 0:
        return False, None
    elif len(found) >= 2:
        return True, found
    else:
        return True, found


def getCsvData(file_name):
    """
    this function will try to open a csv file, read its
    contents and export headers, rows, number of rows
    :param file_name: csv filedata
    :return: <tuple> this tuple contains a list of headers, a list with data rows,
    and the number of rows present in the file, Headers line doesn t count.
    """
    with open(file_name, mode="r", newline='') as csv_fstream:
        csv_reader = csv.DictReader(csv_fstream)
        full_csv_data = []
        headers = csv_reader.fieldnames  # ['Nome', 'Contacto', 'morada', 'codigo postal', 'operador'],

        for counter, row in enumerate(csv_reader):
            for header in headers:
                full_csv_data.append(row[header])
        # counter + 1 because counter starts at 0 (we need number of data rows)
        return headers, full_csv_data, counter + 1


def read_raw_data_from_template(file_path):
    """
    It will open a jinja to file and returns a string with jinja 2 file content
    :param file_path: jinja2 file
    :return:
    """
    with open(file_path, "r") as fstream:
        data = fstream.readlines()
    print(type(data), data)
    outdata_str = ""
    for index in range(len(data)):
        if index < len(data):
            outdata_str = outdata_str + data[index].split("\n")[0]
    return outdata_str


def ExtractValidJinja2Variabbles(text=None):
    """
    This function tries to find jinja2 variables in a string
    inside {{ }}
    :param text: <str> a string containing jinja2 strings
    :return: <tuple> with a list containing variables names, and a list with variables in jinja format {{ variable }}
             <None> returns None, if it cant find
    """

    # SOURCE: https://cs.lmu.edu/~ray/notes/regex/
    import re
    if text is None:
        text = r"ola {{ nome }}, hoje está uma noite de luar triste. Talvez na {{ morada }}"
    pattern = r"\{{2}\s*\w*\s*\}{2}"
    results = re.findall(pattern, text, re.MULTILINE)
    if results is None:
        return False
    else:
        vars_names = list()
        for result in results:
            variable_name = result.split("{")[2].split("}")[0].strip()
            vars_names.append(variable_name)
        return vars_names, results





def isContact_valid(contact):
    pattern = "9(1|2|3|6)\d*"
    find_this = re.compile(pattern, flags=re.IGNORECASE)
    match = find_this.search(contact)
    # if match is found
    if match:
        match.group()
        if len(match.group()) != 9:
            return False
        #print(match)
        #print(match.group())
        return match.group()
    else:
        return False


def add_country_number(phone_number, country=None):
    countries = {"PT": "+351"}

    if phone_number is None or not isinstance(phone_number, str):
        raise ValueError("wrong phone number. Phone number should be a string")
    if country is None:
        return countries["PT"] + str(phone_number)
    else:
        for key, value in countries.items():
            if country != key:
                raise ValueError("Country not Found. Please add a valid Country")
        return countries["PT"] + str(phone_number)



# CALLS
#make_data_table()
#read_template("MessageTemplates/promocao1.j2")

# CSV_FULL_PATH = "/home/user/PycharmProjects/TwillioTests/Demostration2/clients_5.csv"
# J2_TEMPLATE = "/home/user/PycharmProjects/TwillioTests/Demostration2/MessageTemplates/OctoberFest.j2"
# CSV_FNAME= "clients_5.csv"
# j2t_name= "OctoberFest.j2"
#
# headers = get_headers(CSV_FULL_PATH)
#
# headers, csv_data = get_csv_data(file_name=CSV_FNAME)
# print(f"[ headers ] {headers}")
# print(f"[ csv_data ] {csv_data}")
#
#
#
# make_data_table(headers=headers, registries = csv_data, csv=CSV_FULL_PATH, j2template=J2_TEMPLATE)
# message = readTemplate(j2t_name, "ANDRE")
# print(message)
#
#
#
# valid_numbers = ["917589898", "929287373", "962020202"]
# invalid_numbers_pm = ["91758989", "92928737", "96202020", "9175898911", "9292873722", "9620202022"]
# invalid_numbers_pm1 = ["249029921", "218282838", "091792112"]
#
# for number in valid_numbers:
#     print("Checking valid_numbers")
#     print("Checking number ", number)
#     result_number = isContact_valid(contact=number)
#     print(result_number)
#     print(repr(result_number))
#     if result_number and not False:
#         final_number = add_country_number(result_number)
#         print("final: ", final_number)