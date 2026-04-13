# Linux basics
## WSL (Windows Subsystem for Linux)
- Special feature of Windows that allows the users to run Linux environment on a Windows machine, without the need of a separated virtual machine or dual booting.
- Available Linux distributions:
    - Ubuntu
    - Debian
    - Kayli
    - Fedora
- Links:
    - https://learn.microsoft.com/en-us/windows/wsl/about
    - https://learn.microsoft.com/en-us/windows/wsl/install
### Installation
- **Prerequisites**: Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11.
- **Installation**:
    - Open **PowerShell** in administrator rights.
    - Run the command to install wsl: `wsl --install`
    - Reboot the Windows machine.
    - To see all available Linux distributions: `wsl --list --online`
    - Install the needed distro: `wsl --install -d <DistroName>`
        - During the installation process a user and password must be created.
    - To enter into WSL, open a windows terminal and type `wsl`.
- **Recommendations**: 
    - Install `WSL` extension for VSC to be able to use Visual Studio Code in the WSL environment.
        - Link: https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode
    - Make sure WSL version 2 is running to be able to run docker. Use the command: `wsl.exe --list --verbose` to check the verison.
    - It is recommended the use of `Windows Terminal` to be able to work in both terminals (Linux and Windows) at the same time.
## File system structure
### Windows VS Linux
<table>
    <tr>
        <th>Windows</th>
        <th>Linux</th>
    </tr>
    <tr>
        <td>Windows uses hard drivers to allocate the files there in an specific structure</td>
        <td>Linux focuses on folders and files first and it has its own structure</td>
    </tr>
    <tr>
        <td>Windows focuses on drivers first and `C:/` will be the drive containing the OS files</td>
        <td>Hard divers can be attached to some defeminated folder.</td>
    </tr>
    <tr>
        <td>Root disk is `C:\`</td>
        <td>Root folder is located in `/` and the drive or drives are **mounted** there</td>
    </tr>
    <tr>
        <td>Separated drives can be added the will have another name from the alphabet like: `D:\`, `E:\`, etc</td>
        <td>Separated drives can added in another directory like: `/var`, `/opt`, etc</td>
    </tr>
    <tr>
        <td>Default user folder is located in the path <code>C:\Users\&#10216;USER-NAME&#10217;</code></td>
        <td>Default user folder is located in the path <code>/home/&#10216;USER-NAME&#10217;</code></td>
    </tr>
    <tr>
        <td>If a file doesn't have an extension i.e. ".txt", it is difficult for Windows to execute it. Here it is important to almost always have an extension for the files. </td>
        <td>By default all files are treated like txt files, even though there is not extension included in the file name.</td>
    </tr>
</table>

### Root folder structure
```bash
ls /
#Top-level directories associated with root directory
 |-bin/  -> Binaries are allocated (same as .exe files in windows)                         
 |-etc/  -> Stores System config files used to control system behavior
 |-opt/  -> Optional files needed or third-party software packages  installed separately.
 |-home/ -> Contains user home directories and serves as the default working
 |-tmp/  -> Used to allocate temporal files and folders which are deleted when the Linux machin is rebooted or after some periud of time.
 |-usr/  -> Contains user-related programs, utilities, and shared resources.
 |-var/  -> Stores variable data such as log files that change frequently during system operation.
 |-root/ -> User directory to allocate files while root user is loged in.

 #Some other directories in the Linux system
 |-boot/       -> Need files for Linux to boot, including kernel and boot loader configuration files
 |-dev/        -> Hard drives, solid drives, partitions
 |-lib         -> Contains shared libraries and kernel modules required for system programs to function.
 |-lost+found  -> Used to store recovered fragments of corrupted files after file system checks.
 |-media/      -> Contains subdirectories where removable media devices (USB and CDs) are mounted.
 |-mnt/        -> Provides temporary mount points for manually mounting file systems.
 |-proc/       -> A virtual file system that provides information about running processes and system status using process IDs (PIDs).
 |-run/        -> Stores volatile runtime data such as process IDs and system information.
 |-sbin        -> Contains essential system administration binary executables.
 |-srv/        -> Stores server-specific data related to services provided by the system.
 |-sys/        -> A virtual file system used to interact with and manage hardware devices and kernel information.
 
```
## BASH
- A shell is a text-based interface that lets you talk to your computer.
- To check bash version: `bash --version`
- Bash scripts files have the **.sh** extension.
- Bash file requires the line: `#!/bin/bash` or `#!/bin/sh` on top of the document.

Example:
```
#!/bin/bash

echo "This is a sample script"
```
- Before executing the file, fic the permissions with this command: `chmod -x <FILE_NAME>`
- Once the permissions are fixed, the script can be executed like this: `./<FILE_NAME>` or `sh <FILE_NAME>`

## Linux commands
<table>
    <tr>
        <th>Type</th>
        <th>Command</th>
        <th>Description</th>
    </tr>
    <tr>
        <td rowspan=2>Storage</td>
        <td><code>df -h</code></td>
        <td>Command to  see available space on each partition
        <br><code>-h</code> option used to show human readable values.</td>
    </tr>
    <tr>
        <td><code>lsblk -l</code></td>
        <td>Command to see available partitions and where those are mounted
        <br><code>-l</code> option used to list disks, partitions, mounted folders and sizes </td>
    </tr>
    <tr>
        <td rowspan=6>Files and directories</td>
        <td><code>ls -lah &#10216;PATH&#10217;</code> or <code>ll &#10216;PATH&#10217;</code></td>
        <td>Command to list all files and directories in some specific location. 
        <br><code>-a</code> option used to list all files including hidden ones.
        <br><code>-l</code> option used to show more info about the list like: permissions, size, last edition, etc.
        <br><code>-h</code> option used to transform the file's size to human readable value</td>
    </tr>
    <tr>
        <td><code>cd &#10216;PATH&#10217;</code></td>
        <td>Command to enter into some specific directory</td>
    </tr>
    <tr>
        <td><code>mkdir &#10216;FOLDER-NAME&#10217;</code></td>
        <td>Command create a folder</td>
    </tr>
    <tr>
        <td><code>touch &#10216;FILE_NAME&#10217;</code></td>
        <td>Command to create a file</td>
    </tr>
    <tr>
        <td><code>pwd</code></td>
        <td>Command to get current directory path from root "/"</td>
    </tr>
    <tr>
        <td><code>rm  &#10216;FOLDER-NAME or FILE-NAME&#10217;</code></td>
        <td>Command to remove an empty folder or file
        <br>Additional options: <br>(<b>BE CAREFULL WHEN THE OPTIONS BELOW ARE USED BECUASE ONCE THE FILE IS DELETED THERE IS NO WAY TO GET IT BACK</b>):
        <br><code>-r</code> Enable recursive mode to remove <b>ALL</b> inside a folder.
        <br><code>-f</code> Enable force mode to remove the file or files without any additional confirmation.</td>
    </tr>
    <tr>
        <td rowspan=5>Create/Edit files</td>
        <td><code>vi &#10216;FILE_NAME&#10217;</code></td>
        <td>Command to edit files</td>
    </tr>
    <tr>
        <td><code>vim &#10216;FILE_NAME&#10217;</code>
        <td>Command to list all files and directories in some specific location.
        <br> Basic commands to use it:
        <br>-<code>i</code> Command key to enter in insert mode.
        <br>-<code>ESC</code> Command key to enter in view mode.
        <br>-<code>r</code> Command key to replace one character by new one.
        <br>-<code>:w</code> Command to save the changes.
        <br>-<code>:q</code> Command to quit from vim.
        <br>-<code>:&#10216;PATTERM&#10217;</code> Command to search strings based on a word or regex.
        <br>-<code>Ctrl + c</code> Minimize VIM and go to CLI and to go back type <code>fg</code>.
        </td>
    </tr>
    <tr>
        <td><code>nano &#10216;FILE_NAME&#10217;</code></td>
        <td>Command to edit files</td>
    </tr>
    <tr>
        <td><code>&#10216;CLI_COMMAND&#10217; > &#10216;FILE_NAME&#10217;</code></td>
        <td>Command to bulk the command output in a file, this file will be created if it doesn't exists and if there was information there, it is overwritten by the ">" command</td>
    </tr>
    <tr>
        <td><code>&#10216;CLI_COMMAND&#10217; >> &#10216;FILE_NAME&#10217;</code></td>
        <td>Command to bulk the command output in a file, this file will be created if it doesn't exists and if there was information there, it is kept and the new information is added at the botton of the file</td>
    </tr>
    <tr>
        <td rowspan=5>See files content</td>
        <td><code>cat &#10216;FILE_NAME&#10217;</code></td>
        <td>Command to see file information</td>
    </tr>
    <tr>
        <td><code>more &#10216;FILE_NAME&#10217;</code></td>
        <td>Command to see file information </td>
    </tr>
    <tr>
        <td><code>less &#10216;FILE_NAME&#10217;</code></td>
        <td>Command to see file information</td>
    </tr>
    <tr>
        <td><code>head &#10216;FILE_NAME&#10217;</code></td>
        <td>Command to see file information, more exactly the top lines</td>
    </tr>
    <tr>
        <td><code>tail &#10216;FILE_NAME&#10217;</code></td>
        <td>Command to see file information, more exactly the bottom lines</td>
    </tr>
    <tr>
        <td>Search information in a file</td>
        <td><code>grep &#10216;PATTERN&#10217; &#10216;FILE_NAME&#10217;</code> or <code>cat &#10216;FILE_NAME&#10217; |grep &#10216;PATTERN&#10217;</code></td>
        <td>Command to search information in a file</td>
    </tr>
    <tr>
        <td rowspan=2>File permissions</td>
        <td><code>chmod &#10216;PERMISSION_KIND&#10217; &#10216;FILE_NAME&#10217;</code> or <code>cat &#10216;FILE_NAME&#10217; |grep &#10216;PATTERN&#10217;</code></td>
        <td>Command to change permissions files. 
        <br>-Conventions: <code>&minus;<code>=No access, <code>r<code>=read, <code>w<code>=write, <code>x<code>=execute (app or script)
        <br>-Parts:
        <br>-Part1 -> Kind
        <br>--<code><b>d</b>rwxr-xr-x</code> -> Directory
        <br>--<code><b>l</b>rwxrwxrwx</code> -> Simlink (Shortcut)
        <br>--<code><b>-</b>rwxrwxrwx</code> -> File
        <br>-Part2 -> Owner
        <br>--<code>d<b>rwx</b>r-xr-x</code> -> Directory
        <br>--<code>l<b>rwx</b>rwxrwx</code> -> Simlink (Shortcut)
        <br>--<code>-<b>rwx</b>rwxrwx</code> -> File
        <br>-Part2 -> Group
        <br>--<code>drwx<b>r-x</b>r-x</code> -> Directory
        <br>--<code>lrwx<b>rwx</b>rwx</code> -> Simlink (Shortcut)
        <br>--<code>-rwx<b>rwx</b>rwx</code> -> File
        <br>-Part3 -> other
        <br>--<code>drwxr-x<b>r-x</b></code> -> Directory
        <br>--<code>lrwxrwx<b>rwx</b></code> -> Simlink (Shortcut)
        <br>--<code>-rwxrwx<b>rwx</b></code> -> File
        Example:
        <code>
        <br>#Adding permissions
        <br>chmod o+w &#10216;FILE_NAME&#10217;
        <br>chmod g+w &#10216;FILE_NAME&#10217;
        <br>chmod u+w &#10216;FILE_NAME&#10217;
        <br>chmod o+x &#10216;FILE_NAME&#10217;
        <br>chmod +x &#10216;FILE_NAME&#10217; #to all groups
        <br>#Removing permissions
        <br>chmod o-w &#10216;FILE_NAME&#10217;
        <br>chmod g-w &#10216;FILE_NAME&#10217;
        <br>chmod u-w &#10216;FILE_NAME&#10217;
        <br>chmod o-x &#10216;FILE_NAME&#10217;
        <br>chmod -x &#10216;FILE_NAME&#10217; #to all groups</code>
        </td>
    </tr>
    <tr>
        <td><code>chown &#10216;USER&#10217;:&#10216;USER_GROUP&#10217; &#10216;FILE_NAME&#10217;</code> or <code>cat &#10216;FILE_NAME&#10217; |grep &#10216;PATTERN&#10217;</code></td>
        <td>Command to change user in files</td>
    </tr>
    <tr>
        <td rowspan=4>Install and upgrade applications</td>
        <td><code>sudo apt update</code></td>
        <td>Command to update an application and system</td>
    </tr>
    <tr>
        <td><code>sudo apt upgrade</code></td>
        <td>Command to upgrade an application and system</td>
    </tr>
    <tr>
        <td><code>sudo apt install &#10216;APP-NAME&#10217;</code></td>
        <td>Command to install an application</td>
    </tr>
    <tr>
        <td><code>sudo apt remove &#10216;APP-NAME&#10217;</code></td>
        <td>Command to remove an application</td>
    </tr>
</table>

## References
- https://www.geeksforgeeks.org/linux-unix/linux-directory-structure/