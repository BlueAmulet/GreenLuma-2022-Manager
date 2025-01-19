# GreenLuma 2024 Manager
An app to manage the Steam unlocker "GreenLuma 2024" AppList folder

This is a fork of ImaniiTy's GreenLuma Reborn Manager to better support GL2024  
Handles portable GL2024 (not in Steam folder)  
Better searching  
Improved error handling  
Other bugfixes and improvements

## Latest release: **[GreenLuma 2024 Manager](https://github.com/BlueAmulet/GreenLuma-2024-Manager/releases/latest)**
Below text is mostly sourced from ImaniiTy's README

## What is [GreenLuma 2024](https://cs.rin.ru/forum/viewtopic.php?f=29&t=103709)?
GreenLuma 2024 (GL2024) is a Steam unlocker made by Steam006 that is used to obtain games from family shared libraries and DLC for games. There's much more to it, though.

The full list of features provided by Steam006.

![alt text](https://imgur.com/zdCclTP.png)

## Can I get banned for using GreenLuma 2024?
There will always be a risk when using GL2024. If you're willing to take that risk, go right on ahead. If not, then don't bother. Especially when that risk means the status of your Steam account.

As expected, there are some games that blacklist GL2024 and using it will result in receiving a game ban.  
Some games will check for GreenLuma's files or the manager's files in the Steam folder.  
Some games have server side game and DLC ownership checks.

Please keep in mind. Like CreamAPI, GreenLuma 2024 **does not** work for every game.  
Also, keep in mind that not **every game** is available to play through Steam family sharing.

#### Credits to [@linkthehylian](https://github.com/linkthehylian) for this brief explanation

I **highly advise** you to use the "Legit stealth mode" checking the box "NoHook" on my program:
![alt text](https://i.imgur.com/xpAXU1b.png)

## Features
  * Easily manage profiles for various games (good to circumvent the 168 id limit)
    * Add/Remove 1 or more games at once
    * Add/Remove profiles
  * Search for any game you want to add direct from the app
    * Search results are directly from Steam
    * Sort the results by Type (DLC, Game, etc..) or Name
  * Generate the AppList, close Steam and run GreenLuma 2024 in one click
    * You can choose any GL2024 parameters before launch
    * It will detect whether Steam is open or not and close it if necessary
  * All the profiles info are in JSON files so you can easily share with anyone
    * The profiles are saved on: C:\Users\YOUR_USER\AppData\Local\GLR_Manager\Profiles

![alt text](https://i.imgur.com/B8nDYm3.png)

## Future Plans
* Work on the UI
* Add a way to load previous games on your AppList folder
* Load all DLC for a game instead of the first 64
* Better error handling
* Warnings if GL2024 or the manager are in the Steam folder
* Handling elevated permissions as necessary

## Built With
* [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) - The GUI framework
* [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/index.html) - Used to make the standalone executable

## Authors
[**ImaniiTy**](https://github.com/ImaniiTy):

![alt text](https://i.imgur.com/zmS7oBs.gif)

[**BlueAmulet**](https://github.com/BlueAmulet): This fork
