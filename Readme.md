# Chease's Python Password Manager
This is a past time project that I created to self-manage all the passwords that I used across all different sites. The codes are messy since I used Copilot's code and built on top of it and I will try to improve it as time continues but for now it works as intended.

## How to use
- This password manager stores all your password in a json file and later encrypts them after you close the program.
- They are all stored inside the storage/ folders initially having passwords.json in it. (If you decide to delete all the previous passwords and want to restart, delete all files inside of storage and create a passwords.json file that contains {} inside of it.)
- Once you created your master password initially, **YOU MUST REMEMBER THAT PASSWORD** else all your passwords will be loss as that password is the encryption key (I recommend to save it somewhere). Afterward, you must enter that master password each time you access the application (I recommend you use [AutoHotkeys](https://github.com/AutoHotkey/AutoHotkey) to set a custom keybind to automatically run this script).
- Inside the application there are 4 buttons on the top. Add password which adds password. Delete password which deletes password that you selected in the tree and pressing the Enter key. Show password which shows shows the password in the main tree. Refresh which refreshes the tree.
- If you want to change the window sizes or fonts, you can change it inside the config file (Will add more later) else feel free to change the code and its behaviour however you like.

## Warning
If you want to edit the code, ensure that you have grasped how the code work. If you got stuck and broke the code, you can clone this project again then delete the passwords.json and replace it with your previous salt.bin and passwords.enc file in the storage folder. However, this does not guarantee that it will fix all your problems.

## Shortcuts (Windows key only)
### Adding Passwords
- [Control + s] to save
- [Enter] to move to the next input field
- [Control + g] to generate a random password
- [Control + e] to hide or show password
- [Esc] to exit
### Deleting Passwords
- [Control + s] to save
- [Enter] to delete the selected highlight row
- [Esc] to exit
### Main Window
- [Double click] or [Control + c] to copy the selected row password
- [Control + r] to refresh the tree
- [Control + a] to add a password
- [Control + x] to delete a password
- [Control + e] to show or hide password

## Instructions
### **Requirements**
You need to have these python packages installed. (For python versions >= 3.6)
```bash
    pip install cryptography
    pip install pyperclip
```
### **Clone the repo**
```bash
    git clone https://github.com/Cheasbite/Python_Password_Manager.git
```

Then go to main.py and run it

## **Acknowledgements**
Since this is a side project that I made for saving my passwords and was already sastified with what I made. Changes are minimal and slow. So if you are not sastified with it, clone it or forked it and built on top of it. The codes are really messy right now and I will change them to be much cleaner than this.
