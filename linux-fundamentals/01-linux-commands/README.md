# Linux Commands

This section documents the basic Linux commands I practised while learning Linux fundamentals for DevOps.

## Navigating the Linux File System

### Print Working Directory

```bash
pwd
```

Displays the path of the directory I am currently working in.

### List Files and Directories

```bash
ls
```

Lists files and directories in the current directory.

I also practised:

```bash
ls -l
ls -la
```

`ls -l` displays additional information about files, while `ls -la` also includes hidden files.

### Change Directory

```bash
cd /path/to/directory
```

Moves from the current directory to another directory.

For example:

```bash
cd /home/somto
```

To return to my home directory:

```bash
cd ~
```

## Creating Directories

```bash
mkdir test-directory
```

Creates a new directory.

## Creating Files

```bash
touch test-file.txt
```

Creates an empty file if the file does not already exist.

## Viewing File Contents

```bash
cat test-file.txt
```

Displays the contents of a file in the terminal.

## Copying Files

```bash
cp source.txt destination.txt
```

Copies a file from one location or filename to another.

## Moving and Renaming Files

```bash
mv old-name.txt new-name.txt
```

`mv` can be used to move a file or rename it.
## Removing Files

```bash
rm test-file.txt
```

Removes a file.

## Removing Directories

```bash
rmdir test-directory
```

Removes an empty directory.

For directories containing files:

```bash
rm -r directory-name
```

The `-r` option recursively removes the directory and its contents, so I need to use this command carefully.

## What I Learned

Practising these commands helped me become more comfortable navigating the Linux filesystem and performing basic file and directory operations from the command line.

These commands also form the foundation for many of the Linux administration and DevOps tasks I am learning.
