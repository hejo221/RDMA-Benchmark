import os
import time
import paramiko

os.system("")

GREEN = "\033[32m"
BLUE = "\033[34m"
RED = "\033[31m"
RESET = "\033[0m"

conn_flag = 0
host1 = ""
host2 = ""

ssh_client1 = paramiko.SSHClient()
ssh_client2 = paramiko.SSHClient()


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def display_welcome_msg():
    print(GREEN + "**************************************************************")
    print(GREEN + "                       Welcome to RDMA-Bench                  ")
    print(GREEN + "**************************************************************" + RESET)


def show_main_menu():
    global conn_flag

    print("Please select one of the available options: ")
    print("[1] Establish connection to servers")
    print("[2] Run benchmarks for InfiniBand connections")
    print("[3] Run benchmarks for RoCE connections")
    print("[4] Exit the tool")

    print()
    option = int(input(BLUE + "Please enter the number of your chosen option: " + RESET))

    if option == 2 or option == 3:
        if conn_flag == 0:
            clear_console()
            print(RED + "You first need to connect to the servers before running benchmarks!" + RESET)
            print()
            show_main_menu()
        elif option == 2:
            clear_console()
            show_ib_menu()
        elif option == 3:
            clear_console()
            show_roce_menu()
    elif option == 1:
        clear_console()
        establish_connections()
    elif option == 4:
        print(RED + "You will now exit this tool." + RESET)
        if conn_flag == 1:
            close_connections()
        conn_flag = 0
        time.sleep(3)
        quit()

def establish_connections():
    global conn_flag
    global ssh_client1
    global ssh_client2
    global host1
    global host2

    print("You will now establish connections to the servers:")

    host1 = input("Enter the IP address of server 1: ")
    user1 = input("Enter your username on server 1: ")
    pwd1 = input("Enter your password on server 1: ")

    print()

    host2 = input("Enter the IP address of server 2: ")
    user2 = input("Enter your username on server 2: ")
    pwd2 = input("Enter your password on server 2: ")

    print()

    ssh_client1 = paramiko.SSHClient()
    ssh_client1.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client1.connect(hostname=host1, port=22, username=user1, password=pwd1)
    time.sleep(1)
    print("The connection with server 1 has now been established.")

    ssh_client2 = paramiko.SSHClient()
    ssh_client2.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client2.connect(hostname=host2, port=22, username=user2, password=pwd2)
    time.sleep(1)
    print("The connection with server 2 has now been established.")

    conn_flag = 1
    time.sleep(1)

    print(RED + "You will be taken back to the main menu where you can run the benchmarks." + RESET)
    print()

    time.sleep(5)


    show_main_menu()


def close_connections():
    ssh_client1.close()
    ssh_client2.close()


def show_ib_menu():
    print("Please select one of the available options: ")
    print("[1] Run Write Bandwidth Benchmark (InfiniBand)")
    print("[2] Run Read Bandwidth Benchmark (InfiniBand)")
    print("[3] Run Latency Benchmark (InfiniBand)")
    print("[4] Return to main menu")

    ib_option = int(input(BLUE + "Please enter the number of your chosen option: " + RESET))

    if ib_option == 1:
        clear_console()
        ib_write_bench()
    elif ib_option == 2:
        clear_console()
        ib_read_bench()
    elif ib_option == 3:
        clear_console()
        ib_lat_bench()
    elif ib_option == 4:
        clear_console()
        print(RED + "You will be taken back to the main menu where you can run the benchmarks." + RESET)
        time.sleep(3)
        show_main_menu()


def show_roce_menu():
    print("Please select one of the available options: ")
    print("[1] Run Write Bandwidth Benchmark (RoCE)")
    print("[2] Run Read Bandwidth Benchmark (RoCE)")
    print("[3] Run Latency Benchmark (RoCE)")
    print("[4] Return to main menu")

    roce_option = int(input(BLUE + "Please enter the number of your chosen option: " + RESET))

    if roce_option == 1:
        clear_console()
        ib_write_bench()
    elif roce_option == 2:
        clear_console()
        ib_read_bench()
    elif roce_option == 3:
        clear_console()
        ib_lat_bench()
    elif roce_option == 4:
        clear_console()
        print(RED + "You will be taken back to the main menu where you can run the benchmarks." + RESET)
        time.sleep(3)
        show_main_menu()


def ib_write_bench():
    global host1

    data_sizes = []
    exponent = 1

    print("The following devices have been found: ")
    get_ib_dev_info()
    print()
    ibw_device = input(BLUE + "Please enter the name of the device that you want to use for the benchmark: " + RESET)
    data_size = int(input(BLUE + "Please enter the maximum exponent to the base 2 for the payload size: " + RESET))

    while exponent <= data_size:
        data_sizes.append(2**exponent)
        exponent += 1

    for size in data_sizes:
        print(RED + "The benchmark is now running. This might take a while to  complete!" + RESET)
        stdin, stdout, stderr = ssh_client1.exec_command("ib_write_bw -d {} -s {}".format(ibw_device, size))
        while not stdout.channel.exit_status_ready():
            time.sleep(5)
            stdin, stdout, stderr = ssh_client2.exec_command("ib_write_bw {} -d {} -s {}".format(host1, ibw_device, size))
            with open("benchmark_results.txt", "a") as file:
                file.write("\n")
                file.write("Connection Type: InfiniBand\n")
                file.writelines(stdout.readlines())

    clear_console()
    print(GREEN + "The benchmark is now finished. You can find the results in benchmark_results.txt" + RESET)
    print()
    print(RED + "You will be taken back to the main menu." + RESET)
    show_main_menu()


def ib_read_bench():
    global host1

    data_sizes = []
    exponent = 1

    print("The following devices have been found: ")
    get_ib_dev_info()
    print()
    ibw_device = input(BLUE + "Please enter the name of the device that you want to use for the benchmark: " + RESET)
    data_size = int(input(BLUE + "Please enter the maximum exponent to the base 2 for the payload size: " + RESET))

    while exponent <= data_size:
        data_sizes.append(2**exponent)
        exponent += 1

    for size in data_sizes:
        print(RED + "The benchmark is now running. This might take a while to  complete!" + RESET)
        stdin, stdout, stderr = ssh_client1.exec_command("ib_read_bw -d {} -s {}".format(ibw_device, size))
        while not stdout.channel.exit_status_ready():
            time.sleep(5)
            stdin, stdout, stderr = ssh_client2.exec_command("ib_read_bw {} -d {} -s {}".format(host1, ibw_device, size))
            with open("benchmark_results.txt", "a") as file:
                file.write("\n")
                file.write("Connection Type: InfiniBand\n")
                file.writelines(stdout.readlines())

    clear_console()
    print(GREEN + "The benchmark is now finished. You can find the results in benchmark_results.txt" + RESET)
    print()
    print(RED + "You will be taken back to the main menu." + RESET)
    show_main_menu()


def ib_lat_bench():
    global host1

    data_sizes = []
    exponent = 1

    print("The following devices have been found: ")
    get_ib_dev_info()
    print()
    ibw_device = input(BLUE + "Please enter the name of the device that you want to use for the benchmark: " + RESET)
    data_size = int(input(BLUE + "Please enter the maximum exponent to the base 2 for the payload size: " + RESET))

    while exponent <= data_size:
        data_sizes.append(2**exponent)
        exponent += 1

    for size in data_sizes:
        print(RED + "The benchmark is now running. This might take a while to  complete!" + RESET)
        stdin, stdout, stderr = ssh_client1.exec_command("ib_write_lat -d {} -s {}".format(ibw_device, size))
        while not stdout.channel.exit_status_ready():
            time.sleep(5)
            stdin, stdout, stderr = ssh_client2.exec_command("ib_write_lat {} -d {} -s {}".format(host1, ibw_device, size))
            with open("benchmark_results.txt", "a") as file:
                file.write("\n")
                file.write("Connection Type: InfiniBand\n")
                file.writelines(stdout.readlines())

    clear_console()
    print(GREEN + "The benchmark is now finished. You can find the results in benchmark_results.txt" + RESET)
    print()
    print(RED + "You will be taken back to the main menu." + RESET)
    show_main_menu()


def roce_write_bench():
    global host1

    data_sizes = []
    exponent = 1

    print("The following devices have been found: ")
    get_ib_dev_info()
    print()
    ibw_device = input(BLUE + "Please enter the name of the device that you want to use for the benchmark: " + RESET)
    data_size = int(input(BLUE + "Please enter the maximum exponent to the base 2 for the payload size: " + RESET))

    while exponent <= data_size:
        data_sizes.append(2 ** exponent)
        exponent += 1

    for size in data_sizes:
        print(RED + "The benchmark is now running. This might take a while to  complete!" + RESET)
        stdin, stdout, stderr = ssh_client1.exec_command("ib_write_bw -d {} -s {}".format(ibw_device, size))
        while not stdout.channel.exit_status_ready():
            print("Test")
            time.sleep(5)
            stdin, stdout, stderr = ssh_client2.exec_command(
                "ib_write_bw {} -d {} -s {}".format(host1, ibw_device, size))
            with open("benchmark_results.txt", "a") as file:
                file.write("\n")
                file.write("Connection Type: RoCE\n")
                file.writelines(stdout.readlines())

    clear_console()
    print(GREEN + "The benchmark is now finished. You can find the results in benchmark_results.txt" + RESET)
    print()
    print(RED + "You will be taken back to the main menu." + RESET)
    show_main_menu()


def roce_read_bench():
    global host1

    data_sizes = []
    exponent = 1

    print("The following devices have been found: ")
    get_ib_dev_info()
    print()
    ibw_device = input(BLUE + "Please enter the name of the device that you want to use for the benchmark: " + RESET)
    data_size = int(input(BLUE + "Please enter the maximum exponent to the base 2 for the payload size: " + RESET))

    while exponent <= data_size:
        data_sizes.append(2**exponent)
        exponent += 1

    for size in data_sizes:
        print(RED + "The benchmark is now running. This might take a while to  complete!" + RESET)
        stdin, stdout, stderr = ssh_client1.exec_command("ib_read_bw -d {} -s {}".format(ibw_device, size))
        while not stdout.channel.exit_status_ready():
            print("Test")
            time.sleep(5)
            stdin, stdout, stderr = ssh_client2.exec_command("ib_read_bw {} -d {} -s {}".format(host1, ibw_device, size))
            with open("benchmark_results.txt", "a") as file:
                file.write("\n")
                file.write("Connection Type: RoCE\n")
                file.writelines(stdout.readlines())

    clear_console()
    print(GREEN + "The benchmark is now finished. You can find the results in benchmark_results.txt" + RESET)
    print()
    print(RED + "You will be taken back to the main menu." + RESET)
    show_main_menu()


def roce_lat_bench():
    global host1

    data_sizes = []
    exponent = 1

    print("The following devices have been found: ")
    get_ib_dev_info()
    print()
    ibw_device = input(BLUE + "Please enter the name of the device that you want to use for the benchmark: " + RESET)
    data_size = int(input(BLUE + "Please enter the maximum exponent to the base 2 for the payload size: " + RESET))

    while exponent <= data_size:
        data_sizes.append(2**exponent)
        exponent += 1

    for size in data_sizes:
        print(RED + "The benchmark is now running. This might take a while to  complete!" + RESET)
        stdin, stdout, stderr = ssh_client1.exec_command("ib_write_lat -d {} -s {}".format(ibw_device, size))
        while not stdout.channel.exit_status_ready():
            time.sleep(5)
            stdin, stdout, stderr = ssh_client2.exec_command("ib_write_lat {} -d {} -s {}".format(host1, ibw_device, size))
            with open("benchmark_results.txt", "a") as file:
                file.write("\n")
                file.write("Connection Type: RoCE\n")
                file.writelines(stdout.readlines())

    clear_console()
    print(GREEN + "The benchmark is now finished. You can find the results in benchmark_results.txt" + RESET)
    print()
    print(RED + "You will be taken back to the main menu." + RESET)
    show_main_menu()


def get_ib_dev_info():
    stdin, stdout, stderr = ssh_client1.exec_command("ibv_devinfo")
    output = stdout.read().decode()
    lines = output.split('\n')

    for line in lines:
        if line.startswith('hca_id'):
            parts = line.split(':')
            hca_id = parts[1].strip()
            print(hca_id)


def main():
    display_welcome_msg()
    show_main_menu()


main()