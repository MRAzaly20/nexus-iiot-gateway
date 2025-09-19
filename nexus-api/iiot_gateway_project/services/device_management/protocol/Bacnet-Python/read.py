import asyncio
from bacpypes.app import BIPSimpleApplication
from bacpypes.local.device import LocalDeviceObject
from bacpypes.pdu import Address
from bacpypes.apdu import WhoIsRequest, ReadPropertyRequest
from bacpypes.basetypes import PropertyIdentifier
from bacpypes.iocb import IOCB
from bacpypes.core import run, stop

# Konfigurasi device lokal (client)
this_device = LocalDeviceObject(
    objectName="BACnetReaderClient",
    objectIdentifier=("device", 999),
    maxApduLengthAccepted=1024,
    segmentationSupported="segmentedBoth",
    vendorIdentifier=15,
)

# Inisialisasi aplikasi BACnet
app = BIPSimpleApplication(this_device, "192.168.56.1")


async def find_bacnet_devices():
    """Mengirimkan permintaan WhoIs untuk menemukan semua perangkat BACnet di jaringan."""
    print("Mencari perangkat BACnet di jaringan...")
    request = WhoIsRequest()
    app.request(request)


async def read_present_value(target_ip, object_type, object_instance):
    print(f"Membaca {object_type}({object_instance}) dari {target_ip}...")

    request = ReadPropertyRequest(
        objectIdentifier=(object_type, object_instance),
        propertyIdentifier=PropertyIdentifier("presentValue")
    )

    # Pastikan target_ip dalam format tuple (ip, port) atau hanya ip
    if isinstance(target_ip, str) and ":" in target_ip:
        ip, port = target_ip.split(":")
        addr = Address((ip, int(port)))
    else:
        addr = Address(target_ip)

    request.pduDestination = addr

    iocb = IOCB(request)
    app.request_io(iocb)

    if iocb.wait(5.0):  # Tunggu maksimal 5 detik
        if iocb.ioResponse:
            apdu = iocb.ioResponse
            value = apdu.propertyValue.cast_out("Real")
            print(f"Nilai dari {object_type}({object_instance}): {value}")
        elif iocb.ioError:
            print("IO Error:", iocb.ioError)
        else:
            print("Tidak ada respons.")
    else:
        print("Timeout: Tidak ada respons dari perangkat.")

async def main():
    # Langkah 1: Cari perangkat BACnet di jaringan
    await find_bacnet_devices()
    await asyncio.sleep(2)  # Beri waktu untuk menerima I-Am

    # Langkah 2: Baca nilai dari perangkat simulasi
    target_ip = "192.168.56.1"  # Sesuaikan dengan alamat IP server BACnet
    object_type = "analogValue"
    object_instance = 600   # ID instance dari temperature_sensor di bacnet_async.py

    await read_present_value(target_ip, object_type, object_instance)

    # Stop aplikasi setelah selesai
    stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program dihentikan oleh pengguna.")