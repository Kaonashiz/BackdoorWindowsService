import servicemanager
import win32serviceutil
import win32service
import win32api
from os import *
import ctypes


if __name__ == '__main__':
    # Defina um ouvinte para o servicemanager do Windows.
    servicemanager.Initialize()
    # passe um manipulador de classe de serviço, para que sempre que recebermos um sinal do servicemanager, iremos passá-lo para a classe de serviço.
    servicemanager.PrepareToHostSingle(Service)
    servicemanager.StartServiceCtrlDispatcher()
    win32serviceutil.HandleCommandLine(Service) 

class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = 'ScsiAccess'
    _svc_display_name_ = 'ScsiAccess'

    def __init__(self, *args):
        # Inicializa o ServiceFramework e define, em estilo de funções, o que fazer quando um sinal do service manager for recebido.
        win32serviceutil.ServiceFramework.__init__(self, *args)

    def sleep(self, sec):
        # Se o sinal do gerenciador de serviços foi pause - então executa o sleep por uma quantidade de segundos.
        win32api.Sleep(sec*800, True)

    def SvcDoRun(self):
        # Se o sinal recebido foi de início, então:
        # Informa o Service Manager que estamos planejando executar o serviço, informando de volta um status pendente de início.
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            # Avise ao Gerenciador de Serviços que estamos atualmente iniciando o serviço e depois chame a função start(). Se ocorrer alguma exceção, chamaremos a função stop() para encerrar o serviço.
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.start()
        except Exception as x:
            self.SvcStop()

    def SvcStop(self):
        # Informa o Service Manager que estamos planejando parar o serviço.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stop()
        # Indica ao Gerenciador de Serviços que estamos atualmente parando o serviço.
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def start(self):
        # marcar uma flag de status do serviço como Verdadeiro e aguardaremos em um loop while para receber o sinal de parada do serviço do gerenciador de serviços.
        self.runflag = True

        f = open('C:/Users/nonadmin/Desktop/priv.txt', 'w')
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            f.write('[-] CONEXÃO FALHOU! ')
        else:
            f.write('[+] CONEXÃO FEITA COM SUCESSO! ')
        f.close()
        
        # Aguardar o sinal de parada do serviço.
        while self.runflag:
            self.sleep(8)

    def stop(self):
        # Marcar a flag de status do serviço como False para interromper o loop while na função start.
        self.runflag = False
