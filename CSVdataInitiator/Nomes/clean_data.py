import sys

def load_data_from_file(file_path):
    try:
        with open(file_path, "rt") as fstream:
            data = fstream.readlines()
            data = [name.split("\n")[0] for name in data]
            return data
    except OSError as error:
        sys.exit(f"Error, while attempting to open/ read file {file_path}\n ERROR: {error}")


data = load_data_from_file("nomesMasculinos.data")
print(repr(data))
clean_one = []
for index, element in enumerate(data):
    if index==0:
        clean_one.append(element)
    else:
        clean_one.append(element.strip())
    with open("nomesMasculinos.data", "w") as fstream_out:
        for row in clean_one:
            fstream_out.write(row)
            fstream_out.write("\n")




