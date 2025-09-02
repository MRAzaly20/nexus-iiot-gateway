# simple_master.py
import time
from pydnp3 import opendnp3, asiodnp3, asiopal, openpal


class SimpleSOEHandler(opendnp3.ISOEHandler):
    def __init__(self):
        super(SimpleSOEHandler, self).__init__()

    def Process(self, info, values):
        def log_value(v):
            print(f"[SOE] Jenis={info.gv}, Index={v.index}, Nilai={v.value}, Kualitas={v.quality}")
        values.Foreach(log_value)


class SimpleMasterApp(opendnp3.IMasterApplication):
    def OnOpen(self):
        print("[Master] Channel terbuka")

    def OnClose(self):
        print("[Master] Channel tertutup")

    def OnTaskComplete(self, info):
        print(f"[Master] Tugas selesai: {info.result}")


def on_command_complete(result):
    """Callback untuk DirectOperate — perhatikan: gunakan .summary, bukan .result"""
    print(f"[Master] Perintah selesai. Hasil: {result.summary}")


def main():
    HOST = "127.0.0.1"
    PORT = 20000

    # Buat DNP3Manager
    manager = asiodnp3.DNP3Manager(1)

    # Buat TCP Client
    channel = manager.AddTCPClient(
        "master-channel",
        opendnp3.levels.NORMAL,
        asiopal.ChannelRetry.Default(),
        HOST,
        "127.0.0.1",
        PORT,
        asiodnp3.PrintingChannelListener().Create()
    )

    # Konfigurasi stack
    config = asiodnp3.MasterStackConfig()
    config.master.responseTimeout = openpal.TimeDuration().Seconds(3)
    config.link.RemoteAddr = 10  # Alamat outstation
    config.link.LocalAddr = 1    # Alamat master

    # Tambahkan master
    master = channel.AddMaster(
        "master",
        SimpleSOEHandler(),
        SimpleMasterApp(),
        config
    )

    master.Enable()

    # Poll Class 1 (event)
    master.AddClassScan(
        opendnp3.ClassField(opendnp3.ClassField.CLASS_1),
        openpal.TimeDuration().Seconds(5),
        opendnp3.TaskConfig().Default()
    )

    print("✅ Master aktif. Menunggu koneksi...")
    time.sleep(2)

    # === KIRIM PERINTAH CROB ===
    try:
        for i in range(2):
            print(f"\n📤 Mengirim LATCH_ON ke index 0...")
            crob_on = opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON)
            indexed_on = opendnp3.WithIndex(crob_on, 0)
            command_set_on = opendnp3.CommandSet([indexed_on])

            master.DirectOperate(
                command_set_on,
                on_command_complete,
                opendnp3.TaskConfig().Default()
            )

            time.sleep(2)

            print(f"📤 Mengirim LATCH_OFF ke index 0...")
            crob_off = opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_OFF)
            indexed_off = opendnp3.WithIndex(crob_off, 0)
            command_set_off = opendnp3.CommandSet([indexed_off])

            master.DirectOperate(
                command_set_off,
                on_command_complete,
                opendnp3.TaskConfig().Default()
            )

            time.sleep(2)

        print("\n📡 Master tetap hidup. Tekan Ctrl+C untuk keluar.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Master dimatikan.")
        manager.Shutdown()
        exit()


if __name__ == "__main__":
    main()