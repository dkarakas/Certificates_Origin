import subprocess
import os
import glob
import re
import xlrd
import certificate
import pandas as pd


class xls_parser:
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
        xls_files = list()

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
                xls_files.append(file + extension)
        return xls_files

    def fix_first_line(self, abs_file):
        """
        :param abs_file: It is the absolute path to the file
        :return:
        """
        with open(abs_file, 'r+b') as file:
            content = file.readlines()  # not very good on memory
            file.truncate(0)
            file.seek(0)  # otherwise the beginning of the file will be filled with null
            file.writelines(content[2:])

    def extract_manually(self, abs_file):
        """
        Extracts the information from the xls file mannually
        :param abs_file: It is the absolute path to the file
        :return: a list of certificates of origin for each reading
        """
        print("Attempting to extract data manually from the file!")
        content = None
        list_of_certificates = list()
        with open(abs_file, 'r+b') as file:
            content = file.readlines()  # not very good on memory
        content = list(line.decode('utf8', 'ignore').strip() for line in content)
        print(content)


    def extract_from_xls(self, xls_files):
        for xls_file in xls_files:
            xls_file = os.path.dirname(self.file_location) + "/" + xls_file
            print(xls_file)
            self.fix_first_line(xls_file)  # first line of each file corrupts the xls format and that is why here it is removed

            try:
                #TODO: implement code with non corrupted file
                workbook = xlrd.open_workbook(xls_file)
                # print(workbook.sheet_names())
            except xlrd.XLRDError as er:  # although Libre Office recognizes the file, xlrd doesn't recognize it.
                print(er)
                self.extract_manually(xls_file)

            return


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    dir_path = dir_path + "/XLS_data/Xantrex_Inverter_Data.zip.gpg"
    parser = xls_parser(dir_path)
    parser.close()
    xls_files = parser.decrypt_and_unzip()
    parser.extract_from_xls(xls_files)
    # parser.close()
