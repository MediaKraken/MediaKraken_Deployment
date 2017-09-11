# drive to use
DRIVE_ID=/dev/sdb
DRIVE_BOOT=$DRIVE_ID + '1'
DRIVE_SYS=$DRIVE_ID + '2'
CODEVERSION=7.0.3

# setup the partitions on DRIVE_ID
# THIS WILL WIPE OUT DRIVE_ID!!!!!!!!!!
sudo parted -s $DRIVE_ID mklabel msdos
sudo parted -s $DRIVE_ID unit cyl mkpart primary fat32 -- 0 16
sudo parted -s $DRIVE_ID set 1 boot on
sudo parted -s $DRIVE_ID unit cyl mkpart primary ext2 -- 16 -2
sudo parted -s $DRIVE_ID print all
sudo mkfs.vfat -n System $DRIVE_BOOT
sudo mkfs.ext4 -L Storage $DRIVE_SYS
sudo partprobe

# copy bootloader files
sudo cp LibreELEC.tv-$CODEVERSION/build.MediaKrakenCL-RPi.arm-devel/bcm2835-bootloader-*/arm128_start.elf /media/System/start.elf
sudo cp LibreELEC.tv-$CODEVERSION/build.MediaKrakenCL-RPi.arm-devel/bcm2835-bootloader-*/bootcode.bin /media/System/
sudo cp LibreELEC.tv-$CODEVERSION/build.MediaKrakenCL-RPi.arm-devel/bcm2835-bootloader-*/loader.bin /media/System/

# copy system files
sudo cp LibreELEC.tv-$CODEVERSION/target/MediaKrakenCL-RPi.arm-6.0-devel-20150929144729-r21337-geb0ed51.system /media/System/SYSTEM
sudo cp LibreELEC.tv-$CODEVERSION/target/MediaKrakenCL-RPi.arm-6.0-devel-20150929144729-r21337-geb0ed51.kernel /media/System/kernel.img

# set boot options
echo "boot=/dev/mmcblk0p1 disk=/dev/mmcblk0p2 ssh quiet" | sudo tee /media/System/cmdline.txt

# unmount sd card images
sudo umount $DRIVE_BOOT
sudo umount $DRIVE_SYS
