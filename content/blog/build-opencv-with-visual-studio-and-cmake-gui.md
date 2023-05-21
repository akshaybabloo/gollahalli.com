---
title: "Build OpenCV With Visual Studio and CMake GUI"
date: 2023-02-25T12:15:12+13:00
draft: false
categories: ["C++"]
tags: ["C++", "OpenCV", "Visual Studio", "CMake"]
description: "This blog is a tutorial on how to build OpenCV with Visual Studio and CMake GUI. It includes two parts: generating OpenCV build files using CMake GUI and building OpenCV using Visual Studio 2022 Community. The tutorial provides step-by-step instructions and tips and tricks for the process."
images: ["/img/blog/build-opencv-with-visual-studio-and-cmake/Build-OpenCV-with-Visual-Studio-and-CMake-GUI-cover.png", "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui.png", "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-after-configure.png", "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-build-opencv-world.png", "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-compiler-setup.png", "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-generator.png", "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-install-prefix.png", "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-set-environment-variables.png", "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-source-build-path.png", "/img/blog/build-opencv-with-visual-studio-and-cmake/vs-solution-explorer.png"]
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
  - imageLoc: "/img/blog/build-opencv-with-visual-studio-and-cmake/Build-OpenCV-with-Visual-Studio-and-CMake-GUI-cover.png"
    imageCaption: "Build OpenCV With Visual Studio and CMake GUI"
  - imageLoc: "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui.png"
    imageCaption: "CMake GUI"
  - imageLoc: "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-after-configure.png"
    imageCaption: "CMake GUI after configure"
  - imageLoc: "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-build-opencv-world.png"
    imageCaption: "CMake GUI build opencv_world"
  - imageLoc: "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-compiler-setup.png"
    imageCaption: "CMake GUI compiler setup"
  - imageLoc: "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-generator.png"
    imageCaption: "CMake GUI generator"
  - imageLoc: "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-install-prefix.png"
    imageCaption: "CMake GUI install prefix"
  - imageLoc: "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-set-environment-variables.png"
    imageCaption: "CMake GUI set environment variables"
  - imageLoc: "/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-source-build-path.png"
    imageCaption: "CMake GUI source build path"
  - imageLoc: "/img/blog/build-opencv-with-visual-studio-and-cmake/vs-solution-explorer.png"
    imageCaption: "Visual Studio solution explorer"
---

<!--adsense-->

> If you want to use the command line approach, check out my other blog - [Build OpenCV With Visual Studio and CMake CLI]({{< ref "build-opencv-with-visual-studio-and-cmake-cli.md" >}}).

If you have ever used OpenCV, you would know that it is a very powerful library for image processing. This is owing to ease in usage and availability of multiple functions which can be utilised to perform a variety of image processing tasks. In this post, we will explore the steps on how to build OpenCV with Visual Studio and Cmake GUI.

There are two sections to this blog:

1. Generating OpenCV build files using CMake GUI
2. Building OpenCV using Visual Studio 2022 Community

**Table of Contents**

- [Prerequisites](#prerequisites)
- [Section 1: Generating OpenCV build files using CMake GUI](#section-1-generating-opencv-build-files-using-cmake-gui)
  - [Step 1: Know where to find the files](#step-1-know-where-to-find-the-files)
  - [Step 2: Download OpenCV](#step-2-download-opencv)
  - [Step 3: Open CMake GUI](#step-3-open-cmake-gui)
  - [Step 4: Set the source and build directories](#step-4-set-the-source-and-build-directories)
  - [Step 5: Configure build and compiler settings](#step-5-configure-build-and-compiler-settings)
  - [Step 6: Set install location and generate build files](#step-6-set-install-location-and-generate-build-files)
- [Section 2: Building OpenCV using Visual Studio 2022 Community](#section-2-building-opencv-using-visual-studio-2022-community)
- [Few tips and tricks](#few-tips-and-tricks)
  - [CMake for Visual Studio](#cmake-for-visual-studio)
  - [An alternate way to set compiler location](#an-alternate-way-to-set-compiler-location)
  - [Build `opencv_world` library](#build-opencv_world-library)
- [Conclusion](#conclusion)

<!--adsense-->

## Prerequisites

Before we begin, you need to have the following on your computer:

1. [Visual Studio 2022 Community](https://visualstudio.microsoft.com/downloads/) with C++ support
2. [CMake](https://cmake.org/download/) - I am using CMake 3.24.
3. [OpenCV](https://opencv.org/releases/) - I am using OpenCV 4.7.0.
4. [Python](https://www.python.org/downloads/) - I am using Python 3.10.

> Note: Though, CMake is installed with Visual Studio, I would also recommend installing it separately. This will make it easier to use CMake with other IDEs.

## Section 1: Generating OpenCV build files using CMake GUI

Fun part! Let's build OpenCV.

### Step 1: Know where to find the files

First, find the location of VSC Compiler and CMake. VSC uses `cl.exe` as the compiler and CMake GUI uses `cmake-gui.exe`. You can find these files in the following locations:

- For Visual Studio 2022 Community - `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64\cl.exe`
- For CMake - `C:\Program Files\CMake\bin\cmake-gui.exe`

> Note: The version of the compiler could be different. You can find the version of the compiler in - `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\Microsoft.VCToolsVersion.default.txt`. Or, you can also select the latest compiler from `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\`.

### Step 2: Download OpenCV

Download OpenCV from [https://opencv.org/releases](https://opencv.org/releases/). As mentioned previously, I am using OpenCV 4.7.0. You can use any version of OpenCV that you like. Extract the zip file to a location of your choice. I am extracting it to `C:\Users\<user>\Downloads\opencv-4.7.0`. Open the extracted folder and create a new folder called `build`. This is where the build files will be generated.

<!--adsense-->

### Step 3: Open CMake GUI

Open CMake GUI. You can find it in the following location - `C:\Program Files\CMake\bin\cmake-gui.exe`. You can also search for it in the start menu. Once you open it, you will see the following screen:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui.png" title="CMake GUI" alt="CMake GUI" width="300" >}}

### Step 4: Set the source and build directories

Now, let's set the source and build directories.

- Source Directory - `C:\Users\<user>\Downloads\opencv-4.7.0`
- Build Directory - `C:\Users\<user>\Downloads\opencv-4.7.0\build`

This is how it should look like:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-source-build-path.png" title="CMake GUI Source and Build Path" alt="CMake GUI Source and Build Path" width="300" >}}

### Step 5: Configure build and compiler settings

In this step, we will configure the build with appropriate compiler location.

1. Click on `Configure`, this should open a pop-up window. Select `Visual Studio 17 2022` and from the options, select `Specify native compilers`. This should look like:

  {{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-generator.png" title="CMake GUI Configure Generator" alt="CMake GUI Configure" width="300" caption="1. Select Visual Studio 17 2022 from the drop down. 2. Select \"Specify native compilers\". 3. Click \"Next\" to go to next screen" >}}

2. Now, click on `Next`. This should take you to a place where you can set the native compiler location. Remember the `cl.exe` location? That's what we have to set here. Set the following variables:
   - Under `C` and `C++` fields, set it to `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64\cl.exe`

  {{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-compiler-setup.png" title="CMake GUI Configure Compiler" alt="CMake GUI Configure Compiler" width="300" caption="1. Add in the compiler path. And 2. Click \"Finish\"" >}}

And finally, click on `Finish`. This should take you back to the CMake GUI window and generate the build files. This will take some time; and should look like:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-after-configure.png" title="CMake GUI Configure" alt="CMake GUI Configure" width="300" >}}

> Note: Create a folder called `install` in the build directory, if it does not exist.

<!--adsense-->

### Step 6: Set install location and generate build files

In the search field, search for `CMAKE_INSTALL_PREFIX`. Edit `CMAKE_INSTALL_PREFIX` value by double-clicking on it and set it to `C:\Users\<user>\Downloads\opencv-4.7.0\build\install`. This should look like:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-install-prefix.png" title="CMake GUI Configure Installation Path" alt="CMake GUI Configure Installation Path" width="300" caption="1. In the search field, type in \"install\". 2. Edit \"CMAKE_INSTALL_PREFIX\" to add the install path. 3. Click \"Generate\"" >}}

Once you have setup the install path, click on `Generate`. This should generate Visual Studio solution files.

## Section 2: Building OpenCV using Visual Studio 2022 Community

> Warning: This will take a lot of time. So, go grab a cup of coffee (or even tea).

Once the Visual Studio solution files are generated, you can either click on `Open Project`, beside the `Generate` button. Or go to `C:/Users/<user>/Downloads/opencv-4.7.0/build` and click `OpenCV.sln`. This should open Visual Studio 2022 Community.

In your solutions explorer, under `CMakeTargets`, you should see `INSTALL`. Right-click on `INSTALL` and select `Build`. This should build OpenCV.

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/vs-solution-explorer.png" title="Visual Studio Build" alt="Visual Studio Build" width="300" >}}

Once the build is complete, you can find the OpenCV files/binaries in the following locations: 

- Include files - `C:\Users\<user>\Downloads\opencv-4.7.0\build\install\include\opencv2`
- Binaries - `C:\Users\<user>\Downloads\opencv-4.7.0\build\install\x64\vc17\bin`
- Libraries - `C:\Users\<user>\Downloads\opencv-4.7.0\build\install\x64\vc17\lib`

## Few tips and tricks

These are some tips and tricks that I have learnt while building OpenCV using Visual Studio 2022 Community and CMake GUI.

<!--adsense-->

### CMake for Visual Studio

CMake for Visual Studio can be found in - `C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake`

### An alternate way to set compiler location

As an alternative to [Step 5](#step-5-configure-build-and-compiler-settings), we can manually set the compiler location in the environment variables. Do the following:

For the compiler, click on `Environment` button on top right of the window and set the following variables:

- `CMAKE_CXX_COMPILER` - `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64\cl.exe`
- `CMAKE_C_COMPILER` - `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64\cl.exe`

These should look like:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-set-environment-variables.png" title="CMake GUI set compiler environment variables" alt="CMake GUI set compiler environment variables" width="300" caption="1. Click on \"Environment\" button, this will open \"Environment Editor\". 2. Click on \"+ Add Entry\". 3. Edit \"Name\" and \"Value\" with the compiler type and path. 4. Click on \"OK\" to save and close the window. 5. Once, both variables are added click on \"OK\" in \"Environment Editor\"." >}}

And finally, click on option `Use default native compilers` and click on `Finish`.

<!--adsense-->

### Build `opencv_world` library

By default, CMake will build individual libraries for each module. If you want to build a single library, you can do the following:

1. In the search field, search for `BUILD_opencv_world`. Click on the checkbox to enable it. This should look like:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-build-opencv-world.png" title="CMake GUI build opencv_world" alt="CMake GUI build opencv_world" width="300" >}}

2. Click on `Configure` and then `Generate`. This should generate the build files. Now, you can build the `INSTALL` target as mentioned in [Building OpenCV using Visual Studio 2022 Community](#part-2-building-opencv-using-visual-studio-2022-community).

<!--adsense-->

## Conclusion

So now, we have seen how to build OpenCV using Visual Studio 2022 Community and CMake GUI. We have also seen how to set up the environment variables for CMake to use the compiler. I hope you found this article useful. If you have any questions, feel free to ask them in the comments section below.

Until next time, happy coding!

**Update**

1. Added link to [Build OpenCV With Visual Studio and CMake CLI]({{< ref "build-opencv-with-visual-studio-and-cmake-cli.md" >}}).
2. Changed "Part 1" to "Section 1" and "Part 2" to "Section 2".