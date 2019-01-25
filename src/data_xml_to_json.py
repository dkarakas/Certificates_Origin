import subprocess
import os
import glob
import re
import xlrd
from src.certificate import certificate_origin
import json
# import pandas as pd

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))                 # Path to global dir
dir_of_certs = dir_path + "/certs/"                                                     # Path to dir of certificates


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
        print("Attempting to extract data manually from the xls files!")
        list_of_certificates = list()
        with open(abs_file, 'r+b') as file:
            content = file.readlines()  # not very good on memory
        content = list(line.decode('utf8', 'ignore').strip() for line in content)
        serial_number = re.search(r' = ([a-zA-Z0-9]+)', content[3]).group(1)
        for measurement in content[13:]:
            measurement = list(element.strip() for element in measurement.split('\t'))
            cert_for_measurement = certificate_origin()
            cert_for_measurement.issuer = "TODO_Name" # TODO: actual issuer
            cert_for_measurement.time = measurement[1]
            cert_for_measurement.date = measurement[0]
            cert_for_measurement.source_energy = "solar"  # TODO: allow for more
            cert_for_measurement.identity = serial_number
            cert_for_measurement.capacity = "5 kWh"  # TODO: WHAT IS SUPPOSED TO BE THE CAPACITY
            cert_for_measurement.commissioning_date = "01-23-2018"  # TODO: fix this currently random date
            cert_for_measurement.loc_of_gen = "Waterloo"
            cert_for_measurement.units = measurement[7] + " AC Wh" # TODO: temperory since this is only a snapshot
            cert_for_measurement.other_options = "TODO: TO add"
            list_of_certificates.append(cert_for_measurement)
        return list_of_certificates

    def create_json(self, list_of_certificates):
        """
        :param list_of_certificates:  certificates should be passed from the function decrypt_and_unzip
                                        # TODO: You should be able to generate the jason from folder of certs
        :return: list of jsons parsed from the certificates
        """
        jsons_from_cert = list()
        if not os.path.exists(dir_of_certs):
            os.makedirs(dir_of_certs)
        for one_cert in list_of_certificates:
            cert = one_cert.create_json()
            jsons_from_cert.append(cert)
            file_name = dir_of_certs + one_cert.identity + "_" + one_cert.date + "_" + one_cert.time + ".cert"
            with open(file_name, "w+") as file:
                json.dump(cert, file)
        print("Certificates created in folder certs!")
        return jsons_from_cert

    def extract_from_xls(self, xls_files):
        for xls_file in xls_files:
            list_of_certificates = None
            xls_file = os.path.dirname(self.file_location) + "/" + xls_file
            self.fix_first_line(xls_file)  # first line of each file corrupts the xls format and that is why here it is removed
            try:
                #TODO: implement code with non corrupted file
                workbook = xlrd.open_workbook(xls_file)
            except xlrd.XLRDError as er:  # although Libre Office recognizes the file, xlrd doesn't recognize it.
                print(er)
                list_of_certificates = self.extract_manually(xls_file)
            return list_of_certificates  # TODO: for now return ealry or too many certificates will be created!


if __name__ == '__main__':
    dir_path = dir_path + "/XLS_data/Xantrex_Inverter_Data.zip.gpg"
    parser = xls_parser(dir_path)
    parser.close()
    xls_files = parser.decrypt_and_unzip()
    list_of_certificates = parser.extract_from_xls(xls_files)
    parser.create_json(list_of_certificates)
    # parser.close()
