import docker
import subprocess
import os
import time
from src.data_xml_to_json  import xls_parser


class DockerFabric:
    CHANNEL_NAME = "mychannel"
    ORG = "agiletech.vn"

    def __init__(self, *args):
        if len(args) != 1:
            raise ValueError("Accepts only one argument which has to be absolute path to"
                             " hyperledger-fabric-swarm folder")
        # self.abs_path = args
        os.chdir(args[0])

    def start(self):
        # initilize swarm
        command = "docker swarm init"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        if "docker swarm leave" in err.decode('utf8', 'ignore'):
            command = "docker swarm leave --force"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        command = "docker swarm init"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        # Creating an overlay network
        command = "docker network create --attachable --driver overlay --subnet=10.200.1.0/24 hyperledger-ov"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        # Generating artificats
        command = "yarn genConfig -domain agiletech.vn -Kafka 3 -Orderer 2 -Zookeeper 3 -Orgs 2 -Peer 1 -Tag :latest"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        command = "yarn genArtifacts -c mychannel -d agiletech.vn -o 2"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        # starting network
        command = "yarn start"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        # getting all containers
        command = "docker ps -aq"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))
        list_cont = out.decode('utf8', 'ignore').split()

        # for some reason even if docker stop is used containers restart. This fixes the issue
        print("updating the containers so we can stop them")
        for container in list_cont:
            command = "docker update --restart=unless-stopped " + str(container)
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))


        sleep = 30
        while sleep  >0:
            print("Waiting for all containers to start: " + str(sleep) + " seconds left")
            time.sleep(1)
            sleep -= 1

    def find_cli(self):
        cli_container = None
        client = docker.from_env()

        # finding the id of the client container
        for container in client.containers.list(all):
            if "cli_cli" in container.name:
                cli_container = container
        return cli_container

    def create_channel(self):
        cli_container = self.find_cli()

        # creating a channel TODO: fix the variables!!!
        exict_code, output = cli_container.exec_run("peer channel create -o orderer0." + self.ORG + ":7050 -c " +
                                                    self.CHANNEL_NAME +" -f ./channel-artifacts/channel.tx --tls "
                                                    "true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/"
                                                                       "crypto/ordererOrganizations/" +
                                                    self.ORG + "/orderers/orderer0." + self.ORG + "/msp/tlscacerts/"
                                                    "tlsca." + self.ORG + "-cert.pem",
                                                    stream=True)
        for line in output:
            print("create_channel: " + str(line))

    def join_channel(self):
        cli_container = self.find_cli()

        exict_code, output = cli_container.exec_run("peer channel join -b " + self.CHANNEL_NAME + ".block", stream=True)
        for line in output:
            print(line)

        exict_code, output = cli_container.exec_run("peer channel list", stream=True)
        for line in output:
            print("join_channel: " + str(line))

    def install_chaincode(self):
        cli_container = self.find_cli()

        exict_code, output = cli_container.exec_run(" peer chaincode install -n mycc -v 1.0 -p github.com/hyperledger"
                                                    "/fabric/examples/chaincode/go/sacc", stream=True)
        for line in output:
            print(str(line))

        exict_code, output = cli_container.exec_run(
            "peer chaincode instantiate -o orderer0." + self.ORG + ":7050 --tls true"
            " --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto"
            "/ordererOrganizations/" + self.ORG + "/orderers/orderer0." + self.ORG +
            "/msp/tlscacerts/tlsca." + self.ORG + "-cert.pem -C " + self.CHANNEL_NAME +
            " -n mycc -v 1.0 -c '{\"Args\":[\"a\", \"100\"]}'", stream=True)
        for line in output:
            print("install_chaincode: " + str(line))

    def query_entry(self, userID):
        cli_container = self.find_cli()
        exict_code, output = cli_container.exec_run("peer chaincode query -C " + self.CHANNEL_NAME + " -n mycc "
                                                    "-c '{\"Args\":[\"query\",\"" + userID + "\"]}'", stream=True)
        for line in output:
            print("query_entry: " + str(line))

    def set_entry(self, userID , certificate):
        cli_container = self.find_cli()
        exict_code, output = cli_container.exec_run(
            "peer chaincode invoke -o orderer1." + self.ORG + ":7050 --tls true --cafile /opt/gopath/src/github.com/"
            "hyperledger/fabric/peer/crypto/ordererOrganizations/" + self.ORG + "/orderers/orderer1." + self.ORG + "/msp"
            "/tlscacerts/tlsca." + self.ORG + "-cert.pem -C " + self.CHANNEL_NAME + " -n mycc -c "
            "'{\"Args\":[\"set\",\"" + userID + "\",\"" + certificate + "\"]}'", stream=True)
        for line in output:
            print("set_entry: " + str(line))

    def close(self):
        # containers
        command = "docker ps -aq"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))
        list_cont = out.decode('utf8', 'ignore').split()

        # for some reason even if docker stop is used containers restart. This fixes the issue
        for container in list_cont:
            command = "docker update --restart=unless-stopped " + str(container)
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        # stopping containers
        print("Stopping containers")
        for container in list_cont:
            command = "docker stop " + str(container)
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        print("Removing containers")
        # removing containers
        for container in list_cont:
            command = "docker rm -f " + str(container)
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        # containers
        command = "docker ps -aq"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))


if __name__ == "__main__":
    dir = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, os.path.pardir))
    # print(dir)
    # dir_path = dir + "/Certificates_Origin/XLS_data/Xantrex_Inverter_Data.zip.gpg"
    # parser = xls_parser(dir_path)
    # parser.close()
    # xls_files = parser.decrypt_and_unzip()
    # list_of_certificates = parser.extract_from_xls(xls_files)
    # parser.create_json(list_of_certificates)
    # print(list_of_certificates)


    dir = dir + "/hyperledger-fabric-swarm"
    docker_controller = DockerFabric(dir)
    # docker_controller.start()
    # docker_controller.create_channel()
    # docker_controller.join_channel()
    # docker_controller.install_chaincode()
    #
    # ## For test
    # docker_controller.query_entry("a")
    # docker_controller.set_entry("a", "10")
    docker_controller.query_entry("a")
    # docker_controller.close()
