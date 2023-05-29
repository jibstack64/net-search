# net-search

![GitHub](https://img.shields.io/github/license/jibstack64/net-search)

*Finds open and active user accounts on a Windows system/domain.*

Functions on Windows 7+ only, of course.

Syntax: `python ns.py [parameters]` - `parameters` are appended directly to the `net user` command, `/domain` for example.

This is limited in use but is convenient when you want to exploit a large-scale domain server (or messy/old local machine) by logging into vulnerable accounts. Despite being minimal, I believe some of the classes and functions in the script may pose useful in your projects; if so, feel free to borrow.