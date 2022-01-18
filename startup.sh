#!/bin/bash

# Get the emulab repo 
while ! wget -qO - http://repos.emulab.net/emulab.key | sudo apt-key add -
do
    echo Failed to get emulab key, retrying
done

while ! sudo add-apt-repository -y http://repos.emulab.net/powder/ubuntu/
do
    echo Failed to get johnsond ppa, retrying
done

while ! sudo apt-get update
do
    echo Failed to update, retrying
done


#add the default repo from the Ettus's offical guide if this doesn't work

while ! sudo apt-get install libuhd-dev libuhd4.0.0 uhd-host python3-uhd
do
    echo Failed to get uhd packages, retrying
done

do_channel_setup=0

for thing in $*
do
    cmd=(`echo $thing | tr '-' '\n'`)
    case ${cmd[0]} in
        gnuradio)
            while ! sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gnuradio
            do
                echo Failed to get gnuradio, retrying
            done
            ;;

        gnuradio-companion)
            while ! sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gnuradio libgtk-3-dev gir1.2-gtk-3.0 python3-gi gobject-introspection python3-gi-cairo
            do
                echo Failed to get gnuradio, retrying
            done
            ;;
    esac
done

while ! sudo "/usr/lib/uhd/utils/uhd_images_downloader.py"
do
    echo Failed to download uhd images, retrying
done
