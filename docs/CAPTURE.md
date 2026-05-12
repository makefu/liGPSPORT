# Capturing BLE traffic for ligpsport reverse engineering

Two ways to obtain a Wireshark-readable capture of what the iGPSPORT
app and the BSC200 exchange over Bluetooth:

1. **Android HCI snoop log** — the *useful* one. Records everything
   the phone's Bluetooth controller sees, including the MTU
   negotiation, every ATT Write / Notify / Read, and any bonding /
   security exchanges. This is what you want when you're trying to
   compare a working app upload against ``ligpsport``'s wire output.
2. **Linux ``btmon``** — only captures traffic going through the
   *Linux* host's Bluetooth adapter. Useful when debugging the
   ``ligpsport`` library itself (where the host is the BLE central),
   but it can't see app → BSC200 traffic.

Both produce btsnoop-format files that open natively in Wireshark.

---

## 1. Android HCI snoop log

### Enable

1. Open **Settings → About phone**, tap **Build number** seven times
   to unlock Developer Options.
2. Open **Settings → System → Developer options**.
3. Toggle on **Enable Bluetooth HCI snoop log**.
4. Turn Bluetooth **off and on again** — on some Android builds the
   snoop log only starts on a fresh BT session.

### Reproduce the flow

Now do exactly what you want captured, and nothing else. Start small
to keep the capture file readable:

- Open the iGPSPORT app, connect to the BSC200.
- Trigger the operation you're investigating (e.g. upload one short
  route). Wait for the "uploaded successfully" toast.
- Close the app and turn Bluetooth off — this rotates the log file.

### Pull the log

The log path varies by Android version. Try in order:

```sh
# Android 9 and below
adb pull /sdcard/btsnoop_hci.log .

# Android 10+
adb pull /data/misc/bluetooth/logs/btsnoop_hci.log .

# Android 11+ where the path is locked down: take a bug report, which
# embeds the snoop log inside the resulting zip.
adb bugreport bugreport.zip
unzip -p bugreport.zip 'FS/data/misc/bluetooth/logs/btsnoop_hci.log' > btsnoop_hci.log
```

If none of those work, the OEM may have moved the file — check
`adb shell ls -lR /data/misc/bluetooth/logs/` or
`adb shell getprop persist.bluetooth.btsnoopdefaultmode`.

### Open in Wireshark

```sh
nix run nixpkgs#wireshark -- btsnoop_hci.log
```

Filter to traffic involving the BSC200's MAC address:

```
bthci_acl.dst.bd_addr == f7:11:62:07:1f:f5 ||
bthci_acl.src.bd_addr == f7:11:62:07:1f:f5
```

### What to look for

For the **MTU question** (which is blocking the route upload), find
the first **ATT Exchange MTU Request / Response** packets after the
connection is established. They look like:

```
Sent  Exchange MTU Request, Client Rx MTU: 247
Rcvd  Exchange MTU Response, Server Rx MTU: 247
```

The Server Rx MTU is the largest write the BSC200 will accept in one
ATT operation. Subtract 3 (the ATT header overhead) to get the
maximum chunk size the application layer can use. If the app
negotiates 247 and ``ligpsport`` is stuck at 23, that's our problem
— see :mod:`ligpsport.bluez` for the BlueZ-direct backend that
forces a higher MTU through `AcquireWrite` / `AcquireNotify`.

For the **route upload payload**, filter further to writes on the
control RX characteristic:

```
btatt.handle == 0x???? && _ws.col.info contains "Write"
```

(Substitute the handle you see for the
`6e400002-b5a3-f393-e0a9-e50e24dcca8e` characteristic in the GATT
discovery section of the capture.) Each Write Command / Write
Request's "Value" field is one chunk of the upload blob.
Concatenate them in order and compare to what
``ligpsport.file_transfer.upload_route_plan`` produces.

For the **device's reply** to the upload, look at notifications
(`btatt.opcode == 0x1b`) on the data TX char
`6e400003-b5a3-f393-e0a9-e50e24dcca9e`.

### Sanitising the capture

The snoop log contains every BLE device the phone saw during the
window. Trim to just BSC200 traffic before sharing publicly:

```sh
tshark -r btsnoop_hci.log \
  -Y 'bthci_acl.dst.bd_addr == f7:11:62:07:1f:f5 ||
      bthci_acl.src.bd_addr == f7:11:62:07:1f:f5' \
  -w bsc200_only.pcapng
```

Drop the trimmed file into ``tmp/captures/`` (gitignored) for the
library to consume.

---

## 2. Linux btmon

When the **Linux host running ``ligpsport``** is the BLE central
(e.g. you're debugging the library's own writes against the device),
``btmon`` captures every HCI command and event the local controller
sends or receives:

```sh
# Start the capture before launching ligpsport.
sudo btmon -w ligpsport.btsnoop &
BTMON=$!

# Run whatever ligpsport flow you want to debug.
nix run . -- command --name bike upload-route route.geojson

# Stop btmon.
kill $BTMON
```

Open in Wireshark exactly like the Android log. The filter syntax is
the same — `bthci_acl.dst.bd_addr == ...`.

Differences from the Android log:

- **No data outside the local adapter.** If the app on a phone
  uploads a route to the BSC200, ``btmon`` on a Linux laptop
  next-door sees nothing.
- The HCI layer below ATT is visible too (LL Control packets,
  connection parameter updates, link-layer errors). Useful for
  diagnosing disconnects.

---

## 3. Decoding a capture into PROTOCOL.md vectors

When you find an interesting frame, capture it as a hex string and
add it to ``docs/PROTOCOL.md`` §2.4 (Captured frame catalogue). The
``ligpsport.framing`` codec round-trips the bytes; ``parse_frame``
on the hex turns it into a structured ``Frame`` for the doc.

Quick decode in the dev shell:

```sh
nix develop --command python -c '
from ligpsport.framing import parse_frame
f = parse_frame(bytes.fromhex("0111ffff03ffff00257c01ffffffffffffffffd1...payload..."))
print(f)
'
```
