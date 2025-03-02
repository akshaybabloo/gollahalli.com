---
title: "Tauri 2 With Flutter: A Template"
date: 2024-12-22T23:38:20+13:00
draft: false
categories: ["Tauri", "Flutter"]
tags: ["Tauri", "Flutter", "Rust", "Dart"]
description: "Tauri 2 with Flutter template is a great way to build cross-platform desktop applications using Rust and Flutter. This article will guide you through the process of setting up a new project using Tauri 2 with Flutter."
images: ["tauri-flutter.png"]
ads: true
video: true
videos: ["tauri-screencast.webm"]
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
  - imageLoc: "tauri-flutter.png"
    imageCaption: "Tauri 2 With Flutter Template"
siteMapVideos:
  - videoLoc: "tauri-screencast.webm"
    videoDescription: "Example of Flutter and Tauri 2 integration"
---

<!--adsense-->

The template can be found at {{< github-source src="https://github.com/akshaybabloo/tauri_flutter_template" label="akshaybabloo/tauri_flutter_template" >}}

## Introduction

Tauri is a modern framework for building desktop applications using web technologies, powered by Rust. It stands out as a lightweight, fast, and secure alternative to Electron. On the other hand, Flutter is a versatile UI toolkit that enables developers to create natively compiled applications for mobile, web, and desktop from a single codebase. By combining the strengths of Tauri and Flutter, you can craft efficient, cross-platform desktop applications with the robustness of Rust and the flexibility of Flutter.

In this article, we’ll explore how to set up a new project using Tauri 2 and Flutter.

## Prerequisites

Before we begin, make sure you have the following installed on your system:

- [Flutter](https://flutter.dev/docs/get-started/install)
- [Bun](https://bun.sh/) - An alternative to npm and yarn.
- [Node.js](https://nodejs.org/en/)
- [Rust](https://www.rust-lang.org/tools/install)

## Creating a New Project

Once we have the prerequisites installed, we can create individual projects for both Tauri and Flutter, then configure Tauri to integrate seamlessly with Flutter.

### Tauir Project

{{<alert>}}
Make sure your project name has underscores instead of hyphens. For example, `tauri_app` instead of `tauri-app`. Flutter does not support hyphens in the project name.
{{</alert>}}

Lets create a Tauri project with vanilla JavaScript as the UI.

```bash
bun create tauri-app
```

Use these initial configurations:

```md
$ bun create tauri-app
✔ Project name · tauri_app
✔ Identifier · com.gollahalli.tauri-flutter-template
✔ Choose which language to use for your frontend · TypeScript / JavaScript - (pnpm, yarn, npm, deno, bun)
✔ Choose your package manager · bun
✔ Choose your UI template · Vanilla
✔ Choose your UI flavor · JavaScript
```

We should now have a folder called `tauri_app` with the following structure:

```md
tauri_app
├── package.json
├── README.md
├── src/
└── src-tauri/
```

The `src` folder typically contains JavaScript code for the UI, while the `src-tauri` folder houses the Rust code for the backend. Since we’ll be using Flutter for the UI, we can safely delete the `src` folder.

### Flutter Project

In the `tauri_app` folder, create a new Flutter project, using:

```bash
flutter create --org=com.gollahalli.tauri-flutter-template --platforms=web .
```

This command creates a new Flutter project with the organization name `com.gollahalli.tauri-flutter-template` and the platform set to web. The `.` at the end tells Flutter to create the project in the current directory.

Now we should have a structure like this:

```md
tauri_app
├── analysis_options.yaml
├── lib/
├── package.json
├── pubspec.lock
├── pubspec.yaml
├── README.md
├── src-tauri/
├── tauri_app.iml
├── test/
└── web/
```

The `web` folder contains the Flutter web project, but we don’t need to maintain it manually as Flutter handles it for us. The `lib` folder is where the Dart code for the UI resides, while the `test` folder is designated for testing the Dart code.

### Configuring Tauri to Use Flutter

Tauri simplifies the process of integrating any web application into a desktop application. To integrate Flutter Web with Tauri, we need to update the Tauri configuration.

Under the `src-tauri` directory, open the `tauri.conf.json` file, and add change following configuration:

```diff
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "tauri-app",
  "version": "0.1.0",
  "identifier": "com.gollahalli.tauri-flutter-template",
  "build": {
+    "beforeDevCommand": "flutter run -d web-server --web-port 5000",
+    "devUrl": "http://localhost:5000",
+    "beforeBuildCommand": "flutter build web",
-    "frontendDist": "../src"
+    "frontendDist": "../build/web"
  },
  "app": {
    "withGlobalTauri": true,
    "windows": [
      {
        "title": "tauri-app",
        "width": 800,
        "height": 600
      }
    ],
    "security": {
      "csp": null
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

- The `beforeDevCommand` runs the Flutter web server on port `5000` before starting the Tauri development server.
- The `devUrl` points Tauri to the local Flutter web server running at `http://localhost:5000`.
- The `beforeBuildCommand` ensures the Flutter web project is built before the Tauri project.
- The `frontendDist` is updated to `../build/web`, which is the output directory for the Flutter web build.

### Running the Project

With the configurations in place, you can now run the project using the following command:

```bash
bun run tauri dev
```

This command starts the Flutter web server along with the Tauri development server. Once running, you’ll see the Flutter web project displayed inside the Tauri application window.

{{< figure src="tauri-screenshot.png" caption="Screenshot of Flutter UI in Tauri window." width="600" >}}

If you only need to run the UI, the setup is complete, and you’re good to go. However, if you want to enable communication between the Flutter UI and the Rust backend, keep reading for the next steps.

## Functional Add Button

The integration is working! However, the `+` button currently uses Flutter to handle its functionality instead of calling the Rust backend. Let’s modify this behaviour by utilising Tauri’s IPC (Inter-Process Communication) to connect the Flutter UI with the Rust backend.

### Rust Backend

Under `src-tauri/src`, open `lib.rs` and add the following code:

```rust
#[tauri::command]
fn add_one(number: &str) -> String {
    print!("Adding 1 to {}\n", number);
    let number: i32 = number.parse().unwrap();
    let result = number + 1;
    result.to_string()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![add_one]) // <-- Add add_one to this line
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

This code defines a new Tauri command, `add_one`, which takes a number as a string, increments it by 1, and returns the result as a string. The `invoke_handler` is updated to include this command, enabling the Flutter UI to call it via Tauri's IPC.

### Flutter Frontend

To enable communication between Flutter and the Rust backend, we need to create a JavaScript (JS) interop layer. First, add the web package to your Flutter project by running the following command:

```bash
flutter pub add web
```

Next, in the `lib` folder, create a new file named `tauri.dart` and add the following code:

```dart
import 'dart:js_interop';
import 'package:web/web.dart';

@JS()
@staticInterop
class _Tauri {}

@JS()
@staticInterop
class _TauriCore {}

extension TauriCoreExtension on _TauriCore {
  external JSPromise<JSAny> invoke(JSAny target, JSAny? args);
}

extension TauriExtension on _Tauri {
  external _TauriCore get core;
}

extension TauriInterop on Window {
  /// Invokes a Tauri command.
  Future<Object?> invoke(String cmd, [Map<String, Object?> args = const {}]) async {
    final result = await __TAURI__.core.invoke(cmd.toJS, args.jsify()).toDart;
    return result.dartify();
  }

  external _Tauri get __TAURI__;
}
```

This code extends the `window` object in JavaScript to include a method for invoking Tauri commands using `__TAURI__.core.invoke`. This allows the Flutter frontend to call Rust backend commands through the interop layer, making it easy to integrate the two environments.

Now, let’s update the `main.dart` file to ensure the Rust backend is called when the `+` button is clicked. Here’s how it looks:

```dart
import 'package:tauri_flutter_template/tauri.dart';
import 'package:web/web.dart' as web;

// Removed the existing code for brevity

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          try {
            // Call the Rust backend to add 1 to the counter
            final value = await web.window.invoke("add_one", {'number': _counter.toString()});
            setState(() {
              // Update the counter with the new value
              _counter = int.parse(value.toString());
            });
          } catch (e) {
            print(e);
          }
        },
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

The `onPressed` function of the floating action button now invokes the `add_one` command from the Rust backend, passing the current counter value as a string. The Rust function processes this value and returns the incremented result. The state is then updated with the new value, ensuring the UI reflects the change.

Rerun the project using the following command:

```bash
bun run tauri dev
```

Now, clicking the `+` button will call the Rust backend and increment the counter by 1.

{{< video src="tauri-screencast.webm" >}}

## Few Things to Note

- The Flutter web app must be running in web server mode to function correctly. Unlike standard Flutter apps, you can't use the hot restart feature by pressing `r` in the terminal. Instead, you'll need to stop the Tauri app and restart it using `bun run tauri dev`.
- Attaching Flutter DevTools to the Flutter web app running inside the Tauri application doesn’t seem to work with this setup. This might require a different configuration or workaround.
- After the initial run, the app might not load properly. If this happens, simply right-click within the app and select `Reload` to refresh the page. This resolves the issue.

## Conclusion

Tauri 2 and Flutter together offer a powerful solution for building cross-platform desktop applications, combining the performance and security of Rust with the flexibility and beauty of Flutter. By following the steps outlined in this article, you can create a new project with Tauri 2 and Flutter, seamlessly integrating a Flutter web UI with a Rust backend. This combination opens up a wealth of possibilities for creating fast, secure, and visually stunning desktop applications.

While the integration works well overall, there are a few limitations to note. If you manage to overcome any of the challenges mentioned, please share your solutions in the comments below—I’d love to hear how you tackled them!
