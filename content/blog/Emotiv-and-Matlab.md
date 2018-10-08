---
title: "Emotiv and Matlab"
date: 2016-06-06T16:29:14+12:00
draft: false
categories: ["Software"]
tags: ["Matlab"]
description: "Collecting data from Emotiv via Matlab."
ads: true
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
---

**The code can be found at [https://github.com/akshaybabloo/Emotiv-Matlab](https://github.com/akshaybabloo/Emotiv-Matlab)**

> Note 1: Please note that this only works on 32-bit version of Matlab

There are two ways to get the data from your Emotiv EPOC device

[One](https://github.com/akshaybabloo/Emotiv-Matlab/tree/master/one) -> Copyright (c) May 2010 The Johns Hopkins University Applied Physics Laboratory (JHU/APL).

[Two](https://github.com/akshaybabloo/Emotiv-Matlab/tree/master/two) -> Copyright (c) 2012, Gavin

**Table of Contents**

- [1 Structure](#1structure)
- [2 Requirements](#2requirements)
- [3 Installing `mex` compiler](#3installingmexcompiler)
- [4 Using `.m` files](#4usingmfiles)
    - [4.1 Using `one` (EEG Logger)](#41usingoneeeglogger)
    - [4.2 Using `two` (Emotiv EEG)](#42usingtwoemotiveeg)
- [5 Troubleshooting](#5troubleshooting)

**License**

The code is provided under their respective licenses and the tutorial is provided under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)

![CC](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)

## 1 Structure

```md
Emotiv-Matlab
|
+-- one
|   |
|   `-- eeglogger.m
+-- two <-- I prefer using this
|   |
|   +-- EmotivEEG.m
|   `-- ExampleUsage.m
+-- LICENSE
`-- README.md
```

## 2 Requirements

You would need the following softwares:

1.  Visual studion 2010 professional (for Matlab 2013a)
2.  Emotiv SDK v1.0 or v2.0

Emotiv SDk has the following files in `c:/ProgramFiles/Emotiv../doc/examples_Matlab`

1.  edk.dll
2.  edk.h
3.  edk_utils.dll
4.  edkErrorCode.h
5.  EmoStateDLL.h

> Note 2: To run these codes you would have to make sure `Emotiv Control Panel` is open and connected to Emotiv EPOC.

Go to [Emotiv](http://www.emotiv.com) website for more information.

## 3 Installing `mex` compiler

- Open Matlab (this has been tested on R2013a).
- Use mex to install c/c++ compiler by doing the following
- `mex -setup` (Please make sure the required compilers are installed eg: Visual Studio 2010 pro for Matlab R2013a or Microsoft Windows SDK 7.1)

```md
Welcome to mex -setup.  This utility will help you set up
a default compiler.  For a list of supported compilers, see
http://www.mathworks.com/support/compilers/R2013a/win32.html

Please choose your compiler for building MEX-files:

Would you like mex to locate installed compilers [y]/n?
```

- Enter `y` and press enter
- Then you should get the following

```md
Select a compiler:
[1] Lcc-win32 C 2.4.1 in C:\PROGRA~2\MATLAB\R2013A~1\sys\lcc
[2] Microsoft Visual C++ 2010 in c:\Program Files (x86)\Microsoft Visual Studio 10.0

[0] None

Compiler:
```

- Enter the number of the compiler which you want to install and then press enter, eg: `2`; then you will get the following

```md
Please verify your choices:

Compiler: Microsoft Visual C++ 2010
Location: c:\Program Files (x86)\Microsoft Visual Studio 10.0

Are these correct [y]/n?
```

- enter `y` and press enter. Then you will get the following

```md
***************************************************************************
  Warning: MEX-files generated using Microsoft Visual C++ 2010 require
           that Microsoft Visual Studio 2010 run-time libraries be
           available on the computer they are run on.
           If you plan to redistribute your MEX-files to other MATLAB
           users, be sure that they have the run-time libraries.
***************************************************************************


Trying to update options file: C:\Users\gollahalli\AppData\Roaming\MathWorks\MATLAB\R2013a\mexopts.bat
From template:              C:\PROGRA~2\MATLAB\R2013A~1\bin\win32\mexopts\msvc100opts.bat

Done . . .

**************************************************************************
  Warning: The MATLAB C and Fortran API has changed to support MATLAB
           variables with more than 2^32-1 elements.  In the near future
           you will be required to update your code to utilize the new
           API. You can find more information about this at:
           http://www.mathworks.com/help/matlab/matlab_external/upgrading-mex-files-to-use-64-bit-api.html
           Building with the -largeArrayDims option enables the new API.
**************************************************************************
```

- This means you have successfully installed the compiler for Matlab.
- **(OR)**
- If you select `1`, **Note: This is only applicable for Windows**, and you will get

```md
Please verify your choices:

Compiler: Lcc-win32 C 2.4.1
Location: C:\PROGRA~2\MATLAB\R2013A~1\sys\lcc

Are these correct [y]/n?
```

- Enter `y` then you will get

```md
Trying to update options file: C:\Users\gollahalli\AppData\Roaming\MathWorks\MATLAB\R2013a\mexopts.bat
From template:              C:\PROGRA~2\MATLAB\R2013A~1\bin\win32\mexopts\lccopts.bat

Done . . .

**************************************************************************
  Warning: The MATLAB C and Fortran API has changed to support MATLAB
           variables with more than 2^32-1 elements.  In the near future
           you will be required to update your code to utilize the new
           API. You can find more information about this at:
           http://www.mathworks.com/help/matlab/matlab_external/upgrading-mex-files-to-use-64-bit-api.html
           Building with the -largeArrayDims option enables the new API.
**************************************************************************
```

- This means you have installed the compiler for Matlab.

## 4 Using `.m` files

The `*.m` files are available in [one](https://github.com/akshaybabloo/Emotiv-Matlab/tree/master/one) and [Two](https://github.com/akshaybabloo/Emotiv-Matlab/tree/master/two).

### 4.1 Using `one` (EEG Logger)

When running this code make sure the files are in the proper structure

```md
your_folder_name
|
+-- eeglogger.m
+-- edk.dll
+-- edk.h
+-- edk_utils.dll
+-- edkErrorCode.h
`-- EmoStateDLL.h
```

- Make sure your Emotiv Control Panel is open.
- Plug in the USB Bluetooth and switch on the Emotiv EEG Headset.
- Open Matlab, add `eeglogger.m`, `*.dll` and `*.h` files in the same folder.
- Open `eeglogger.m` file and run it.
- You should get the following

```md
EDK library loaded

nf =

    'EE_CheckSecurityCode'    'EE_GetSecurityCode'


w =

     ''



sampFreqOut =

         128

Warning: The following error was caught while executing 'EmotivEEG' class destructor:
Method 'delete' is not defined for class 'EmotivEEG' or is removed from MATLAB's search path.

ans =

     0
```

### 4.2 Using `two` (Emotiv EEG)

```md
your_folder_name
|
+-- EmotivEEG.m
+-- ExampleUsage.m
+-- edk.dll
+-- edk.h
+-- edk_utils.dll
+-- edkErrorCode.h
`-- EmoStateDLL.h
```

- Make sure you have opened `EmotivEEG.m`, `ExampleUsage.m` added all `*.dll` & `*.h` files in the same folder.
- Open Emotiv Control Panel and connect your Emotiv headset.
- I have commented a piece of code in that, I will tell you about this as we go further.

```matlab
% for i = 1:20
%     data_local = h.data;
%     data_local = (data_local+1)*10;
%     plot(data_local);
%     pause(0.5);
% end
```

- Now go to `ExampleUsage.m` file and run it (This will record your brain for the given seconds and show you the plot of it).
- you should get this in the Matlab

```md
>>ExampleUsage
Warning: The function 'EE_GetSecurityCode' was not found in the library
> In loadlibrary at 403
  In EmotivEEG>EmotivEEG.EmotivEEG at 73
  In ExampleUsage at 2
Warning: The function 'EE_CheckSecurityCode' was not found in the library
> In loadlibrary at 403
  In EmotivEEG>EmotivEEG.EmotivEEG at 73
  In ExampleUsage at 2
EDK library loaded
Successfully connected to Emotiv Systems-5
Warning: You should not run the timer and record simultaneously. Stopping the timer
> In EmotivEEG>EmotivEEG.Record at 160
  In ExampleUsage at 13
Recording... recieved  ,42 samples so far in0.004 secs. Still waiting for 1240 of 1280 samples
Recording... recieved  ,86 samples so far in0.356 secs. Still waiting for 1196 of 1280 samples
Recording... recieved  ,134 samples so far in0.72 secs. Still waiting for 1148 of 1280 samples
Recording... recieved  ,178 samples so far in1.077 secs. Still waiting for 1104 of 1280 samples
Recording... recieved  ,222 samples so far in1.436 secs. Still waiting for 1060 of 1280 samples
Recording... recieved  ,270 samples so far in1.796 secs. Still waiting for 1012 of 1280 samples
Recording... recieved  ,318 samples so far in2.156 secs. Still waiting for 964 of 1280 samples
Recording... recieved  ,362 samples so far in2.514 secs. Still waiting for 920 of 1280 samples
Recording... recieved  ,410 samples so far in2.873 secs. Still waiting for 872 of 1280 samples
Recording... recieved  ,454 samples so far in3.236 secs. Still waiting for 828 of 1280 samples
Recording... recieved  ,498 samples so far in3.592 secs. Still waiting for 784 of 1280 samples
Recording... recieved  ,546 samples so far in3.954 secs. Still waiting for 736 of 1280 samples
Recording... recieved  ,590 samples so far in4.308 secs. Still waiting for 692 of 1280 samples
Recording... recieved  ,638 samples so far in4.67 secs. Still waiting for 644 of 1280 samples
Recording... recieved  ,682 samples so far in5.032 secs. Still waiting for 600 of 1280 samples
Recording... recieved  ,730 samples so far in5.391 secs. Still waiting for 552 of 1280 samples
Recording... recieved  ,774 samples so far in5.746 secs. Still waiting for 508 of 1280 samples
Recording... recieved  ,822 samples so far in6.11 secs. Still waiting for 460 of 1280 samples
Recording... recieved  ,866 samples so far in6.466 secs. Still waiting for 416 of 1280 samples
Recording... recieved  ,914 samples so far in6.825 secs. Still waiting for 368 of 1280 samples
Recording... recieved  ,962 samples so far in7.186 secs. Still waiting for 320 of 1280 samples
Recording... recieved  ,1006 samples so far in7.544 secs. Still waiting for 276 of 1280 samples
Recording... recieved  ,1054 samples so far in7.905 secs. Still waiting for 228 of 1280 samples
Recording... recieved  ,1098 samples so far in8.266 secs. Still waiting for 184 of 1280 samples
Recording... recieved  ,1146 samples so far in8.627 secs. Still waiting for 136 of 1280 samples
Recording... recieved  ,1190 samples so far in8.981 secs. Still waiting for 92 of 1280 samples
Recording... recieved  ,1238 samples so far in9.344 secs. Still waiting for 44 of 1280 samples
Recording... recieved  ,1282 samples so far in9.699 secs. Still waiting for 0 of 1280 samples
Recording complete. Saved to EEGlog20141125T140701.mat
Successfully disconnected from Emotiv Systems-5
```

- Now comment this

```matlab
% lastfilename = h.Record(10);
% h.LoadRecordedData(lastfilename)
% data_local = h.data;
% plot(data_local);
```

- And uncomment this

```matlab
for i = 1:5
    data_local = h.data;
    data_local = (data_local+1)*10;
    plot(data_local);
    pause(0.5);
end
```

- Save this file (ExampleUsage.m) and run it.
- You should get the following

```md
>>ExampleUsage

EDK library loaded
Successfully connected to Emotiv Systems-5
Successfully disconnected from Emotiv Systems-5
```

- you can also see that a plot is updated dynamically.

## 5 Troubleshooting

- Have you tried using their example files and running it? You should try this.
- Try downgrading your Matlab to 2013b or 2014b (if using 2015, I have tested the code on this and works fine)
- Make sure you have installed the `mex` installer and have the `visual studio` before doing it.
- I have tried this on Windows 7, may be that could be an issue.
