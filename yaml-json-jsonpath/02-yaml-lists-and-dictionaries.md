# YAML Lists and Dictionaries

## Overview

Two important structures in YAML are:

- Lists
- Dictionaries

These structures can also be combined to create more complex data.

When reading YAML, I should pay close attention to:

- `-` for list items
- `:` for key-value relationships
- indentation for parent-child relationships

---

# YAML Lists

A list represents a collection of items.

Example:

```yaml
Fruits:
  - Orange
  - Apple
  - Banana
```

`Fruits` is the key.

Its value is a list containing:

```text
Orange
Apple
Banana
```

The hyphen `-` identifies each item in the list.

---

## Identifying List Items

Consider:

```yaml
Vehicles:
  - Car
  - Bus
  - Truck
  - Bike
```

This does **not** contain five keys.

There is only one key:

```text
Vehicles
```

The values underneath it are list items:

```text
Car
Bus
Truck
Bike
```

The structure is:

```text
Vehicles
   ↓
  List
   ├── Car
   ├── Bus
   ├── Truck
   └── Bike
```

---

# YAML Dictionaries

A dictionary represents data using key-value pairs.

Example:

```yaml
Banana:
  Calories: 105
  Fat: 0.4
  Carbs: 27
```

`Banana` contains another dictionary.

That dictionary contains:

```text
Calories → 105
Fat      → 0.4
Carbs    → 27
```

The structure is:

```text
Banana
   ↓
Dictionary
   ├── Calories: 105
   ├── Fat: 0.4
   └── Carbs: 27
```

---

# Dictionary vs List

The difference can often be recognised by looking at the syntax.

## Dictionary

```yaml
Car:
  Color: Blue
  Model: Corvette
```

The nested values use key-value pairs:

```text
Color: Blue
Model: Corvette
```

Therefore, `Car` contains a dictionary.

---

## List

```yaml
Cars:
  - Corvette
  - BMW
  - Toyota
```

The values begin with `-`.

Therefore, `Cars` contains a list.

---

## Quick Comparison

Dictionary:

```yaml
Car:
  Color: Blue
  Model: Corvette
```

Structure:

```text
Car
 ↓
Dictionary
 ├── Color
 └── Model
```

List:

```yaml
Cars:
  - Corvette
  - BMW
  - Toyota
```

Structure:

```text
Cars
 ↓
List
 ├── Corvette
 ├── BMW
 └── Toyota
```

The important clue is the `-`.

---

# List of Dictionaries

A list can contain dictionaries.

Example:

```yaml
Fruits:
  - Banana:
      Calories: 105
      Fat: 0.4
      Carbs: 27

  - Grape:
      Calories: 62
      Fat: 0.3
      Carbs: 16
```

Here:

- `Fruits` is a key.
- `Fruits` contains a list.
- `Banana` is part of the first list item.
- `Grape` is part of the second list item.
- Each fruit contains another dictionary of nutritional information.

The structure can be visualised as:

```text
Fruits
  ↓
 List
  │
  ├── Banana
  │     ↓
  │   Dictionary
  │     ├── Calories: 105
  │     ├── Fat: 0.4
  │     └── Carbs: 27
  │
  └── Grape
        ↓
      Dictionary
        ├── Calories: 62
        ├── Fat: 0.3
        └── Carbs: 16
```

---

# A More Common List of Dictionaries

Another common structure is:

```yaml
Cars:
  - Color: Blue
    Model: Corvette

  - Color: Red
    Model: BMW
```

The first `-` starts the first dictionary:

```yaml
- Color: Blue
  Model: Corvette
```

The second `-` starts another dictionary:

```yaml
- Color: Red
  Model: BMW
```

Therefore:

```text
Cars
 ↓
List
 ├── Dictionary
 │     ├── Color: Blue
 │     └── Model: Corvette
 │
 └── Dictionary
       ├── Color: Red
       └── Model: BMW
```

---

# Lists Inside Dictionaries

A dictionary can contain a list as one of its values.

Example:

```yaml
Employee:
  Name: John
  Role: Developer
  Skills:
    - Linux
    - Docker
```

`Employee` contains a dictionary.

Inside that dictionary:

```text
Name   → simple value
Role   → simple value
Skills → list
```

The structure is:

```text
Employee
   ↓
Dictionary
   ├── Name: John
   ├── Role: Developer
   └── Skills
         ↓
        List
         ├── Linux
         └── Docker
```

---

# List of Dictionaries Containing Lists

These structures can be combined further.

Example:

```yaml
Employees:
  - Name: John
    Role: Developer
    Skills:
      - Linux
      - Docker

  - Name: Sarah
    Role: Engineer
    Skills:
      - Python
      - Kubernetes
```

Let's break this down one level at a time.

First:

```yaml
Employees:
```

`Employees` is a key.

Next:

```yaml
  - Name: John
```

The `-` tells us that the value of `Employees` is a list.

Each employee is represented by a dictionary.

For John:

```yaml
Name: John
Role: Developer
Skills:
```

These are keys inside John's dictionary.

Then:

```yaml
Skills:
  - Linux
  - Docker
```

`Skills` contains another list.

The complete structure is therefore:

```text
Dictionary
   ↓
Employees
   ↓
List
   │
   ├── Dictionary
   │     ├── Name: John
   │     ├── Role: Developer
   │     └── Skills
   │           ↓
   │          List
   │           ├── Linux
   │           └── Docker
   │
   └── Dictionary
         ├── Name: Sarah
         ├── Role: Engineer
         └── Skills
               ↓
              List
               ├── Python
               └── Kubernetes
```

---

# How I Identify the Structure

Instead of trying to understand the entire YAML document at once, I can read it one level at a time.

For example:

```yaml
Employees:
  - Name: John
    Skills:
      - Linux
      - Docker
```

Start with:

```text
Employees
```

Ask:

**What is the value of Employees?**

I see:

```text
-
```

Therefore:

```text
Employees → List
```

Then inspect the first item:

```yaml
Name: John
Skills:
```

These are key-value relationships.

Therefore:

```text
List item → Dictionary
```

Then inspect `Skills`:

```yaml
Skills:
  - Linux
  - Docker
```

Again I see `-`.

Therefore:

```text
Skills → List
```

The final structure is:

```text
Employees
    ↓
   List
    ↓
Dictionary
    ↓
Skills
    ↓
   List
```

---

# Useful Recognition Patterns

## Simple dictionary

```yaml
Person:
  Name: John
  Age: 28
```

Think:

```text
Dictionary inside dictionary
```

---

## Simple list

```yaml
Fruits:
  - Apple
  - Banana
```

Think:

```text
List inside dictionary
```

---

## List of dictionaries

```yaml
Employees:
  - Name: John
    Age: 28

  - Name: Sarah
    Age: 35
```

Think:

```text
List containing dictionaries
```

---

## Dictionary containing a list

```yaml
Employee:
  Name: John
  Skills:
    - Linux
    - Docker
```

Think:

```text
Dictionary containing a list
```

---

# Key Lesson

When analysing YAML, I should not identify the structure based only on the names of the values.

I should inspect the syntax.

```text
-  → list item

:  → key-value relationship

indentation → relationship between parent and child data
```

For example:

```yaml
Cars:
  - Corvette
  - BMW
```

means:

```text
Cars → List
```

while:

```yaml
Car:
  Color: Blue
  Model: Corvette
```

means:

```text
Car → Dictionary
```

and:

```yaml
Cars:
  - Color: Blue
    Model: Corvette
  - Color: Red
    Model: BMW
```

means:

```text
Cars → List → Dictionaries
```

Being able to identify these structures is important before moving on to JSON and JSONPath, where the same concepts of lists/arrays and dictionaries/objects appear in a different syntax.
