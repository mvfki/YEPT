# YEPT - YEast Primer Tool

## Usage
### Packaged GUI Application
For MS Windows users, download the executable [here](https://github.com/mvfki/YEPT/releases/download/YEPT_2.0/YEPT_2.0_win.exe).  
For MacOSX users, please wait for some days...  
### Run from Development Level
For users from ANY operation system. The application can be run from the source code.  
First clone this repository.
```
git clone https://github.com/mvfki/YEPT.git
cd YEPT
```
There is no installation need. The visible window interface can be invoked by:
```
python main.py
```

## Updates
### 2.0 - Update  

#### For User  
1. Largely reduced volume of the application
2. Changed online BLAST to local BLAST, so that it is fast now
3. Added the support for searching with systematic ID for S. pombe.  
4. Added the support for searching with ambiguous query text. (e.g. Search "S. pombe" data for "cdc")  

#### For Developer  
1. Reconstructed the structure of the GUI script, making things more maintainable.  
2. Changed the way of storing the genomes, which is better for importing the data.  
3. Utilized SQLite3 library for storing annotations, which made things clean.  
4. Windows executable packaging method see:  

> Run "Command Prompt" (CMD for later) as **administrator**

First jump to the proper working directory. By default CMD start with `C:\WINDOWS\system32>`. If you put this direcory, where everything about YEPT is placed, at another volume, say "D:", then just type `D:` and press `<enter>`. Then go to the address, which can be found when you right click any file here and go to its property, by:  
```
>cd DIRECTORY\WHERE\YOU\SEE\THIS
```
Then we'd better prepare a clean environment, otherwise the tool who do the packaging job would wrap up many things useless. 
```
>conda create -n yept_dev biopython
>activate yept_dev
>pip install pyinstaller
### Optional, to check whether all dependencies are done ###
>python __main__.py
```
Finally, we pack it with pre-tested script. 
```
>pyinstaller YEPT_win.spec
```

5. TODOs. (sorted by priority)
- Support more types of alias. For example, a case when gene symbol is "new10" but protein product is called "erh1", where the latter is actually more popular and meaningful.  
- MacOSX version.  
- Maybe better arrangement of the core calculation functions
