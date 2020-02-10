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

print(devices)

#
# def show_devices(devices):
#     global dev, x, e
#     for dev in devices:
#         for x in range(3):
#             try:
#                 print(dev.device_name)
#                 print(dumps(vars(dev), indent=4))
#                 break
#             # print(dumps(decawave_ble.get_data_multiple_devices(anchor_devices), indent=4))
#             except (KeyboardInterrupt, SystemExit, SystemError) as e:
#                 raise e
#             except:
#                 continue
#             finally:
#                 if x == 2:
#                     print("\n\tproblem trying to print anchor and tag devices\n")
#
#
# show_devices(devices=devices)
