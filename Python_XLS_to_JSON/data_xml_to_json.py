import subprocess
import os
import glob
import re
import xlrd
import pandas as pd


class xml_parser:
    def __init__(self, file_loc):
        if (file_loc[-3:] != "gpg"):
            raise ValueError("The script accepts only encrypted input")
            return
        self.file_location = file_loc
        self.decrypted = False

    def __del__(self):
        pass
        # for file in glob.glob(os.path.dirname(self.file_location[:-4]) + "/*.xls"):
        #     command = "rm " + file
        #     process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     output = process.communicate()
        #     print("File deleted: " + output)

    def close(self):
        types_of_files = ["zip", "xls"]
        for type in types_of_files:
            for file in glob.glob(os.path.dirname(self.file_location[:-4]) + "/*." + type):
                subprocess.Popen(["rm", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("File deleted: " + str(file))

    def decrypt_and_unzip(self):
        """
        Decrypts and unzips the file.
        :return: A list of xls files that have been decrypted
        """
        attempts = 3
        xml_files = list()

        while (self.decrypted == False and attempts > 0):
            password = input("Enter password to decrypt file:")

            command = "echo " + password
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            command = "gpg --batch --yes --passphrase-fd 0 " + self.file_location
            process = subprocess.Popen(command.split(), stdin=process.stdout, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

            output = process.communicate()
            if "failed" in str(output[1]):
                print("Decryption of data failed!")
                print("Please, try again!")
                attempts -= 1
            else:
                print("Successful decryption!")
                self.decrypted = True

        if not self.decrypted:
            raise ValueError("Please. make sure you know the PIN!")

        command = "unzip " + self.file_location[:-4] + " -d " + os.path.dirname(self.file_location[:-4])
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()

        files_unzipped = re.findall(r'([^/]+?)(xls|zip)', str(output[0]))

        for file, extension in files_unzipped:
            print("File created " + file + extension)
            match = re.search("Data Log [0-9]{2}-[0-9]{2}-[0-9]{4}\.xls", file + extension)
            # adds only xls files with daily log
            if match and extension == "xls":
                xml_files.append(file + extension)
        return xml_files

    def fix_file(self, abs_file):
        with open(abs_file, 'r+b') as file:
            content = file.readlines()  # not very good on memory
            print(content)
            print(content[2:])
            file.writelines(content[2:])

    def extract_from_xml(self, xml_files):
        for xml_file in xml_files:
            xml_file = os.path.dirname(self.file_location) + "/" + xml_file
            print(xml_file)
            self.fix_file(xml_file)  # first line of each file corrupts the xml format and that is why here it is removed

            # workbook = xlrd.open_workbook(xml_file)
            # print(workbook.sheet_names())
            return
            # with open(os.path.dirname(self.file_location) + "/" + xml_file, 'rb') as file:
            #     content = file.read()
            #     each_row = content.decode('utf8', 'ignore').split('\t')
            #     for row in each_row[1:]:
            #         print(row)
            # return

            # print(os.path.dirname(self.file_location) + "/" + file)
            # read = pd.read_csv(os.path.dirname(self.file_location) + "/" + file)
            # print(read)


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    dir_path = dir_path + "/XLS_data/Xantrex_Inverter_Data.zip.gpg"
    parser = xml_parser(dir_path)
    parser.close()
    xml_files = parser.decrypt_and_unzip()
    parser.extract_from_xml(xml_files)
    parser.close()
