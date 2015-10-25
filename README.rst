Peacock Image Viewer
====================

This is a very simple picture viewer written in Python using Tkinter.

Goals
-----
    * Portability - runs on Windows, OSX, Linux, wherever
    * Lean - This is what you'd get by clicking on files in a file explorer
             plus the ability to tag images.
    * Non-intrusive - Unlike many picture viewing programs, this doesn't
             require or let you to move files around or change their metadata.
             That makes it a good fit for environments where you want to give
             other users the ability to view pictures without editting them.
    * Works on the Raspberry Pi - Self explanatory.

Progress
--------
This project is extremely simple at the moment. I'm still evaluating other
solutions to the problems I'm trying to solve.


Requirements
------------
This uses the "Pillow" library, a "friendly-fork" of Pil. Unfortunately this
means you have to build Pil stuff which can be a pain.

Windows
^^^^^^^
To build this sucker right you need to download or have a copy of Visual C++.

This gets into the sucky mess that is using Python with C or C++ extensions.

That's beyond the scope of this text file, but basically if you get the
worthless error message "unable to find vcvarsall.bat" you know this is the
problem.

There should be a
The easiest way to get this is by downloading Visual Studio 2012 Express.
Then add this to your %PATH% environment variable:

..code: bash

    set PATH=%PATH%;C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC

However this is considered sinful by some and can lead to other problems. Works
on my box though!

Installation
------------

    $ python.exe -m venv peacock-venv
    $ peacock-venv/Scripts/activate
    $ pip install -r requirements
    $
