# Tetris

### Reboot PI

```bash
sudo reboot
```

### Stop game

```bash
ps -ax | grep python
sudo kill -9 791
```

### Start game

```bash
sudo python main.py
```

### Commit GIT

```bash
git status 
git add --all
git commit -m "messqge"
git push origin master
```

### Pull GIT (update)

```bash
git pull origin master
```

### Modify boot sequence (splash + game)

```bash
sudo nano /etc/rc.local
```

```bash
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

/usr/bin/fbi -noverbose -d /dev/fb0 -T 1 -a /home/admin/tetris/images/Tetris_splash.png
cd /home/admin/tetris && /usr/bin/python main.py >> /home/admin/tetris/log.txt 2>&1

exit 0
```

### Boot Config (/boot/firmware/config.txt)

```bash
# For more options and information see
# http://rptl.io/configtxt
# Some settings may impact device functionality. See link above for details

# Uncomment some or all of these to enable the optional hardware interfaces
dtparam=i2c_arm=on # <---
dtparam=i2s=on # <---
dtparam=spi=on # <---

# Enable audio (loads snd_bcm2835)
dtparam=audio=on

# Additional overlays and parameters are documented
# /boot/firmware/overlays/README

# Automatically load overlays for detected cameras
camera_auto_detect=1

# Automatically load overlays for detected DSI displays
display_auto_detect=1

# Automatically load initramfs files, if found
auto_initramfs=1

# Enable DRM VC4 V3D driver
dtoverlay=vc4-kms-v3d
max_framebuffers=2 # <---

# Don't have the firmware create an initial video= setting in cmdline.txt.
# Use the kernel's default instead.
disable_fw_kms_setup=1

# Run in 64-bit mode
arm_64bit=1

# Disable compensation for displays with overscan
disable_overscan=1

# Run as fast as firmware / board allows
arm_boost=1

disable_splash=1 # <---

[cm4]
# Enable host mode on the 2711 built-in XHCI USB controller.
# This line should be removed if the legacy DWC2 controller is required
# (e.g. for USB device mode) or if USB support is not required.
otg_mode=1

[all]
display_hdmi_rotate=1 # <---
```

### Command Line (/boot/firmware/cmdline.txt)

```
console=serial0,115200 console=tty2 root=PARTUUID=5d44a020-02 rootfstype=ext4 fsck.repair=yes rootwait cfg80211.ieee80211_regdom=GB fbcon=rotate_all:1 video=HDMI-A-1:480x480M@60,rotate=90 video=HDMI-A-2:480x480M,rotate=90 splash quiet logo.nologo vt.global_cursor_default=0
```