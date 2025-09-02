# simple_outstation.py
import time
from pydnp3 import opendnp3, asiodnp3, asiopal


class SimpleCommandHandler(opendnp3.ICommandHandler):
    def __init__(self):
        super(SimpleCommandHandler, self).__init__()

    def Select(self, command, index):
        print(f"[Outstation] Select perintah di index {index}: {command}")
        return opendnp3.CommandStatus.SUCCESS

    def Operate(self, command, index, op_type):
        print(f"[Outstation] Operate perintah di index {index}: {command}, Tipe: {op_type}")
        return opendnp3.CommandStatus.SUCCESS

    def Start(self):
        pass

    def End(self):
        pass


class SimpleOutstationApplication(opendnp3.IOutstationApplication):
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
        self.manager = asiodnp3.DNP3Manager(1)
        self.command_handler = SimpleCommandHandler()
        self.application = SimpleOutstationApplication()

        # Buat channel TCP server
        retry = asiopal.ChannelRetry().Default()
        self.channel = self.manager.AddTCPServer(
            id="outstation-channel",
            levels=opendnp3.levels.NORMAL,
            retry=retry,
            endpoint="127.0.0.1",
            port=20000,
            listener=asiodnp3.PrintingChannelListener().Create()
        )

        # Konfigurasi stack
        config = asiodnp3.OutstationStackConfig(opendnp3.DatabaseSizes.AllTypes(10))
        config.link.LocalAddr = 10
        config.link.RemoteAddr = 1
        self._configure_database(config.dbConfig)

        # Tambahkan outstation
        self.outstation = self.channel.AddOutstation(
            id="outstation",
            commandHandler=self.command_handler,
            application=self.application,
            config=config
        )

        self.outstation.Enable()
        print("✅ Outstation aktif di port 20000")

    def _configure_database(self, db_config):
        # Binary Input (Group 1 Var 2)
        for i in [0, 1]:
            db_config.binary[i].clazz = opendnp3.PointClass.Class2
            db_config.binary[i].svariation = opendnp3.StaticBinaryVariation.Group1Var2
            db_config.binary[i].evariation = opendnp3.EventBinaryVariation.Group2Var2

        # Analog Input (Group 30 Var 1)
        for i in [0, 1]:
            db_config.analog[i].clazz = opendnp3.PointClass.Class2
            db_config.analog[i].svariation = opendnp3.StaticAnalogVariation.Group30Var1
            db_config.analog[i].evariation = opendnp3.EventAnalogVariation.Group32Var7

        # CROB (Control Relay Output Block) - Group 12 Var 1
        for i in [0]:
            db_config.binary[i].clazz = opendnp3.PointClass.Class1  # Untuk respon cepat

    def update_binary(self, index, value):
        builder = asiodnp3.UpdateBuilder()
        builder.Update(opendnp3.Binary(value), index)
        self.outstation.Apply(builder.Build())

    def update_analog(self, index, value):
        builder = asiodnp3.UpdateBuilder()
        builder.Update(opendnp3.Analog(value), index)
        self.outstation.Apply(builder.Build())

    def shutdown(self):
        print("\n🛑 Mematikan outstation...")
        self.manager.Shutdown()


# Jalankan outstation
if __name__ == "__main__":
    outstation = SimpleOutstation()

    try:
        # Simulasi update data
        print("📈 Mengirim update data tiap 5 detik...")
        for i in range(10):
            temp = 20 + (i % 10)
            motion = i % 2 == 0
            outstation.update_analog(0, temp)
            outstation.update_binary(0, motion)
            print(f"📊 Update: Suhu={temp}°C, Gerak={motion}")
            time.sleep(5)
    except KeyboardInterrupt:
        outstation.shutdown()