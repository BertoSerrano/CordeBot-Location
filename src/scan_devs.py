import decawave_ble
from bluepy.btle import Peripheral
from json import dumps

# scanner = Scanner()
# devices = scanner.scan(10.0)
#
# print(type(devices))
# for dev in devices:
#     print(type(dev))
#     print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
#     print(dev.getScanData())
#     for (adtype, desc, value) in dev.getScanData():
#         print("  %s = %s" % (desc, value))

_original = decawave_ble.is_decawave_scan_entry


def is_decawave_scan_entry(scan_entry):
    # print("Inside IS DECAWAVE SCAN ENTRY:")
    # print(scan_entry)
    # print(type(scan_entry))
    scan_data = scan_entry.getScanData()
    # print("This is scan Data:")
    # print(scan_data)
    # print(type(scan_data))
    try:
        short_name = scan_entry.getValueText(8)
        # short_name = scan_entry.getValue(8)
        # print("short name:  ", short_name)
    except:
        pass
    # print("continue..")
    for (adtype, desc, value) in scan_entry.getScanData():
        if adtype == 33 or desc == "128b Service Data" or "e72913c2a1" in value:
            return True
        continue
    return _original(scan_entry)


#     short_local_name = scan_entry.getValueText(decawave_ble.SHORT_LOCAL_NAME_TYPE_CODE)
#     return (short_local_name is not None and short_local_name.startswith('DW'))

decawave_ble.is_decawave_scan_entry = is_decawave_scan_entry
print("using API:")


class DecawaveDevice:
    def __init__(self, decawave_scan_entry):
        self.scan_entry = decawave_scan_entry
        self.mac_address = decawave_scan_entry.addr
        self.address_type = decawave_scan_entry.addrType
        self.interface = decawave_scan_entry.iface
        self.rssi = decawave_scan_entry.rssi
        self.connectable = decawave_scan_entry.connectable
        advertising_data_tuples = decawave_scan_entry.getScanData()
        self.advertising_data = []
        self.device_name = None
        for advertising_data_tuple in advertising_data_tuples:
            type_code, description, value = advertising_data_tuple
            self.advertising_data.append({
                'type_code': type_code,
                'description': description,
                'value': value})
            if type_code == decawave_ble.SHORT_LOCAL_NAME_TYPE_CODE:
                self.device_name = value

    def scan_data(self):
        return {
            'device_name': self.device_name,
            'mac_address': self.mac_address,
            'address_type': self.address_type,
            'interface': self.interface,
            'rssi': self.rssi,
            'connectable': self.connectable,
            'advertising_data': self.advertising_data}


def scan_for_decawave_devices():
    decawave_scan_entries = decawave_ble.get_decawave_scan_entries()
    decawave_devices = {}
    for decawave_scan_entry in decawave_scan_entries:
        # print("let's try to show the SHORT LOCAL NAME: ")
        # print("  ", decawave_scan_entry.getValueText(8))
        # print(decawave_scan_entry)
        # print(type(decawave_scan_entry))
        decawave_device = decawave_ble.DecawaveDevice(decawave_scan_entry)
        # print(decawave_device)
        # print(type(decawave_device))
        decawave_devices[decawave_device.device_name] = decawave_device
    return decawave_devices


devices = scan_for_decawave_devices()
# print(len(devices))
# print(type(devices))

anchor_devices = {}
tag_devices = {}

for k, dev in devices.items():
    # print("key: ", k, " --  device: ", dev, "    -- (", type(dev), ")")
    if dev is not None:
        print(dev)
        print("TYPE: ", type(dev))
        print(vars(dev))

        print("Utils: \n addr: {}\n addrType: {}, adrr.iface: {}".format(dev.mac_address, dev.address_type, dev.interface))
        # decawave_ble.get_decawave_peripheral(dev).connect(dev.mac_address, dev.address_type, dev.interface)
        try:
            data = decawave_ble.get_data(dev)
            print(dumps(data["location_data"], indent=4))
            if data["operation_mode_data"]["device_type"] == 0:
                tag_devices[k] = dev
            elif data["operation_mode_data"]["device_type"] == 1:
                anchor_devices[k] = dev
        except:
            print("get data for device ", dev, " not working")

# print(dumps(decawave_ble.get_data_multiple_devices(devices), indent=4))

#
try:
    print("\n\n\t ANCHOR DEVICES:")
    for dev in anchor_devices:
        print(dev)
        print(vars(dev))
    # print(dumps(decawave_ble.get_data_multiple_devices(anchor_devices), indent=4))

    print("\n\n\t  TAG   DEVICES:")
    for dev in tag_devices:
        print(dev)
        print(vars(dev))
    # print(dumps(decawave_ble.get_data_multiple_devices(anchor_devices), indent=4))
except:
    print("problem trying to print anchor and tag devices")


#
try:
    for x in range(10):
        for k, dev in tag_devices.items():
            data = decawave_ble.get_data(dev)
            print("Device: ", k)
            print(dumps(data["location_data"], indent=4))
except:
    pass
# print("\n\n\n")
# print(dumps(decawave_ble.get_data_multiple_devices(devices), indent=4))
