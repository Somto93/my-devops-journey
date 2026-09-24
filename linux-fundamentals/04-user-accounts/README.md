# Linux User Accounts

This section documents my learning and practice with Linux user accounts, privileges, and switching between users.

## Understanding Linux Users

Linux is a multi-user operating system. Different users can have different permissions and access to files, directories, and system resources.

I learned that there is an important distinction between a regular user account and the root user.

## Checking the Current User

To see which user I am currently logged in as:

```bash
whoami
```

For example:

```text
somto
```

## The Root User

The `root` user is the administrative user in Linux and has extensive privileges over the system.

Because root has the ability to make system-wide changes, commands executed with root privileges need to be used carefully.

## Using sudo

`sudo` allows an authorised user to execute a command with elevated privileges.

For example:

```bash
sudo systemctl status my_app
```

I also used `sudo` when installing software:

```bash
sudo apt install package-name
```

This helped me understand why some commands work as a regular user while other administrative tasks require elevated privileges.

## Switching Users

The `su` command can be used to switch to another user account:

```bash
su username
```

To switch to the root user, where permitted:

```bash
su -
```

The `-` starts a login shell with the environment of the target user.

## Viewing User Information

The `/etc/passwd` file contains information about user accounts on the system.

I can view it using:

```bash
cat /etc/passwd
```

An entry contains information about a user account, including the username, user ID, group ID, home directory, and login shell.

## Creating a User

A user can be created using:

```bash
sudo useradd username
```

A password can then be assigned using:

```bash
sudo passwd username
```

## Deleting a User

A user account can be removed using:

```bash
sudo userdel username
```

## What I Learned

Working with Linux user accounts helped me understand that commands and processes operate under particular users and that permissions affect what those users are allowed to do.

I also learned the importance of using administrative privileges only when required rather than performing every task as the root user.
