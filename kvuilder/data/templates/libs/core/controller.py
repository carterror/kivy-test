import plyer

from kivy import Logger
from kivy.event import EventDispatcher
from kivy.utils import platform

from libs.core.rpc import API, send_message

if platform == 'android':
    import android

SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
        packagename=u'org.test',
        servicename=u'${nama_program}'
)


class Controller(EventDispatcher):
    
    def __init__(self, app):
        """

        :param app:
        :type app: chat.MainApp
        """
        self.app = app
        self.api = API(port=3001, callback=self.service_connect)
    
    def service_start(self):
        Logger.info(f"${nama_program}Controller: calling service start")
        if platform == 'android':
            from jnius import autoclass
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            service = autoclass(SERVICE_NAME)
            argument = ''
            service.start(mActivity, argument)
        elif platform in ('linux', 'linux2', 'macos', 'win'):
            from runpy import run_path
            from threading import Thread
            self.service = Thread(
                    target=run_path,
                    args=['service/main.py'],
                    kwargs={'run_name': '__main__'},
                    daemon=True
            )
            self.service.start()
        else:
            Logger.error(f"${nama_program}Controller: service start not implemented on this platform")
            raise NotImplementedError(
                    "service start not implemented on this platform"
            )
    
    def service_connect(self):
        self.api.register_agent(('127.0.0.1', 3000), description='${nama_program}Service')
        send_message(b'/register', values=[('127.0.0.1', 3001), '${nama_program}Controller'], ip_address='127.0.0.1', port=3000)
    
    def service_disconnect(self):
        self.api.emit(callback=b'/reset')
    
    def test_notify(self):
        plyer.notification.notify(title='test', message="Notification using plyer")
