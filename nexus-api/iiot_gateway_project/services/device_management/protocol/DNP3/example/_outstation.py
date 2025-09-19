import sys
import time
from pydnp3 import opendnp3, openpal, asiodnp3, asiopal


# Konfigurasi dasar
LOCAL_IP = "0.0.0.0"
PORT = 20000
CHANNEL_ID = "server"
OUTSTATION_ID = "outstation"
LOG_LEVEL = opendnp3.levels.NORMAL


class SimpleCommandHandler(opendnp3.ICommandHandler):
    """Handler untuk perintah Select/Operate dari master."""
    def __init__(self):
        super(SimpleCommandHandler, self).__init__()

    def Select(self, command, index):
        print(f"[Perintah] Select pada index {index}: {command}")
        return opendnp3.CommandStatus.SUCCESS

    def Operate(self, command, index, op_type):
        print(f"[Perintah] Operate pada index {index}: {command}, Tipe Operasi: {op_type}")
        return opendnp3.CommandStatus.SUCCESS

    def Start(self):
        pass

    def End(self):
        pass


class SimpleOutstationApplication(opendnp3.IOutstationApplication):
    """Implementasi IOutstationApplication untuk fitur tambahan."""
    def __init__(self):
        super(SimpleOutstationApplication, self).__init__()

    def GetApplicationIIN(self):
        return opendnp3.ApplicationIIN()

    def SupportsWriteAbsoluteTime(self):
        return False

    def SupportsWriteTimeAndInterval(self):
        return False

    def SupportsAssignClass(self):
        return False

    def ColdRestartSupport(self):
        return opendnp3.RestartMode.UNSUPPORTED

    def WarmRestartSupport(self):
        return opendnp3.RestartMode.UNSUPPORTED


class SimpleOutstation:
    def __init__(self):
        # Buat manager
        self.manager = asiodnp3.DNP3Manager(1)

        # Buat channel TCP server
        retry = asiopal.ChannelRetry().Default()
        self.channel = self.manager.AddTCPServer(
            id=CHANNEL_ID,
            levels=LOG_LEVEL,
            retry=retry,
            endpoint=LOCAL_IP,
            port=PORT,
            listener=asiodnp3.PrintingChannelListener().Create()
        )

        # Konfigurasi database
        config = asiodnp3.OutstationStackConfig(opendnp3.DatabaseSizes.AllTypes(10))
        self._configure_database(config.dbConfig)

        # Buat instance dari handler dan application
        self.command_handler = SimpleCommandHandler()
        self.application = SimpleOutstationApplication()  # Ini yang benar!

        # Tambahkan outstation — PENTING: gunakan instance application, bukan self
        self.outstation = self.channel.AddOutstation(
            id=OUTSTATION_ID,
            commandHandler=self.command_handler,
            application=self.application,
            config=config
        )

        # Aktifkan
        self.outstation.Enable()
        print(f"✅ Outstation aktif di {LOCAL_IP}:{PORT}")

    def _configure_database(self, db_config):
        """Konfigurasi titik data: 2 binary, 2 analog."""
        # Binary Input
        for i in [1, 2]:
            db_config.binary[i].clazz = opendnp3.PointClass.Class2
            db_config.binary[i].svariation = opendnp3.StaticBinaryVariation.Group1Var2
            db_config.binary[i].evariation = opendnp3.EventBinaryVariation.Group2Var2

        # Analog Input
        for i in [1, 2]:
            db_config.analog[i].clazz = opendnp3.PointClass.Class2
            db_config.analog[i].svariation = opendnp3.StaticAnalogVariation.Group30Var1
            db_config.analog[i].evariation = opendnp3.EventAnalogVariation.Group32Var7

    def update_binary(self, index, value):
        """Update nilai binary input."""
        builder = asiodnp3.UpdateBuilder()
        builder.Update(opendnp3.Binary(value), index)
        self.outstation.Apply(builder.Build())

    def update_analog(self, index, value):
        """Update nilai analog input."""
        builder = asiodnp3.UpdateBuilder()
        builder.Update(opendnp3.Analog(value), index)
        self.outstation.Apply(builder.Build())

    def shutdown(self):
        """Matikan outstation."""
        print("\n🛑 Mematikan outstation...")
        self.manager.Shutdown()


# ================
# Contoh Penggunaan
# ================
if __name__ == "__main__":
    outstation = SimpleOutstation()

    try:
        # Kirim beberapa update contoh
        print("⏳ Mengirim update ke master dalam 3 detik...")
        time.sleep(3)

        outstation.update_binary(1, True)
        outstation.update_analog(1, 100.5)
        time.sleep(2)

        outstation.update_binary(1, False)
        outstation.update_analog(1, 200.0)
        time.sleep(2)

        # Biarkan tetap hidup
        print("📡 Outstation berjalan. Tekan Ctrl+C untuk keluar.")
        while True:
            
            time.sleep(1)

    except KeyboardInterrupt:
        outstation.shutdown()