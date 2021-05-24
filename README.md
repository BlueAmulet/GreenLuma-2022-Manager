# GreenLuma 2020 Manager
An app to manage the Steam unlocker "GreenLuma 2020" AppList folder

This is a fork of ImaniiTy's GreenLuma Reborn Manager to better support GL2020

## What is [GreenLuma 2020](https://cs.rin.ru/forum/viewtopic.php?f=29&t=103709) ?
GreenLuma 2020 (GL2020) is a Steam unlocker made by Steam006 that is used to obtain games from family shared libraries and DLC for games. There's much more to it, though.

The full list of features provided by Steam006.

![alt text](https://i.imgur.com/D18pz0f.png)

## Can I get banned for using GreenLuma 2020 ?
There will always be a risk when using GL2020. If you're willing to take that risk, go right on ahead. If not, then don't bother. Especially when that risk means the status of your Steam account.

As expected, there are some games that blacklist GL2020 and using it will result in receiving a game ban. Refer to [this page](https://github.com/linkthehylian/GreenLuma-Reborn-App/wiki/Blacklist) if you want to check what games NOT to play.

Please keep in mind. Like CreamAPI, GreenLuma 2020 **does not** work for every game.

Also, keep in mind that not **every game** is available to play through Steam family sharing.

#### Credits to [@linkthehylian](https://github.com/linkthehylian) for this brief explanation

I **highly advise** you to use the "Legit stealth mode" checking the box "NoHook" on my program:
![alt text](https://i.imgur.com/xpAXU1b.png)

## Latest release: **[GreenLuma 2020 Manager v1.3.8.5](https://github.com/BlueAmulet/GreenLuma-2020-Manager/releases)**

## Features
  * Easily manage profiles for various games(good to circumvent the 168 id limit)
    * Add/Remove 1 or more games at once
    * Add/Remove profiles
  * Search for any game you want to add direct from the app
    * Search results are directly from SteamDB
    * Sort the results from Type(DLC, Game, etc..) or Name
  * Generate the Applist, close Steam and run GreenLuma 2020 in one click
    * You can choose any GL2020 parameters before launch
    * It will detect whether Steam is open or not and close it if necessary
  * All the profiles info are in JSON files so you can easily share with anyone
    * The profiles are saved on: C:\Users\YOUR_USER\AppData\Local\GLR_Manager\Profiles

![alt text](https://i.imgur.com/B8nDYm3.png)
  
## What's the difference between your app and [GreenLuma Reborn App](https://github.com/linkthehylian/GreenLuma-Reborn-App)?
  Well the main difference, like i said on the topic above, is that on my app you can search the game you want to add directly from the program and my version is more focused on the management of the folder (and if you're like me who don't like having all the games unlocked at the same time the profile system can help you alot)
  
## Future Plans
* **Work on the UI(I still suck at UI design)**
* **Add varius QoL stuff(Would love some ideas for this)**
* Add a way to load previous games on your AppList folder
* ~~Add a way to launch GL2020 direct from the app~~
* Add some user input validation
  
## Built With
* [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) - The GUI framework
* [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/index.html) - Used to make the standalone executable

## Authors
[**ImaniiTy**](https://github.com/ImaniiTy):

![alt text](https://i.imgur.com/zmS7oBs.gif)

[**BlueAmulet**](https://github.com/BlueAmulet): This fork