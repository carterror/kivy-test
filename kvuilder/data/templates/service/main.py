from os.path import join
from time import sleep

from kivy.storage.dictstore import DictStore

from kivy import Logger
from libs.core.rpc import API, send_message

try:
    from android.storage import app_storage_path
    from jnius import autoclass

    PythonService = autoclass('org.kivy.android.PythonService')
    PythonService.mService.setAutoRestartService(True)
except ImportError:
    app_storage_path = lambda : './'


class ${nama_program}Service:
    def __init__(self):
        self.store = DictStore(join(app_storage_path(), 'storage.bin'))
        self.api = API(objects={'storage':self.store}, port=3000, callback=self.callback)
        
    def callback(self):
        Logger.info('${nama_program}Service: callback works!')
        

if __name__ == '__main__':
    try:
        service = ${nama_program}Service()
        Logger.info(f'${nama_program}Service: Service initialization complete')
        service.api.register_agent(('127.0.0.1', 3001), description='${nama_program}Controller')
        Logger.info(f'${nama_program}Service: Notifying to ${nama_program}Controller for connection')
        service.api.emit()
        while True:
            sleep(1)
    except Exception as e:
        Logger.error(f'${nama_program}Service: Error in class ${nama_program}Service')
        Logger.error(f'${nama_program}Service: Exception {e}')
        
