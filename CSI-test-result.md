# AMB82-mini Wi-Fi / CSI test result

- Board: AMB82-mini, COM5, 115200 baud.
- Arduino platform: AmebaPro2 4.0.9-build20250805.
- WLAN driver build: 2025.05.27.18.12_b9.6.
- Wi-Fi association and DHCP succeeded; board IP: 192.168.0.42.
- LAN ping: 4 replies out of 4. Internet access was not tested.
- CSI setup returned -1. CSI was not enabled and no CSI reports were collected.

Inspection of the installed libwlan.a shows both rltk_wlan_csi_config and
rltk_wlan_csi_report consist only of these instructions:

```asm
mov.w r0, #4294967295
bx lr
```

Both functions unconditionally return -1. They are stubs in this library,
despite their public declarations and exported symbols. Changing application
parameters cannot enable CSI with this binary.

This establishes lack of usable CSI support in this installed driver build;
it does not establish that the silicon or every other SDK build lacks support.
A driver with an actual RTL8735B CSI implementation is needed before further
capture testing. Boot evidence is saved locally in wifi-csi-boot.log.

## Public SDK / driver check

Checked Realtek's public AmebaPro2 Arduino package index on 2026-09-11.
The installed package was 4.0.9-build20250805. The latest stable package in
the public index was 4.1.0-build20260213, and the latest early/dev package was
4.1.1-build20260831.

Downloaded and verified the early/dev package:

- File: downloads/ameba_pro2-4.1.1-build20260831/ameba_pro2-4.1.1-build20260831.tar.gz
- SHA-256: 81A07D46F91BD1DACCCB8DF6FF002AF1E1AC2CD1B3D54E717C9260DFD2ECF738
- Library inspected: extract/hardware/variants/common_libs/libwlan.a

The CSI functions in 4.1.1-build20260831 are still stubs:

```asm
00000000 <rltk_wlan_csi_config>:
   0: f04f 30ff  mov.w r0, #4294967295
   4: 4770       bx lr

00000000 <rltk_wlan_csi_report>:
   0: f04f 30ff  mov.w r0, #4294967295
   4: 4770       bx lr
```

Conclusion: neither the installed 4.0.9 package nor the newest public early
4.1.1 package contains a usable RTL8735B Wi-Fi CSI implementation in libwlan.a.
The public CSI documentation currently lists RTL8721Dx, RTL8720E, RTL8726E, and
RTL8730E parameter tabs, but not RTL8735B/AmebaPro2.

## Realtek confirmation request

Suggested question for Realtek forum/support:

> We are testing Wi-Fi CSI capture on AMB82-mini / RTL8735B / AmebaPro2.
> With Arduino AmebaPro2 4.0.9-build20250805, Wi-Fi association and DHCP work,
> but wifi_csi_config() returns -1. Disassembly of libwlan.a shows
> rltk_wlan_csi_config() and rltk_wlan_csi_report() are stubs that
> unconditionally return -1. We also checked the public early package
> 4.1.1-build20260831 and found the same stub implementations.
>
> Does RTL8735B/AMB82-mini support Wi-Fi CSI in any public or FAE-provided SDK?
> If yes, which exact SDK/package version contains the implemented
> rltk_wlan_csi_config/report driver, and is there a sample for passive Rx
> normal mode CSI capture?
