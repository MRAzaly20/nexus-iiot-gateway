# simple_master.py
import time
from pydnp3 import opendnp3, asiodnp3, asiopal, openpal


class SimpleSOEHandler(opendnp3.ISOEHandler):
    """ Handler untuk data (Sequence of Events) dari Outstation """
    def __init__(self):
        super().__init__()

    def Process(self, info, values):
        # Loop semua data yang diterima
        def log_item(v):
            print(f"[SOE] Header={info.gv}, Index={v.index}, Value={v.value}")
        values.Foreach(log_item)


class SimpleMasterApp(opendnp3.IMasterApplication):
    """ Handler untuk event aplikasi Master """
    def __init__(self):
        super().__init__()

    def OnOpen(self):
        print("[MasterApp] Channel opened")

    def OnClose(self):
        print("[MasterApp] Channel closed")

    def OnTaskComplete(self, info):
        print(f"[MasterApp] Task completed: {info.result}")


def main():
    HOST = "127.0.0.1"
    PORT = 20000

    # Buat Manager
    manager = asiodnp3.DNP3Manager(1)

    # Channel TCP ke Outstation
    channel = manager.AddTCPClient(
        "master-channel",
        opendnp3.levels.NORMAL | opendnp3.levels.ALL_COMMS,
        asiopal.ChannelRetry.Default(),
        HOST,
        "0.0.0.0",
        PORT,
        asiodnp3.PrintingChannelListener().Create()
    )

    # Konfigurasi stack
    stack_config = asiodnp3.MasterStackConfig()
    stack_config.master.responseTimeout = openpal.TimeDuration().Seconds(2)
    stack_config.link.RemoteAddr = 10  # alamat Outstation

    # Tambahkan Master
    master = channel.AddMaster(
        "master",
        SimpleSOEHandler(),
        SimpleMasterApp(),
        stack_config
    )

    # Aktifkan komunikasi
    master.Enable()
    
    # Poll data Class 1 (event data)
    master.AddClassScan(
        opendnp3.ClassField(opendnp3.ClassField.CLASS_1),
        openpal.TimeDuration().Seconds(5),
        opendnp3.TaskConfig().Default()
    )

    print("[Master] Running... Press CTRL+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[Master] Shutting down...")
        manager.Shutdown()
        exit()


if __name__ == "__main__":
    main()
