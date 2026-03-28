# SideGDB

a custom GDB UI made in Python.

## ⚠️⚠️ THIS IS ALPHA SOFTWARE ⚠️⚠️
Parts of this project could be rewritten when you least expect it: this documentation can get outdated very easily.
  
# VERY IMPORTANT NOTE

this program was made with OSDev in mind, i made it so that i could debug [my kernel](https://github.com/purpleK2/kernel) with something other than VSCode's debugger. I did NOT test this with your average C program that's supposed to run on your terminal, or something like that.

# Prerequisites

If you want to run directly the Python code from the repo, you'll have to do some preparation.

All required libraries are in the [requirements.txt](requirements.txt) file. Anyways, these are the needed libraries:
- `pygdbmi`:  [A library to parse gdb mi output](https://cs01.github.io/pygdbmi/) and interact with gdb subprocesses
- `PySide6`: the [official Qt Widgets implementation](https://doc.qt.io/qtforpython-6/) for Python
- `loguru`: [Python logging](https://pypi.org/project/loguru/) made (stupidly) simple

# Check out the [wiki](https://github.com/RepubblicaTech/SideGDB/wiki) for usage instructions

# CREDITS

- [Fugue Icons](assets/fugue) by [Yusuke Kamiyamane](http://p.yusukekamiyamane.com/). Licensed under a Creative Commons Attribution 3.0 License.
- [Upscaled Fugue](assets/fugue-2x) by [chrisjbillington](https://github.com/chrisjbillington/fugue-2x-icons)
