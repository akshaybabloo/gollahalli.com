---
title: "STM32 and Bluetooth LE: Sending Your First Message - Part 1"
date: 2025-03-02T19:41:44+13:00
draft: false
categories: ["STM32"]
tags: ["STM32", "Bluetooth", "BLE", "NUCLEO-WB55RG"]
description: "In this blog post, we will explore on how to use Bluetooth Low Energy (BLE) on the STM32's NUCLEO-WB55RG development board to send a message from a smartphone to the board. In this first part, we will setup the IDE and update the board firmware to support BLE."
images: ["stm32-bluetooth.webp"]
ads: true
video: false
# htmlScripts: []
author:
  prefix: "Mr."
  firstName: "Akshay Raj"
  lastName: "Gollahalli"
  honorarySuffix: "MCIS (FCH)"
  jobTitle: "Research Assistant"
  email: "akshay@gollahalli.com"
  addressCity: "Auckland"
  addressCountry: "New Zealand"
sitemap:
  priority: 0.8
  changeFreq: monthly
siteMapImages:
  - imageLoc: "stm32-bluetooth.webp"
    imageCaption: "STM32 and Bluetooth LE: Sending Your First Message"
# siteMapVideos:
#   - videoLoc: ""
#     videoDescription: ""
---

<!--adsense-->

Hello! And welcome back to another blog post! This is going to be a long one.

Here we will explore on how to use Bluetooth Low Energy (BLE) on the STM32's [NUCLEO-WB55RG](https://www.st.com/en/evaluation-tools/nucleo-wb55rg.html) development board to send a message from a smartphone to the board. Let's divided this into three parts:

1. In the first part, we will setup the IDE and update the board firmware to support BLE.
2. In the second part, we will setup the BLE service and characteristics. 
3. And finally, we will send a message from a smartphone to the board.

Let's start simple. Make sure you have the following:

1. [STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html) installed. Install this first so that it also installs the necessary drivers.
2. [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html) installed.
3. [STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html) - optional, if you use a different IDE.
4. [NUCLEO-WB55RG](https://www.st.com/en/evaluation-tools/nucleo-wb55rg.html) development board.
5. {{< github-source src="https://github.com/STMicroelectronics/STM32CubeWB/tree/master/Projects/STM32WB_Copro_Wireless_Binaries/STM32WB5x" label="STM32WB5x" >}} or [STM32CubeWB](https://www.st.com/en/embedded-software/stm32cubewb.html).
6. A smartphone with BLE capabilities.
7. A USB cable to connect the board to your computer. It still uses micro-USB.
8. I am using Windows 11, but you can use any OS.

## Step 1: Update ST-Link Firmware

Your NUCLEO-WB55RG board comes with an ST-Link debugger. It may be using an older firmware, so it is recommended to update it.

Connect the board to your computer using the micro-USB cable. Open STM32CubeIDE and go to `Help > ST-LINK Upgrade`:

{{< figure src="st-link-upgrade.png" caption="Upgrade ST-Link Firmware" width="600" >}}

This should open the ST-Link Upgrade window. Make sure you are able to see your device in the list, and click on `Open in update mode`:

{{< figure src="st-link-upgrade-2.png" caption="ST-Link Upgrade Window. My board is upto date so my upgrade button is grayed out." width="600" >}}

Now you should see the `Upgrade` button enabled. In the 1st Green box, the top version is your current STLink firmware version and the bottom version is the latest version available. Click on `Upgrade` to update the firmware (Mine is already up to date, but clicking on upgrade will start the process again):

{{< figure src="st-link-upgrade-3.png" caption="Click on upgrade to update the firmware." width="600" >}}

Now, you should see the upgrade in progress:

{{< figure src="st-link-upgrade-4.png" caption="Upgrade in progress." width="600" >}}

After the upgrade is completed, you should see the following screen with the latest firmware version:

{{< figure src="st-link-upgrade-5.png" caption="Upgrade completed." width="600" >}}

## Step 2: Updating BLE Firmware

The NUCLEO-WB55RG board comes with a BLE firmware, but it may be outdated. Let's update it to the latest version.

Open STM32CubeProgrammer and connect your board. You should see the device in the list. Click on `Connect` to connect to the board.

{{< figure src="before-connect-prog.png" caption="Connecting STM32 CubeProgrammer to your board" width="300" >}}

Click on the WiFi looking icon - {{< inline-image src="fus-icon.png" alt="FUS Icon" >}} **Firmware Upgrade Services** - on the bottom left (this will only be visible if the microcontroller is connected).

{{< figure src="after-connect-prog.png" caption="After connecting to the board" width="800" >}}

There are three things to note in the below image; you can download the firmware from {{< github-source src="https://github.com/STMicroelectronics/STM32CubeWB/tree/master/Projects/STM32WB_Copro_Wireless_Binaries/STM32WB5x" label="STM32WB5x" >}} or [STM32CubeWB](https://www.st.com/en/embedded-software/stm32cubewb.html) or click on the GitHub icon. Whenever you flash the firmware make sure you click on `Start FUS` button. And finally, you can read the current FUS information of the board by clicking on the `Read FUS infos` button. 

{{< figure src="fus-page-init.png" caption="FUS - 1 GitHub link to download the firmware. 2 Starting an FUS service. 3 Reading the current FUS information of the board." width="800" >}}

Let's look at our current FUS information:

1. Click on the `Start FUS` button - You should get a message saying `StartFus activated successfully`.
2. And then click on the `Read FUS infos` button - you should see:

{{< figure src="read-fus.png" caption="My current FUS information." width="400" >}}

### Step 2.1: Updateing FUS Firmware

In this step, we will update the FUS and BLE stack firmware. You should by now have downloaded the firmware from the STM32CubeWB or STM32WB5x GitHub page. In this go to `<downloaded-path>/STM32CubeWB/Projects/STM32WB_Copro_Wireless_Binaries/STM32WB5x`, in this, you will need three files:

1. `stm32wb5x_FUS_fw.bin` - This is the FUS firmware.
2. `stm32wb5x_BLE_Stack_full_fw.bin` - This is the BLE stack firmware with all the features.
3. `Release_Notes.html` - This contains the start address for the firmwares.

{{<alert>}}
Always refer to the `Release_Notes.html` file for the start address of the firmware. This is important as the firmware will be flashed to the microcontroller at a specific address.
{{</alert>}}

Let's first update the FUS firmware.

{{<alert>}}
First flash the FUS firmware and then the BLE stack firmware. This is important as the BLE stack firmware requires the FUS firmware to be updated first.
{{</alert>}}

Before updating the firmware, let's look at the required addresses, open the `Release_Notes.html` file and look for the start address of the FUS firmware:

{{< figure src="release-notes.png" caption="Release Notes - Start address for the firmware." width="600" >}}

1. Start the FUS service by clicking on the `Start FUS` button.
2. Click on `Browse` and select the `stm32wb5x_FUS_fw.bin` from the path mentioned above.
3. Finally, Click on `Firmware Upgrade` to update the firmware.

{{< figure src="fus-update.png" caption="Updating FUS firmware" width="600" >}}

Finally, let's update the BLE stack firmware.

{{<alert>}}
Make sure you have choosen the right address for the BLE stack firmware. This is important as the firmware will be flashed to the microcontroller at a specific address.
{{</alert>}}

1. Start the FUS service by clicking on the `Start FUS` button.
2. Click on `Browse` and select the `stm32wb5x_BLE_Stack_full_fw.bin` from the path mentioned above.
3. Finally, Click on `Firmware Upgrade` to update the firmware.

{{< figure src="ble-stack-update.png" caption="Updating BLE stack" width="600" >}}

## Conclusion


