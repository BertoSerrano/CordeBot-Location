import decawave_ble
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
    short_name = None
    try:
        short_name = scan_entry.getValueText(8)
    except:
        pass
    for (adtype, desc, value) in scan_entry.getScanData():
        if short_name is not None or adtype == 33 or desc == "128b Service Data" or "e72913c2a1" in value:
            return True
        continue
    return _original(scan_entry)

decawave_ble.is_decawave_scan_entry = is_decawave_scan_entry

# def scan_for_decawave_devices():
#     decawave_scan_entries = decawave_ble.get_decawave_scan_entries()
#     decawave_devices = {}
#     for decawave_scan_entry in decawave_scan_entries:
#         # print("let's try to show the SHORT LOCAL NAME: ")
#         # print("  ", decawave_scan_entry.getValueText(8))
#         # print(decawave_scan_entry)
#         # print(type(decawave_scan_entry))
#         decawave_device = decawave_ble.DecawaveDevice(decawave_scan_entry)
#         # print(decawave_device)
#         # print(type(decawave_device))
#         decawave_devices[decawave_device.device_name] = decawave_device
#     return decawave_devices


devices = decawave_ble.scan_for_decawave_devices() # scan_for_decawave_devices()

anchor_devices = {}
tag_devices = {}
print("Configuration of the devices:")
for k, dev in devices.items():
    print(" ")
    # print("key: ", k, " --  device: ", dev, "    -- (", type(dev), ")")
    if dev is not None:
        print(dev)
        print("TYPE: ", type(dev))
        print(vars(dev))

        print("Utils: \n addr: {}\n addrType: {}, adrr.iface: {}".format(dev.mac_address, dev.address_type, dev.interface))
        try:
            data = decawave_ble.get_data(dev)

            # print(dumps(data["location_data"], indent=4))
            if data["operation_mode_data"]["device_type"] == 0:
                tag_devices[k] = dev
            elif data["operation_mode_data"]["device_type"] == 1:
                anchor_devices[k] = dev
        except:
            print("\n\tget data for device ", dev.device_name, " not working\n")



print("\n\n\t ANCHOR DEVICES:")
for dev in anchor_devices:
    try:
        print(dev.device_name)
        print(dumps(vars(dev), indent=4))
# print(dumps(decawave_ble.get_data_multiple_devices(anchor_devices), indent=4))
    except:
        print("\n\tproblem trying to print anchor and tag devices\n")

print("\n\n\t  TAG   DEVICES:")
for dev in tag_devices:
    try:
        print(dev.device_name)
        print(dumps(vars(dev), indent=4))
# print(dumps(decawave_ble.get_data_multiple_devices(anchor_devices), indent=4))
    except:
        print("\n\tproblem trying to print anchor and tag devices\n")

print("\n\n\nLet's show a few values of our tag devices...\n\n")

#
for x in range(10):
    print(" ")
    for k, dev in tag_devices.items():
        try:
            data = decawave_ble.get_data(dev)
            if data is not None:
                print("Device: ", k)
                print(dumps(data["location_data"]["position_data"], indent=4))
        except:
            pass
# print("\n\n\n")
# print(dumps(decawave_ble.get_data_multiple_devices(devices), indent=4))
