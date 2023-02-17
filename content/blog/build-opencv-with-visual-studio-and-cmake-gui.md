---
title: "Build OpenCV With Visual Studio and CMake GUI"
date: 2023-02-17T12:15:12+13:00
draft: false
categories: []
tags: []
description: ""
images: []
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
# siteMapImages:
#   - imageLoc: ""
#     imageCaption: ""
---

<!--adsense-->

If you have every used OpenCV, you would know that it is a very powerful library for image processing. It is very easy to use and has a lot of functions that can be used to perform a lot of image processing tasks. In this post, I will show you how to build OpenCV with Visual Studio and Cmake.

There are two parts in this post:

1. Generating OpenCV build files using CMake GUI
2. Building OpenCV using Visual Studio 2022 Community

**Table of Contents**

- [Prerequisites](#prerequisites)
- [Part 1: Generating OpenCV build files using CMake GUI](#part-1-generating-opencv-build-files-using-cmake-gui)
  - [Step 1: Know where to find the files](#step-1-know-where-to-find-the-files)
  - [Step 2: Download OpenCV](#step-2-download-opencv)
  - [Step 3: Open CMake GUI](#step-3-open-cmake-gui)
  - [Step 4: Set the source and build directories](#step-4-set-the-source-and-build-directories)
  - [Step 5: Configure build](#step-5-configure-build)
  - [Step 6: Set install location and generate build files](#step-6-set-install-location-and-generate-build-files)
- [Part 2: Building OpenCV using Visual Studio 2022 Community](#part-2-building-opencv-using-visual-studio-2022-community)
- [Few tips and tricks](#few-tips-and-tricks)
  - [CMake for Visual Studio](#cmake-for-visual-studio)
  - [An alternate way to set compiler location](#an-alternate-way-to-set-compiler-location)
  - [Build `opencv_world` library](#build-opencv_world-library)
- [Conclusion](#conclusion)


## Prerequisites

Before you start, you need to have the following installed on your computer:

1. [Visual Studio 2022 Community](https://visualstudio.microsoft.com/downloads/) with C++ support - I am using Visual Studio 2022 Community edition.
2. [CMake](https://cmake.org/download/) - I am using CMake 3.24.
3. [OpenCV](https://opencv.org/releases/) - I am using OpenCV 4.7.0.
4. [Python](https://www.python.org/downloads/) - I am using Python 3.10.

> Note: Though, CMake is installed with Visual Studio, I would recommend installing it separately as well. This will make it easier to use CMake with other IDEs. Also, we will be using cmake-gui to build OpenCV.

-DBUILD_opencv_world:BOOL="1" -DCMAKE_INSTALL_PREFIX:PATH="C:/Users/gollaha/Downloads/opencv-4.7.0/build/install" 

## Part 1: Generating OpenCV build files using CMake GUI

Fun part! Let's build OpenCV.

### Step 1: Know where to find the files

First, find the location of VSC Compiler and CMake. VSC uses `cl.exe` as the compiler and CMake uses `cmake.exe`. You can find the location of these files in the following locations:

- For Visual Studio 2022 Community - `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64\cl.exe`
- For CMake - `C:\Program Files\CMake\bin`

> Note: The version of the compiler could be different. You can find the version of the compiler in the following location - `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\Microsoft.VCToolsVersion.default.txt`. Or you can also select the latest compiler from `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\`.

### Step 2: Download OpenCV

Download OpenCV from [here](https://opencv.org/releases/). I am using OpenCV 4.7.0. You can use any version of OpenCV that you want. Extract the zip file to a location of your choice. I am extracting it to `C:\Users\<user>\Downloads\opencv-4.7.0`. Open the extracted folder and create a new folder called `build`. This is where the build files will be generated.

### Step 3: Open CMake GUI

Open CMake GUI. You can find it in the following location - `C:\Program Files\CMake\bin\cmake-gui.exe`. You can also search for it in the start menu. Once you open it, you will see the following screen:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui.png" title="CMake GUI" alt="CMake GUI" width="300" >}}

### Step 4: Set the source and build directories

Now, let's set the source and build directories, along with compiler and instillation location.

- Source Directory - `C:\Users\<user>\Downloads\opencv-4.7.0`
- Build Directory - `C:\Users\<user>\Downloads\opencv-4.7.0\build`

This is how it should look like:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-source-build-path.png" title="CMake GUI Source and Build Path" alt="CMake GUI Source and Build Path" width="300" >}}

### Step 5: Configure build

In this step we will configure the build with appropriate compiler location.

1. Click on `Configure`, this should open a pop-up window. Select `Visual Studio 17 2022` and from the options, select `Specify native compilers`. This should look like:

  {{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-generator.png" title="CMake GUI Configure Generator" alt="CMake GUI Configure" width="300" >}}

2. Now, click on `Next`. This should take you to a place where you can set native compiler location. Remember the `cl.exe` location? That's what we have to set here. Set the following variables:
   - Under `C` and `C++` fields, set it to `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64\cl.exe`

  {{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-compiler-setup.png" title="CMake GUI Configure Compiler" alt="CMake GUI Configure Compiler" width="300" >}}

And finally, click on `Finish`. This should take you back to the CMake GUI window and generate the build files. This will take some time; and should look like:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-after-configure.png" title="CMake GUI Configure" alt="CMake GUI Configure" width="300" >}}

> Note: Create a folder called `install` in the build directory, if it does not exist.

### Step 6: Set install location and generate build files

In the search filed, type in `search` and search for `CMAKE_INSTALL_PREFIX`. Edit `CMAKE_INSTALL_PREFIX` value by double-clicking on it and set it to `C:\Users\<user>\Downloads\opencv-4.7.0\build\install`. This should look like:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-install-prefix.png" title="CMake GUI Configure Installation Path" alt="CMake GUI Configure Installation Path" width="300" >}}

Once you have setup the install path, click on `Generate`. This should generate visual studio solution files.

## Part 2: Building OpenCV using Visual Studio 2022 Community

> Warning: This will take a lot of time. So, go grab a cup of coffee.

Once the Visual Studio solutions files are generated, you can either click on `Open Project`, beside the `Generate` button. Or go to `C:/Users/<user>/Downloads/opencv-4.7.0/build` and click `OpenCV.sln`. This should open Visual Studio 2022 Community.

In your solutions explorer, under `CMakeTargets`, you should see `INSTALL`. Right-click on `INSTALL` and select `Build`. This should build OpenCV.

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/vs-solution-explorer.png" title="Visual Studio Build" alt="Visual Studio Build" width="300" >}}

Once the build is complete, you can find the OpenCV binaries in the following location: 

- Include files - `C:\Users\<user>\Downloads\opencv-4.7.0\build\install\include\opencv2`
- Binaries - `C:\Users\<user>\Downloads\opencv-4.7.0\build\install\x64\vc17\bin`
- Libraries - `C:\Users\<user>\Downloads\opencv-4.7.0\build\install\x64\vc17\lib`

## Few tips and tricks

### CMake for Visual Studio

CMake for Visual Studio can be found in - `C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake`

### An alternate way to set compiler location

An alternate to [Step 5](#step-5-configure-build), we can manually set the compiler location in the environment variables. Do the following:

For the compiler, click on `Environment` button on top right of the window and set the following variables:

- `CMAKE_CXX_COMPILER` - `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64\cl.exe`
- `CMAKE_C_COMPILER` - `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64\cl.exe`

These should look like:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-set-environment-variables.png" title="CMake GUI set compiler environment variables" alt="CMake GUI set compiler environment variables" width="300" >}}

And finally, click on option `Use default native compilers` and click on `Finish`.

### Build `opencv_world` library

By default, CMake will build individual libraries for each module. If you want to build a single library, you can do the following:

1. In the search field, search for `BUILD_opencv_world`. Click on the checkbox to enable it. This should look like:

{{< figure src="/img/blog/build-opencv-with-visual-studio-and-cmake/cmake-gui-build-opencv-world.png" title="CMake GUI build opencv_world" alt="CMake GUI build opencv_world" width="300" >}}

2. Click on `Configure` and then `Generate`. This should generate the build files. Now, you can build the `INSTALL` target as mentioned in [Building OpenCV using Visual Studio 2022 Community](#building-opencv-using-visual-studio-2022-community).

## Conclusion

In this article, we have seen how to build OpenCV using Visual Studio 2022 Community and CMake. We have also seen how to set up the environment variables for CMake to use the compiler. I hope you found this article useful. If you have any questions, feel free to ask them in the comments section below.

Until next time, happy coding!