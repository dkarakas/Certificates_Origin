import docker
import subprocess
import os

class fabric_docker:

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
        command = "yarn genConfig -domain agiletech.vn -Kafka 3 -Orderer 2 -Zookeeper 3 -Orgs 2 -Peer 1 -Tag :x86_64-1.1.0-preview"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        command = "yarn genArtifacts -c mychannel -d agiletech.vn -o 2"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

        #starting network
        command = "yarn start"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))

    def create_channel(self):
        cli_container = None
        client = docker.from_env()

        #finding the id of the client container
        for container in client.containers.list(all):
            if "cli_cli" in container.name:
                cli_container = container
        print(cli_container)
        ret = cli_container.exec_run("bash CHANNEL_NAME=mychannel")
        print(ret.output.decode('utf8', 'ignore'))
        ret = cli_container.exec_run("bash export CHANNEL_NAME")
        print(ret.output.decode('utf8', 'ignore'))
        ret = cli_container.exec_run("sh export ORG=agiletech.vn")
        print(ret.output.decode('utf8', 'ignore'))
        ret = cli_container.exec_run("peer channel create -o orderer0.${ORG}:7050 -c $CHANNEL_NAME "
                                     "-f ./channel-artifacts/channel.tx --tls true --cafile"
                                     " /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations"
                                     "/$ORG/orderers/orderer0.${ORG}/msp/tlscacerts/tlsca.${ORG}-cert.pem")
        print(ret.output.decode('utf8', 'ignore'))


    def close(self):
        #containers
        command = "docker ps -aq"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))
        list_cont = out.decode('utf8', 'ignore').split()

        # print(process.stdout)
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

        #containers
        command = "docker ps -aq"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print(out.decode('utf8', 'ignore') + " " + err.decode('utf8', 'ignore'))


if __name__ == "__main__":
    dir = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, os.path.pardir))
    dir = dir + "/hyperledger-fabric-swarm"
    docker_controller = fabric_docker(dir)
    # docker_controller.start()
    docker_controller.create_channel()
    # docker_controller.close()