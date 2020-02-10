import os
from json import dumps

import decawave_ble

_original = decawave_ble.is_decawave_scan_entry


def is_decawave_scan_entry(scan_entry):
    short_name = None
    try:
        short_name = scan_entry.getValueText(8)
    except (KeyboardInterrupt, SystemExit, SystemError) as e:
        raise e
    except:
        pass
    for (adtype, desc, value) in scan_entry.getScanData():
        if short_name is not None or adtype == 33 or desc == "128b Service Data" or "e72913c2a1" in value:
            return True
        continue
    return _original(scan_entry)


decawave_ble.is_decawave_scan_entry = is_decawave_scan_entry

devices = decawave_ble.scan_for_decawave_devices()  # scan_for_decawave_devices()

anchor_devices = {}
tag_devices = {}
print("Configuration of the devices:")
for k, dev in devices.items():
    print(" ")
    if dev is not None:
        # print(dev)
        # print("TYPE: ", type(dev))
        # print(vars(dev))

        print("Utils: \n addr: {}\n addrType: {}, adrr.iface: {}".format(dev.mac_address, dev.address_type,
                                                                         dev.interface))
        for x in range(4):
            try:
                data = decawave_ble.get_data(dev)

                print(dumps(data, indent=4))

                if data["operation_mode_data"]["device_type"] == 0\
                        or "robot" in str(k).lower() or "oveja" in str(k).lower():
                    tag_devices[k] = dev
                elif data["operation_mode_data"]["device_type"] == 1:
                    anchor_devices[k] = dev
                break
            except (KeyboardInterrupt, SystemExit, SystemError) as e:
                raise e
            except:
                continue
            finally:
                if x == 3:
                    print("\n\tget data for device ", dev.device_name, " not working\n")




def show_devices(devices):
    global dev, x, e
    for dev in devices:
        for x in range(3):
            try:
                print(dev.device_name)
                print(dumps(vars(dev), indent=4))
                break
            # print(dumps(decawave_ble.get_data_multiple_devices(anchor_devices), indent=4))
            except (KeyboardInterrupt, SystemExit, SystemError) as e:
                raise e
            except:
                continue
            finally:
                if x == 2:
                    print("\n\tproblem trying to print anchor and tag devices\n")

print("\n\n\t ANCHOR DEVICES:")
show_devices(devices=anchor_devices)

print("\n\n\t  TAG   DEVICES:")
show_devices(devices=tag_devices)


print("\n\n\nLet's show a few values of our tag devices...\n\n")

#

import time

start = time.time()

FileRobot = "Robot_results_inside.txt"
FileOveja = "Oveja_results_inside.txt"

file_robot = open(FileRobot, "w")
file_oveja = open(FileOveja, "w")

file = None
while time.time() - start < 2040:
    print(" ")
    for k, dev in tag_devices.items():
        for y in range(3):
            try:
                data = decawave_ble.get_data(dev)
                if data is not None:
                    print("Device: ", k)
                    if "robot" in str(k).lower():
                        file = file_robot
                    elif "oveja" in str(k).lower():
                        file = file_oveja
                    else:
                        print(k)
                        print(str(k).lower())
                        print("there's no key in the device dictionary")
                        continue
                    to_show = str(data["location_data"]["position_data"])
                    if to_show == "None":
                        print("The call to : 'data[...] gets Nothing")
                        continue
                    print(dumps(data["location_data"]["position_data"], indent=4))
                    file.write(dumps(data["location_data"]["position_data"], indent=4))
                    print(type(to_show))
                    break
            except (KeyboardInterrupt, SystemExit, SystemError) as e:
                raise e
            except:
                pass

file_robot.close()
file_oveja.close()

os.chmod("results__inside_lab.txt", 0o777)
# print("\n\n\n")
# print(dumps(decawave_ble.get_data_multiple_devices(devices), indent=4))
