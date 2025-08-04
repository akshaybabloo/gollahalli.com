---
title: "Serial Communication Between STM32 and Web via USB"
date: 2025-08-05T10:27:22+12:00
draft: false
categories: ["STM32", "Serial Communication"]
tags: ["STM32", "Web", "Serial Communication"]
description: "Learn how to establish serial communication between an STM32 microcontroller and a web application using USB, enabling real-time data exchange for interactive applications."
images: ["serial-communication-between-stm32-and-web-via-usb.png"]
ads: true
video: false
toc: true
# htmlScripts: []
author:
  prefix: "Mr."
  firstName: "Akshay Raj"
  lastName: "Gollahalli"
  honorarySuffix: "MCIS (FCH)"
  jobTitle: "Software Engineer"
  email: "akshay@gollahalli.com"
  addressCity: "Auckland"
  addressCountry: "New Zealand"
sitemap:
  priority: 0.8
  changeFreq: monthly
siteMapImages:
  - imageLoc: "serial-communication-between-stm32-and-web-via-usb.png"
    imageCaption: "Serial Communication Between STM32 and Web via USB"
# siteMapVideos:
#   - videoLoc: ""
#     videoDescription: ""
---

<!--adsense-->

The code can be found on {{< github-source src="https://github.com/akshaybabloo/stm32-virtual-comm-example" label="akshaybabloo/stm32-virtual-comm-example" >}}

In this blog, we will explore how to establish serial communication via USB between an STM32 microcontroller and a web application. This setup allows us to send and receive data in real-time, enabling interactive applications such as sensor monitoring or control systems. Before going into the sensor data transmission, we will first try to toggle an LED on the STM32 NUCLEO-WB55RG board using a web application.

## Prerequisites

I have tested this on Ubuntu because I didn't want to mess with Windows registry. However, it should work on Windows as well, I will put the instructions for Windows at the end of this blog.

- STM32 NUCLEO-WB55RG board
- STM32CubeIDE
- STM32CubeMX
- NodeJS
- C++ compiler with CMake support (e.g., g++)
- Python 3 (For testing the serial communication)
- A web browser (show work on any Chromium-based browser)

## Architecture Overview

{{< figure src="architecture.svg" caption="Screenshot of Flutter UI in Tauri window." width="1200" >}}

The architecture consists of three main components:

1. The web browser with a web application that provides the user interface and a Chrome extension to handle native messaging.
2. The backend written in C++ that communicates with the STM32 board over USB serial.
3. The STM32 board running a firmware that handles serial communication and controls the LED.

I wanted each of these components to do few things:

1. The **web application** should request ports available, get the information about the port, and toggle the light all while communicating with the Chrome extension, lets call it the **Bridge**.
2. The **Bridge** should act like a middleman between the web application and the backend, and nothing more. All it has to do it forward messages from the web application to the backend and vice versa.
3. The **backend** should handle the serial communication with the **STM32 board** and provide an API for the **Bridge** to interact with.

Lets looks at them in detail.

## Web Browser and Chrome Extension

I have used Chrome just because it is probably the de facto browser with good support for extensions. I think any browser that is based off Chromium should work, but I have not tested it.

The web application uses {{< external-link src="https://developer.chrome.com/docs/extensions/reference/api/runtime#method-sendMessage" label="chrome.runtime.sendMessage()" >}} to send message to the extension worker. The worker in the extension then uses {{< external-link src="https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging" label="Native Messaging" >}} to forward the information to the backend.

In {{< github-source src="https://github.com/akshaybabloo/stm32-virtual-comm-example/blob/main/web/src/components/SwitchComponent.vue" label="SwitchComponent.vue" >}}, we use this code below to send a message to the extension:

```ts
async function sendMessageToBackend(payload: { action: string; value?: any }): Promise<BackendResponseMessage> {
  if (!EXTENSION_ID) {
    const errorMsg = "Extension ID is not set. Please update the EXTENSION_ID constant in the script.";
    console.error(errorMsg);
    errorMessage.value = errorMsg;
    return { success: false, action: payload.action, error: errorMsg };
  }

  try {
    const reply = await window.chrome.runtime.sendMessage(EXTENSION_ID, payload);
    console.log(`Reply for '${payload.action}':`, reply);

    if (!reply || !reply.success) {
      throw new Error(reply?.message || reply?.error || 'An unknown error occurred');
    }
    return reply;
  } catch (error) {
    console.error(`Error sending '${payload.action}':`, error);
    errorMessage.value = (error as Error).message;
    return { success: false, action: payload.action, error: (error as Error).message };
  }
}
```

Which essentially sends a message to the extension with the action and value.

### The Extension Worker - Bridge

First make sure you have developer mode enabled in Chrome. You can do this by going to `chrome://extensions/` and toggling the "Developer mode" switch on the top right corner. Take a look at {{< external-link src="https://developer.chrome.com/docs/extensions/get-started/tutorial/hello-world" label="Hello World Tutorial" >}} on how to install local extension in Chrome.

The extension needs few permissions before it can communicate with a native application. These information is specified in the `manifest.json` file of the extension. See {{< github-source src="https://github.com/akshaybabloo/stm32-virtual-comm-example/blob/main/extension/public/manifest.json" label="manifest.json" >}} for more information. It should look something like this:

```json
{
  "manifest_version": 3,
  "name": "Serial Bridge",
  "short_name": "Serial Bridge",
  "description": "A Chrome extension for serial communication",
  "version": "1.0",
  "action": {
    "default_popup": "index.html",
    "default_icon": "bridge-icon.png"
  },
  "permissions": [
    "activeTab",
    "nativeMessaging"
  ],
  "background": {
    "service_worker": "assets/background.js"
  },
  "externally_connectable": {
    "matches": [
      "http://localhost:5173/*",
      "*://localhost/*"
    ]
  }
}
```

The main permission we are interested in is `nativeMessaging`, which allows the extension to communicate with a native application installed on the user's machine.

Using the {{< external-link src="https://developer.chrome.com/docs/extensions/reference/api/runtime#event-onMessageExternal" label="chrome.runtime.onMessageExternal.addListener()" >}} API, we can listen for messages from the web application. This can be seen in {{< github-source src="https://github.com/akshaybabloo/stm32-virtual-comm-example/blob/main/extension/src/background.ts" label="background.ts" >}}, which has:

```ts
chrome.runtime.onMessageExternal.addListener((message, _sender, sendResponse) => {
  // Handle messages from the web application
})
```

Once a `message` is received, we can then use {{< external-link src="https://developer.chrome.com/docs/extensions/reference/api/runtime#method-sendNativeMessage" label="chrome.runtime.sendNativeMessage()" >}} to forward the message to the backend. In the same file, we have:

```ts
chrome.runtime.onMessageExternal.addListener((message, _sender, sendResponse) => {

  // In this case, the message is an object of type {action: string, value: any, port?: string}
  if (message.action === 'toggleLight') {
        // Handle the message, e.g., send it to the serial device
        console.log(`Toggling light: ${message.value}`);

        chrome.runtime.sendNativeMessage(
            'com.gollahalli.serial_example',
            {action: 'toggleLight', value: message.value, port: message.port},
            function (response) {
                console.log('Received ' + JSON.stringify(response));
                // @ts-ignore
                sendResponse(response);
            }
        );
    }

  // Handle other actions similarly

  return true; // Keep the message channel open for sendResponse
})
```

Once a message is received from the native application, we can then use `sendResponse` to send the response back to the web application. Once you install the extension, you can get the extension ID from `chrome://extensions/` page. You will need this ID to communicate with the extension from the web application.

## Native Application - Backend

{{<alert>}}
The native application can be written in any language. I chose C++ because I use it a lot and also because of this library called [ami-iit/serial_cpp](https://github.com/ami-iit/serial_cpp) which makes it easy to communicate with serial devices. You can use any other library that supports serial communication in your preferred language.
{{</alert>}}

The backed is a simple C++ that takes in messages via the `stdin` and sends messages to the STM32 board over USB serial and replies to the extension worker using `stdout`.

For Chrome to able to communicate with a native application, we must create a manifest file that describes where the native application is installed and who can access it. This should be placed in `~/.config/google-chrome/NativeMessagingHosts/com.gollahalli.serial_example.json` (or the equivalent path for your browser). The manifest file should look like this:

```json
{
  "name": "com.gollahalli.serial_example",
  "description": "Serial communication example for STM32",
  "path": "/path/to/your/backend/binary",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://<YOUR_EXTENSION_ID>/"
  ]
}
```

With this information, the extension now knows how to communicate with the backend.

First, lets look at how do the extension and native application communicate. As we have seen earlier, the extension uses `chrome.runtime.sendNativeMessage()` to send a message to the native application. The native application listens for messages on `stdin` and replies on `stdout`. The message format is JSON, so we can use any JSON library to parse the message. From {{< github-source src="https://github.com/akshaybabloo/stm32-virtual-comm-example/blob/main/main.cpp" label="main.cpp" >}}, we first read the length of the message from `stdin`, then read the message:

```cpp
uint32_t readMessageLength() {
    uint32_t length = 0;
    std::cin.read(reinterpret_cast<char *>(&length), 4);
    return length;
}

std::string readMessage(const uint32_t &length) {
    std::string message(length, '\0');
    std::cin.read(&message[0], length);
    return message;
}

int main(int argc, char *argv[]) {
    while (true) {
        const uint32_t length = readMessageLength();
        if (std::cin.eof()) break;

        std::string messageStr = readMessage(length);
        // Parse the message
    }
    return 0;
}
```

The read message is then parsed using a JSON library, in this case, we are using [nlohmann/json](https://github.com/nlohmann/json).

```cpp
#include <nlohmann/json.hpp>

using json = nlohmann::json;

// reading the message helpers...

int main(int argc, char *argv[]) {
    while (true) {
        const uint32_t length = readMessageLength();
        if (std::cin.eof()) break;

        std::string messageStr = readMessage(length);
        json message = json::parse(messageStr);

        // Handle the message
    }
    return 0;
}
```

This message should now be handled to do its task - toggle the LED in our case. In `handleMessage()` function, we check the action and perform the corresponding task:

```cpp
void handleMessage(const json &message, const std::shared_ptr<spdlog::logger>& logger) {
    logger->debug("Received message: {}", message.dump());

    auto serialPort = std::make_unique<SerialPort>(logger);

    if (message.contains("action")) {
        std::string action = message["action"];

        if (action == "toggleLight") {
            bool value = message.value("value", false);
            string port = message.value("port", "");
            logger->info("Light toggle received: {}", value);

            try {
                if (value) {
                    logger->info("Turning on light");
                    // Send command to turn on light
                    serialPort->sendData(port, "011");
                } else {
                    logger->info("Turning off light");
                    // Send command to turn off light
                    serialPort->sendData(port, "001");
                }
            } catch (const std::exception &e) {
                logger->error("Error toggling light: {}", e.what());
                const json response = {
                    {"action", "toggleLight"},
                    {"success", false},
                    {"error", e.what()}
                };
                sendMessage(response);
                return;
            }
        }
    } else {
        logger->error("Unknown action in message: {}", message.dump());
    }
}

int main(int argc, char *argv[]) {
    while (true) {
        const uint32_t length = readMessageLength();
        if (std::cin.eof()) break;

        std::string messageStr = readMessage(length);
        json message = json::parse(messageStr);

        handleMessage(message, logger);
    }
    return 0;
}
```

Similar structure to the extension - `{action: string, value?: any, port?: string}` is used to send the message to the STM32 board. The `port` is the serial port that the STM32 board is connected to, which can be obtained from the web application.

A response can be sent back to the extension using `sendMessage()` function, which writes the response to `stdout`:

```cpp
void sendMessage(const json &message) {
    const std::string msgStr = message.dump();
    const uint32_t length = msgStr.length();

    std::cout.write(reinterpret_cast<const char *>(&length), 4);
    std::cout.write(msgStr.c_str(), length);
    std::cout.flush();
}

void handleMessage(const json &message, const std::shared_ptr<spdlog::logger>& logger) {
    logger->debug("Received message: {}", message.dump());

    auto serialPort = std::make_unique<SerialPort>(logger);

    if (message.contains("action")) {
        std::string action = message["action"];

        if (action == "toggleLight") {
            bool value = message.value("value", false);
            string port = message.value("port", "");
            logger->info("Light toggle received: {}", value);

            try {
                if (value) {
                    logger->info("Turning on light");
                    // Send command to turn on light
                    serialPort->sendData(port, "011"); // Replace "COM1" with actual port
                } else {
                    logger->info("Turning off light");
                    // Send command to turn off light
                    serialPort->sendData(port, "001"); // Replace "COM1" with actual port
                }
            } catch (const std::exception &e) {
                logger->error("Error toggling light: {}", e.what());
                const json response = {
                    {"action", "toggleLight"},
                    {"success", false},
                    {"error", e.what()}
                };
                sendMessage(response);
                return;
            }

            // Send response back to extension
            const json response = {
                {"action", "toggleLight"},
                {"success", true},
                {"message", "Light toggled"},
                {"value", value}
            };
            sendMessage(response);
        } else {
          const json response = {
            {"success", false},
            {"error", "Unknown action"}
          };
          sendMessage(response);
          logger->error("Unknown action in message: {}", message.dump());
        }
    }
}
```

Take a look at the helper functions in {{< github-source src="https://github.com/akshaybabloo/stm32-virtual-comm-example/blob/main/serialport.cpp" label="serialport.cpp" >}} and {{< github-source src="https://github.com/akshaybabloo/stm32-virtual-comm-example/blob/main/portdescription.h" label="portdescription.h" >}} for more information on how to handle serial communication and get the port description.

Combination of message sent to the NUCLEO board is shown in the next section.

## STM32 Firmware - NUCLEO-WB55RG

The STM32 firmware is written in C using STM32CubeIDE and STM32CubeMX. The firmware initializes the USB CDC (Communication Device Class) to handle serial communication over USB. The code listens for incoming data and toggles the LED based on the received command.

### USB CDC Initialisation

Lets setup the USB CDC in STM32CubeMX. Find the board and create a new project - `serial-device`.

1. Under `System Core | RCC`, enable `HSE` and `LSE` by setting them both to `Crystal/Ceramic Resonator`.
2. Under `Connectivity | USB`, enable `Device (FS)`  - This should enable USB Device middlewares.
3. Under `Middleware and Software Packs | USB Device`, in `Class For FS IP`, select `Communication Device Class (Virtual COM Port)`.
   1. In the `Configuration` section, I have set the following to detect the port easily:
      - `MANUFACTURER_STRING`: `Gollahalli`
      - `PRODUCT_STRING`: `SerialDeviceExample`

You might have errors in `Clock Configuration` tab, in that tab, click on `Resolve Clock Issues` to fix them.

### Generate the code and open it in STM32CubeIDE

Under `Project Manager`, make sure the `Toolchain / IDE` is set to `STM32CubeIDE`, then click on `Generate Code`. This will generate the code and open it in STM32CubeIDE.

### The Firmware Code

There are two main files we need to modify: `usb_device_if.c` and `main.c`. `usb_device_if.c` handles the USB CDC communication, while `main.c` contains the main loop and LED control logic.

#### `usb_device_if.c`

See {{< github-source src="https://github.com/akshaybabloo/stm32-virtual-comm-example/blob/main/serial-device/USB_Device/App/usbd_cdc_if.c" label="usbd_cdc_if.c" >}} for the complete code.

Most of the code is already generated for us, we just need to make sure that any data coming in can also be accessed by the main loop. We can do this by using a global variable to store the received data. Add the following `extern` declaration at the top of the file:

```c
/* USER CODE BEGIN PRIVATE_FUNCTIONS_DECLARATION */
extern void usb_data_received(uint8_t* buf, uint32_t len);
/* USER CODE END PRIVATE_FUNCTIONS_DECLARATION */
```

Then, in the `CDC_Receive_FS()` function, we can call this function to pass the received data to the main loop:

```c
static int8_t CDC_Receive_FS(uint8_t* Buf, uint32_t *Len)
{
  /* USER CODE BEGIN 6 */
  usb_data_received(Buf, *Len); // <-- Add this line to pass the data to the main loop
  USBD_CDC_SetRxBuffer(&hUsbDeviceFS, &Buf[0]);
  USBD_CDC_ReceivePacket(&hUsbDeviceFS);
  return (USBD_OK);
  /* USER CODE END 6 */
}
```

Now, we can handle the received data in the main loop.

#### `main.c`

See {{< github-source src="https://github.com/akshaybabloo/stm32-virtual-comm-example/blob/main/serial-device/Core/Src/main.c" label="main.c" >}} for the complete code.

We can use the `usb_data_received()` function to handle the received data. Which is:

```c
void usb_data_received(uint8_t* buf, uint32_t len) {
  // Handle the received data here
}
```

The native application sends 3 bytes to the STM32 board. Which are of type:

```c
typedef enum {
  LED_VALUE,
  STATE_VALUE,
  REQUEST_VALUE
} CommandType;
```

`LED_VALUE` can be any of the following values, here are three LEDs on the NUCLEO board, each of them have an enum assigned to them:

```c
// These are already defined in the `stm32wbxx_nucleo.h` file
typedef enum
{
  LED1 = 0,
  LED2 = 1,
  LED3 = 2,
  /* Color led aliases */
  LED_BLUE   = LED1,
  LED_GREEN  = LED2,
  LED_RED    = LED3
} Led_TypeDef;
```

`STATE_VALUE` is given by:

```c
typedef enum {
  LED_OFF = 0,
  LED_ON = 1
} Led_State;
```

`REQUEST_VALUE` is given by:

```c
typedef enum {
  LED_STATUS = 0,
  LED_SET = 1,
} Request_Type;
```

For example, to turn on the blue LED, the native application sends `011` to the STM32 board, which means `LED_VALUE = LED_BLUE`, `STATE_VALUE = LED_ON`, and `REQUEST_VALUE = LED_SET`. And to turn off the red LED, it sends `001` to the STM32 board, which means `LED_VALUE = LED_BLUE`, `STATE_VALUE = LED_OFF`, and `REQUEST_VALUE = LED_SET`.

## Conclusion

In this blog, we have seen how to setup a simple serial communication between an STM32 microcontroller and a web application using USB. We have also seen how to toggle an LED on the STM32 board using a web application. This setup can be extended to send and receive sensor data, control other peripherals, and create interactive applications.
