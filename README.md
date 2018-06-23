# JXMonitor

Python script for monitoring [ JXMiner ](https://github.com/duckzland/jxminer) via TUI.

![Alt text](docs/jxmonitor.png?raw=true "JXMonitor Screenshot")

## Requirement
- JXMiner installed and running


## Installation (Ubuntu)       
1. Install python dependencies via requirement.txt:
```bash
    sudo pip install -r requirement.txt  
```
    
3. Install the deb
```bash
    sudo dpkg -i python-monitor-VERSION.deb
```
    


## Usage

```bash
    jxmonitor -s|-h|-v
```

Valid options for the client :
```bash
    -s    Display the monitor in a single column
    -h    Prints this help message
    -v    Prints the jxmonitor version
```



## Authors

* **Jason Xie** - *Initial work* - [VicTheme.com](https://victheme.com)



## License

This project is licensed under the GNU General Public License - see the [LICENSE.md](LICENSE.md) file for details
