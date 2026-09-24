# Linux Package Management

This section documents my learning and hands-on practice with Linux package management, particularly RPM and YUM.

## What is Package Management?

Package management allows software to be installed, queried, updated, and removed from a Linux system.

During my labs, I worked with RPM packages and learned how package managers help manage installed software.

## RPM

RPM stands for RPM Package Manager and is used to manage `.rpm` software packages on RPM-based Linux distributions.

### List Installed RPM Packages

```bash
rpm -qa
```

I learned that:

- `q` means query
- `a` means all

Therefore, `rpm -qa` queries all installed RPM packages.

## Query a Specific Package

```bash
rpm -q package-name
```

For example:

```bash
rpm -q ftp
```

This can be used to check whether a particular package is installed.

## Installing an RPM Package

During my KodeKloud lab, I installed an FTP package provided as an RPM file.

The package was located in `/opt`, so I used:

```bash
sudo rpm -i /opt/ftp-0.17-89.el9.x86_64.rpm
```

The `-i` option tells RPM to install the package.

An important thing I learned from this exercise is that when installing an RPM file directly, I need to provide the correct path to the `.rpm` file.

## Verifying the Installation

After installing the package, I verified it using:

```bash
rpm -qa | grep ftp
```

This combines two commands using a pipe (`|`).

`rpm -qa` lists installed RPM packages, while:

```bash
grep ftp
```

filters the output for entries containing `ftp`.

This was also useful practice in combining Linux commands.

## YUM

I also learned about YUM as a package management tool.

Unlike installing an individual RPM file directly, YUM can work with configured repositories and handle package dependencies.

A package can be installed using:

```bash
sudo yum install package-name
```

Packages can also be removed using:

```bash
sudo yum remove package-name
```

## RPM vs YUM

One of the important concepts I learned is the difference between working directly with an RPM package and using a package manager such as YUM.

With RPM, I can work directly with a `.rpm` package file:

```bash
sudo rpm -i package.rpm
```

With YUM, I can request a package by name from configured repositories:

```bash
sudo yum install package-name
```

YUM can also resolve dependencies required by the package.

## Troubleshooting Lesson

While practising package installation, I learned that command syntax and file paths matter.

For example, the RPM package file must be supplied as an argument to `rpm -i`:

```bash
sudo rpm -i /opt/ftp-0.17-89.el9.x86_64.rpm
```

This reinforced the importance of reading Linux command syntax carefully and understanding which part of a command is the command, which part is an option, and which part is the argument.

## What I Learned

This exercise helped me understand:

- How to query installed RPM packages
- How to install an RPM package from a file
- How to verify whether a package is installed
- How pipes can connect commands
- The basic difference between RPM and YUM
- The importance of paths and command syntax when installing software
