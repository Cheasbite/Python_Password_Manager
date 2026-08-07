# Chease's Password Manager
A simple python password manager built using tkinter <br />
with the focus on using the keyboard only to navigate around the app.

## Dependencies:
```bash
pip install cryptography
```

> [!Note]
> You may need to install extra dependencies depending on your python version. <br />
> It is recommended that you have a python version >= 3.10

## Run the program
```bash
git clone https://github.com/Cheasbite/Python_Password_Manager.git
cd Python_Password_Manager
python3 main.py # Depends on where your path is but run it in main.py
```

## First run
    You will be prompted to enter a master password afterward this password will be used to decrypt
your credentials in the next run.

> [!Important]
> You $\color{red}{MUST}$ remember your master password! <br />
> You will be locked out and there is no way to change it!

## Keybinds
### Universal (Works no matter where you are in the app)
|Keybind|Function|
|----|----|
|Esc|Go below the app 1 level (without save)|
| TAB| Switch the focus window/widget|


### Main Menu

|Keybind|Function|
|----|----|
|a|Add Button|
|d|Delete Button|
|e|Edit Button|
|h| Hide/Show Button|
|s|Setting Button|
|Double Click| Copy the Service/Email/Password|

> [!Note]
> Double Click depends on what collums you click on!

#### Support some vim-like bindings:

|Keybind|Function|
|----|----|
|j| Move down the tree|
|k| Move up the tree|
|q| Quits the program|
|y| Yank the password|

> [!Tip]
> Arrow keys (Up and Down) can also be used to move around the tree <br />
> instead of J and K.

### Add Button & Edit Button

|Keybind|Function|
|----|----|
|Enter| Move to the next box|
|Control + e|Hide/Show password|
|Control + s|Save|
|Control + g|Generate password|

> [!Note]
> When entering the service, you can use the arrow button (Up or Down) to navigate some predefined options.

### Delete Button

|Keybind|Function|
|----|----|
|d|Mark for deletions|
|j| Move down the tree|
|k| Move up the tree|
|o|Move to the top/bottom most in Multi-select|
|J|Multi-select up|
|K|Multi-select down|
|Enter| Confirm or Refuses (Use Tab to switch)|
|Control + s| Save|

> [!Tip]
> You can also use the arrow key too for this.

### Setting Button

|Keybind|Function|
|----|----|
|Control + s|Save|

## Recommendations
    It is recommended that you use something that directly binds one of your key <br />
to run this automatically. On windows, you may use [AutoHotkey](https://www.autohotkey.com/) to achieve this <br />
by letting it run on startup.
    Don't forget to continuosly change the iterations overtime. You can change it in the <br />
codes/config.py in the section security section on this part:
```python
# Security
# Reference for the amount of iterations should be used:
# https://github.com/cudocharles/OWASP-CheatSheetSeries/blob/master/cheatsheets/Password_Storage_Cheat_Sheet.md#pbkdf2
ALLOW_LOWER_ITERATION = False   # If set to true, you can lower the PBKDF2HMAC_iterations (not recommended)
osUrandomSize = 16              # How many bytes should the os generate (chunk size is not recommended)
PBKDF2HMAC_Lenght = 32          # How long should the encryption length be
PBKDF2HMAC_iterations = 600000  # How many time should the encryption be hash
```
> [!Note]
> Your master will be fine after iteration changes, it will be the same regardless. <br />
> However, please do it when you are in the situation to be able to do so such as <br />
> having good % remaining on the battery, not in a performance bottleneck, etc.... <br />
> You may be locked out of your own app!

## Compatability
    It should be able to run on both Linux and Window (MacOS is not tested). <br />
However, I can't guarantee that it will work smoothly.

