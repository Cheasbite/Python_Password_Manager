# Chease's Password Manager
A simple python password manager built using tkinter.

## Dependencies:
```bash
pip install cryptography
```

> [!Note]
> You may need to install extra dependencies depending on your python version. \n
> It is recommended that you have a python version >= 3.10

## Run the program
```bash
python3 main.py # Depends on where your path is but run it in main.py
```

## First run
You will be prompted to enter a master password afterward this password will be used to decrypt
your credentials in the next run.

> [!Important]
> You $\color{red}{MUST}$ remember your master password!
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


### Add Button & Edit Button

|Keybind|Function|
|----|----|
|Enter| Move to the next box|
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


### Setting Button

|Keybind|Function|
|----|----|
|Control + s|Save|


