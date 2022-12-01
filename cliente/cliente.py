from pyModbusTCP.client import ModbusClient
from time import sleep
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder


class ClienteMODBUS():
    """
    Classe Cliente MODBUS
    """

    def __init__(self, server_ip, porta, scan_time=1):
        """
        Construtor
        """
        self._cliente = ModbusClient(host=server_ip, port=porta)
        self._scan_time = scan_time

    def atendimento(self):
        """
        Método para atendimento do usuário
        """
        self._cliente.open()
        try:
            atendimento = True
            while atendimento:

                sel = input(
                    "\nDeseja realizar uma leitura, escrita ou configuração? (1- Leitura | 2- Escrita | 3- Configuração |4- Sair): "
                )

                if sel == '1':

                    op = input(
                        """\nQual tipo de dado deseja ler? (1- float |2- string): """
                    )
                    addr = input(f"Digite o endereço da tabela MODBUS: ")

                    if op == '1':

                        print(f"Leitura: {self.lerDado(int(op), int(addr))}")
                        # nvezes = input ("Digite o número de vezes que deseja ler: ")
                        # for i in range(0,int(nvezes)):
                        #     print(f"Leitura {i+1}: {self.lerDado(1, int(addr))}")
                        sleep(self._scan_time)

                    elif op == '2':
                        print(f"Leitura: {self.lerDado(int(op), int(addr))}")

                    else:
                        print("Seleção invalida")

                elif sel == '2':

                    op = input(
                        """\nQual tipo de dado deseja escrever? (1- float | 2- string): """
                    )
                    addr = input(f"Digite o endereço da tabela MODBUS: ")
                    if op == '1':
                        valor = input(f"Digite o valor que deseja escrever: ")
                        self.escreveDado(1, int(addr), float(valor),0)

                    elif op == '2':
                        valor = input(f"Digite a string que deseja escrever: ")
                        self.escreveDado(2, int(addr), str(valor), int(len(str(valor))))

                    else:
                        print("Seleção invalida")

                elif sel == '3':
                    scant = input("Digite o tempo de varredura desejado [s]: ")
                    self._scan_time = float(scant)

                elif sel == '4':
                    self._cliente.close()
                    atendimento = False
                else:
                    print("Seleção inválida")
        except Exception as e:
            print('Erro no atendimento: ', e.args)

    def lerDado(self, tipo, addr):
        """
        Método para leitura de um dado da Tabela MODBUS
        """
        if tipo == 1:  #Float
            leitura = self._cliente.read_holding_registers(addr, 2)
            decoder = BinaryPayloadDecoder.fromRegisters(leitura)
            return decoder.decode_32bit_float()
            #return self._cliente.read_holding_registers(addr,1)[0]

        if tipo == 2:  #String
            tamStr = self._cliente.read_holding_registers(int(addr)-1,2)[0]
            leitura = self._cliente.read_holding_registers(addr, tamStr)
            decoder = BinaryPayloadDecoder.fromRegisters(leitura)
            #tamStr = int(tamStr)
            return str(decoder.decode_string(tamStr))[1:]

        # if tipo == 1:
        #     return self._cliente.read_input_registers(addr,1)[0]

        # if tipo == 1:
        #     return self._cliente.read_discrete_inputs(addr,1)[0]

    def escreveDado(self, tipo, addr, valor, tamStr):
        """
        Método para a escrita de dados na Tabela MODBUS
        """
        if tipo == 1:  #Float
            builder = BinaryPayloadBuilder()
            builder.add_32bit_float(float(valor))
            payload = builder.to_registers()
            return self._cliente.write_multiple_registers(addr, payload)

        elif tipo == 2: #String
            self._cliente.write_single_register(addr-1,tamStr)
            builder = BinaryPayloadBuilder()
            builder.add_string(valor)
            payload = builder.to_registers()
            return self._cliente.write_multiple_registers(addr, payload)
