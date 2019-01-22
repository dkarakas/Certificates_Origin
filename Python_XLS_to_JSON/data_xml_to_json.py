import subprocess
import os, glob
import re

class xml_parser:
    def __init__(self, file_loc):
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
        """
        attempts = 3

        while(self.decrypted == False and attempts > 0):
            password = input("Enter password to decrypt file:")

            command = "echo " + password
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            command = "gpg --batch --yes --passphrase-fd 0 " + self.file_location
            process = subprocess.Popen(command.split(), stdin=process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    dir_path = dir_path + "/XLS_data/Xantrex_Inverter_Data.zip.gpg"
    parser = xml_parser(dir_path)
    parser.decrypt_and_unzip()
    # parser.close()