---
title: "Using Dirent With Msvc Compilers"
date: 2017-12-12T12:58:56+12:00
draft: false
categories: ["Tutorial"]
tags: ["C++"]
description: "Using Dirent With Msvc Compilers"
ads: true
---

At the time of writing this blog, I am developing a C++ version of my [Spiks](https://github.com/akshaybabloo/Spikes) library - [libSpikes](https://github.com/akshaybabloo/libSpikes). I was compiling the `libSpikes` using [Cygwin](https://www.cygwin.com/) and [MinGW](http://www.mingw.org/). 

If you have used Linux before you can recognise the way Cygwin folder is structured. Cygwin tends to create a complete POSIX environment on the Windows, that means it brings loads of DLL files to compile C++ files. MinGW, on the other hand, brings the functionality of Win 32 API's and also provides specific POSIX API's.

Microsoft released [MSVC toolset for VS2017 and VS2015](https://blogs.msdn.microsoft.com/vcblog/2017/11/02/visual-studio-build-tools-now-include-the-vs2017-and-vs2015-msvc-toolsets/?utm_source=vs_developer_news&utm_medium=referral), which is an independent installation of their developer tools.

Linux has a fantastic library called `dirent.h`, I use it for listing the directory contents, Visual C++ does not provide this library (though they use a [different way](https://msdn.microsoft.com/en-us/library/windows/desktop/aa365200(v=vs.85).aspx)) and creating a custom directory listing was not an answer. So, [dirent](https://github.com/tronkko/dirent) is a POSIX port of dirent header to Windows.

To use this, do the following:

1. If you are using the MSVC toolset, you would have to clone the repository from [https://github.com/tronkko/dirent](https://github.com/tronkko/dirent).
2. Copy the `dirent.h` from the `include` folder and paste it in `C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Tools\MSVC\14.12.25827\include` - `14.12.25827` is the build number of the tools that I have installed, yours could be different.

That's it. You should be able to use it as you would use it in a POSIX. Or you could do something like this:

In my project, I have a folder called `libWins`; this is where I keep all my 3rd party windows related header files. I copied `dirent.h` to this folder.  Then in the root `CMakeLists.txt` I have the following

```
set(EXTERNAL_LIBS_WINDOWS "${PROJECT_SOURCE_DIR}/winLibs")

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
    INCLUDE_DIRECTORIES ( "${EXTERNAL_LIBS_WINDOWS}" )
endif()
```

If you are using Visual Studio, then you can add the header file to `C:\Program Files\Microsoft Visual Studio 14.0\VC\include`.

Happy coding.