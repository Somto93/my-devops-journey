# YAML Fundamentals

## What is YAML?

YAML is used to represent data.

A YAML file represents information using a human-readable structure based on indentation, keys, values, lists, and dictionaries.

A simple YAML file might look like:

```yaml
Fruit: Apple
Vegetable: Carrot
Liquid: Water
Meat: Chicken
```

---

## Key-Value Pairs

One of the basic ways data is represented in YAML is with **key-value pairs**.

The general structure is:

```yaml
Key: Value
```

For example:

```yaml
Fruit: Apple
```

Here:

- `Fruit` is the key.
- `Apple` is the value.
- `:` separates the key from the value.

Another example:

```yaml
Name: John
Age: 28
Role: Developer
```

This contains three key-value pairs.

---

## YAML Lists

YAML can also represent a collection of items using a **list**.

For example:

```yaml
Fruits:
  - Orange
  - Apple
  - Banana
```

Here:

- `Fruits` is the key.
- The value of `Fruits` is a list.
- `Orange`, `Apple`, and `Banana` are items in the list.
- The `-` identifies each list item.

It is important not to confuse list items with keys.

In this example:

```yaml
Fruits:
  - Orange
  - Apple
  - Banana
```

there is **one key**:

```text
Fruits
```

and three list items:

```text
Orange
Apple
Banana
```

---

## Multiple Lists

A YAML document can contain multiple keys whose values are lists.

Example:

```yaml
Fruits:
  - Orange
  - Apple
  - Banana

Vegetables:
  - Carrot
  - Cauliflower
  - Tomato
```

The top-level keys are:

```text
Fruits
Vegetables
```

Each key contains a list.

The structure can be understood as:

```text
Fruits
 ├── Orange
 ├── Apple
 └── Banana

Vegetables
 ├── Carrot
 ├── Cauliflower
 └── Tomato
```

---

## YAML Dictionaries

A YAML key can contain another collection of key-value pairs.

For example:

```yaml
Banana:
  Calories: 105
  Fat: 0.4
  Carbs: 27
```

Here, `Banana` contains a dictionary.

Inside the `Banana` dictionary are three key-value pairs:

```text
Calories → 105
Fat      → 0.4
Carbs    → 27
```

The structure can be visualised as:

```text
Banana
 ├── Calories: 105
 ├── Fat: 0.4
 └── Carbs: 27
```

---

## Nested Dictionaries

Dictionaries can be placed inside other dictionaries.

For example:

```yaml
Car:
  Color: Blue
  Model: Corvette
```

`Car` is a key whose value is another dictionary.

The nested dictionary contains:

```text
Color → Blue
Model → Corvette
```

This can be thought of as:

```text
Dictionary
   ↓
Car
   ↓
Dictionary
   ├── Color: Blue
   └── Model: Corvette
```

---

## Lists Inside Dictionaries

A dictionary can also contain a list.

Example:

```yaml
Cars:
  - Corvette
  - BMW
  - Toyota
```

Here:

```text
Cars
  ↓
List
  ├── Corvette
  ├── BMW
  └── Toyota
```

`Cars` is a key whose value is a list.

---

## Lists of Dictionaries

A list can contain dictionaries rather than simple values.

For example:

```yaml
Cars:
  - Color: Blue
    Model: Corvette

  - Color: Red
    Model: BMW
```

Here:

- `Cars` is a key.
- The value of `Cars` is a list.
- Each list item is a dictionary.

The structure is:

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

The `-` is an important clue that we are looking at list items.

---

## More Complex YAML Structure

YAML structures can combine dictionaries and lists.

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

The structure is:

```text
Employees
    ↓
   List
    ↓
 ┌───────────────┐
 │               │
Dictionary    Dictionary
 │               │
 ├─ Name          ├─ Name
 ├─ Role          ├─ Role
 └─ Skills        └─ Skills
      ↓                ↓
     List              List
```

More specifically:

```text
Employees
├── Employee 1
│   ├── Name: John
│   ├── Role: Developer
│   └── Skills
│       ├── Linux
│       └── Docker
│
└── Employee 2
    ├── Name: Sarah
    ├── Role: Engineer
    └── Skills
        ├── Python
        └── Kubernetes
```

Therefore:

- `Employees` is a key whose value is a list.
- Each employee is represented by a dictionary.
- `Name` and `Role` are key-value pairs.
- `Skills` is a key whose value is another list.

---

## Recognising YAML Structures

When reading YAML, I can identify the structure by looking for a few important patterns.

### Key-value pair

```yaml
Name: John
```

Pattern:

```text
Key: Value
```

### Dictionary

```yaml
Person:
  Name: John
  Age: 28
```

Pattern:

```text
Key:
  Key: Value
  Key: Value
```

### List

```yaml
Skills:
  - Linux
  - Docker
```

Pattern:

```text
Key:
  - Item
  - Item
```

### List of dictionaries

```yaml
Employees:
  - Name: John
    Role: Developer

  - Name: Sarah
    Role: Engineer
```

Pattern:

```text
Key:
  - Key: Value
    Key: Value
  - Key: Value
    Key: Value
```

---

## Key Takeaways

When reading YAML, I should first identify:

1. The keys.
2. The values associated with those keys.
3. Whether a value is a simple value, list, or dictionary.
4. Whether lists contain simple values or dictionaries.
5. How the indentation shows the relationship between the data.

A useful mental model is:

```text
Key: Value
```

```text
Key:
  Dictionary
```

```text
Key:
  - List item
  - List item
```

or:

```text
Key:
  - Dictionary
  - Dictionary
```

Understanding these structures makes it easier to read more complex YAML configuration files.
