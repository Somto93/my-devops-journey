# VI Editor

This section documents my practice using the VI text editor in Linux.

VI is a command-line text editor that allows me to create and modify files directly from the terminal.

## Opening a File

```bash
vi filename.txt
```

If the file exists, VI opens it. If it does not exist, I can create it by saving the file after editing.

## VI Modes

One of the important concepts I learned is that VI operates using different modes.

### Command Mode

VI starts in command mode.

In this mode, I can navigate through the file and perform actions such as deleting, copying, pasting, searching, saving, and quitting.

I can press:

```text
Esc
```

to return to command mode.

### Insert Mode

Insert mode allows me to enter and edit text.

From command mode, I can press:

```text
i
```

to enter insert mode.

After editing, I press `Esc` to return to command mode.

## Navigation

In command mode, I can use:

```text
h    Move left
j    Move down
k    Move up
l    Move right
```

## Deleting Text

To delete a character:

```text
x
```

To delete an entire line:

```text
dd
```

## Copying and Pasting

To copy a line:

```text
yy
```

To paste the copied line:

```text
p
```

## Searching

To search for text within a file:

```text
/search-term
```

Press `Enter` to perform the search.

I can use:

```text
n
```

to move to the next matching result.

## Saving and Exiting

To save changes:

```text
:w
```

To quit:

```text
:q
```

To save and quit:

```text
:wq
```

To quit without saving changes:

```text
:q!
```

## What I Learned

The most important concept for me was understanding the difference between command mode and insert mode.

When I want to type or modify text, I enter insert mode. When I want to perform VI commands such as saving, deleting, copying, searching, or exiting, I return to command mode.

Practising VI is useful because Linux servers are often managed through the command line, where a terminal-based text editor can be used to modify configuration and other text files.
