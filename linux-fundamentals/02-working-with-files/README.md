# Working with Files and Directories

This section documents my practice working with files and directories from the Linux command line.

## Creating Files

I used `touch` to create empty files:

```bash
touch file1.txt
```

Multiple files can also be created at once:

```bash
touch file1.txt file2.txt file3.txt
```

## Creating Directories

I used `mkdir` to create directories:

```bash
mkdir test-directory
```

## Copying Files

The `cp` command is used to copy files.

```bash
cp file1.txt file2.txt
```

This creates a copy of `file1.txt` named `file2.txt`.

Files can also be copied to another directory:

```bash
cp file1.txt test-directory/
```

## Moving Files

The `mv` command can move a file to another directory:

```bash
mv file1.txt test-directory/
```

## Renaming Files

I learned that `mv` is also used to rename files:

```bash
mv old-name.txt new-name.txt
```

## Viewing File Contents

I used `cat` to display the contents of a file:

```bash
cat file1.txt
```

## Removing Files

Files can be removed using:

```bash
rm file1.txt
```

## Removing Directories

An empty directory can be removed using:

```bash
rmdir test-directory
```

A directory containing files can be removed recursively using:

```bash
rm -r test-directory
```

Because `rm -r` can remove an entire directory and its contents, I learned to use it carefully.

## Absolute and Relative Paths

I also learned that Linux commands can work with both absolute and relative paths.

An absolute path specifies the complete location:

```bash
/home/somto/test-directory/file1.txt
```

A relative path specifies a location relative to my current working directory:

```bash
test-directory/file1.txt
```

I can use:

```bash
pwd
```

to check my current location before performing file operations.

## What I Learned

Working with files from the command line helped me understand how Linux paths, files, and directories relate to each other.

I also learned that commands such as `cp`, `mv`, and `rm` can change the filesystem directly, so checking my current directory and command arguments before executing them is important.
