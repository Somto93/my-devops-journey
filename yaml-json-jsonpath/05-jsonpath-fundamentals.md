# JSONPath Fundamentals

## What is JSONPath?

JSONPath is used to navigate and select data from JSON structures.

Before writing a JSONPath expression, I should first understand whether the JSON contains:

- Objects
- Arrays
- Nested objects
- Nested arrays

A JSONPath is then built by moving through that structure one level at a time.

---

# The Root Element `$`

In JSONPath:

```text
$
```

represents the **root element**.

The root is the starting point of the JSON document.

For example:

```json
{
  "Color": "Blue",
  "Model": "Corvette"
}
```

The `$` represents the entire object:

```text
$
↓
{
  "Color": "Blue",
  "Model": "Corvette"
}
```

Every JSONPath expression begins from the root.

---

# Accessing an Object Property

Consider:

```json
{
  "Color": "Blue",
  "Model": "Corvette"
}
```

To retrieve the value of `Color`:

```text
$.Color
```

Result:

```text
Blue
```

To retrieve `Model`:

```text
$.Model
```

Result:

```text
Corvette
```

The path can be read from left to right:

```text
$        → root
.Model   → access the Model property
```

---

# Root-Level Arrays

The root of a JSON document does not always have to be an object.

It can be an array.

Example:

```json
[
  "car",
  "bus",
  "truck",
  "bike"
]
```

Because the root itself is the array, we can access its elements directly from `$`.

---

# Array Indexing

JSON array indexes start at `0`.

For:

```json
[
  "car",
  "bus",
  "truck",
  "bike"
]
```

the indexes are:

```text
0 → car
1 → bus
2 → truck
3 → bike
```

Therefore:

```text
$[0]
```

selects:

```text
car
```

And:

```text
$[1]
```

selects:

```text
bus
```

Similarly:

```text
$[2]
```

returns:

```text
truck
```

and:

```text
$[3]
```

returns:

```text
bike
```

---

# Understanding `$[0]`

Consider:

```json
[
  "car",
  "bus",
  "truck",
  "bike"
]
```

The expression:

```text
$[0]
```

can be read as:

```text
$     → start at the root
[0]   → select item at index 0
```

Result:

```text
car
```

---

# Root Object vs Root Array

This distinction is very important when constructing JSONPath expressions.

## Root Object

If the JSON starts with:

```json
{
  "employees": [
    {"name": "John"},
    {"name": "Sarah"}
  ]
}
```

the root is an object.

To access the employees array:

```text
$.employees
```

---

## Root Array

If the JSON starts with:

```json
[
  {"name": "John"},
  {"name": "Sarah"}
]
```

the root itself is an array.

Therefore, we do not write:

```text
$.employees
```

because there is no key called `employees`.

Instead:

```text
$[0]
```

selects the first object.

And:

```text
$[1]
```

selects the second object.

---

# Accessing a Property Inside an Array Item

Consider:

```json
[
  {"name": "John", "age": 28},
  {"name": "Sarah", "age": 35},
  {"name": "Mike", "age": 24}
]
```

To retrieve Sarah's name:

```text
$[1].name
```

Breakdown:

```text
$        → root array
[1]      → second item
.name    → name property
```

Result:

```text
Sarah
```

To retrieve Mike's age:

```text
$[2].age
```

Breakdown:

```text
$        → root array
[2]      → third item
.age     → age property
```

Result:

```text
24
```

---

# Accessing an Array Stored Under a Key

Consider:

```json
{
  "cars": [
    "Corvette",
    "BMW",
    "Toyota"
  ]
}
```

The root is an object.

The object contains a key called:

```text
cars
```

The value of `cars` is an array.

To retrieve the first car:

```text
$.cars[0]
```

Result:

```text
Corvette
```

To retrieve the second car:

```text
$.cars[1]
```

Result:

```text
BMW
```

The expression:

```text
$.cars[1]
```

can be read as:

```text
$        → root
.cars    → access cars
[1]      → select index 1
```

---

# Accessing Properties Inside Objects Stored in Arrays

Consider:

```json
{
  "cars": [
    {
      "model": "Corvette",
      "color": "Blue"
    },
    {
      "model": "BMW",
      "color": "Black"
    }
  ]
}
```

To retrieve the model of the second car:

```text
$.cars[1].model
```

Breakdown:

```text
$          → root
.cars      → cars array
[1]        → second car
.model     → model property
```

Result:

```text
BMW
```

To retrieve the color of the first car:

```text
$.cars[0].color
```

Result:

```text
Blue
```

---

# Building a JSONPath One Level at a Time

Instead of trying to write a complete path immediately, I can build it gradually.

Consider:

```json
{
  "cars": [
    {
      "model": "Corvette",
      "color": "Blue"
    },
    {
      "model": "BMW",
      "color": "Black"
    }
  ]
}
```

Suppose I want:

```text
BMW
```

First identify the root:

```text
$
```

Then identify the key:

```text
$.cars
```

`cars` is an array.

BMW is in the second object, which is index `1`:

```text
$.cars[1]
```

Then access the `model` property:

```text
$.cars[1].model
```

So the construction was:

```text
$
↓
$.cars
↓
$.cars[1]
↓
$.cars[1].model
```

This is a useful way to reason about JSONPath.

---

# Do Not Put an Extra Dot Before an Array Index

During practice, we considered a path similar to:

```text
$.cars.[1].model
```

In the notation used in these exercises, the array index belongs directly after the array property.

Use:

```text
$.cars[1].model
```

not:

```text
$.cars.[1].model
```

Think:

```text
cars → select index 1
```

Therefore:

```text
.cars[1]
```

---

# Nested Object Navigation

Consider:

```json
{
  "company": {
    "name": "TechCorp"
  }
}
```

To retrieve `TechCorp`:

```text
$.company.name
```

Breakdown:

```text
$          → root
.company   → company object
.name      → name property
```

Result:

```text
TechCorp
```

Each `.` moves to a property inside an object.

---

# Combining Objects and Arrays

Consider:

```json
{
  "company": {
    "employees": [
      {
        "name": "John"
      },
      {
        "name": "Sarah"
      }
    ]
  }
}
```

To retrieve Sarah:

```text
$.company.employees[1].name
```

Read it one level at a time:

```text
$
↓
company
↓
employees
↓
index 1
↓
name
```

Or:

```text
$                       → root
.company                → company object
.employees              → employees array
[1]                     → second employee
.name                   → employee's name
```

Result:

```text
Sarah
```

---

# Basic JSONPath Patterns

## Access a root property

```text
$.property
```

Example:

```text
$.Model
```

---

## Access an item in a root array

```text
$[index]
```

Example:

```text
$[0]
```

---

## Access an array stored under a property

```text
$.property[index]
```

Example:

```text
$.cars[1]
```

---

## Access a property of an array item

```text
$.property[index].property
```

Example:

```text
$.cars[1].model
```

---

## Access a property when the root itself is an array

```text
$[index].property
```

Example:

```text
$[2].age
```

---

# Common Mistakes

## Mistake 1 — Forgetting zero-based indexing

For:

```json
[
  "car",
  "bus",
  "truck"
]
```

the first element is:

```text
$[0]
```

not:

```text
$[1]
```

---

## Mistake 2 — Assuming the root has a key that does not exist

Given:

```json
[
  {"name": "John"},
  {"name": "Sarah"}
]
```

this is incorrect:

```text
$.employees[1].name
```

There is no `employees` key.

The root itself is the array.

Use:

```text
$[1].name
```

---

## Mistake 3 — Navigating in the wrong order

Given:

```json
[
  {"name": "John"},
  {"name": "Sarah"}
]
```

this is not the path we want:

```text
$.name[1]
```

The array must be indexed first:

```text
$[1].name
```

The structure determines the order of the JSONPath.

---

# A Useful Mental Model

When constructing JSONPath, I can ask:

```text
Where am I starting?
        ↓
       Root $
        ↓
What structure am I looking at?
        ↓
Object or Array?
        ↓
Object → access a property
        ↓
Array → select an index
        ↓
Repeat until I reach the value
```

For example:

```json
{
  "cars": [
    {"model": "Corvette"},
    {"model": "BMW"}
  ]
}
```

To reach BMW:

```text
Root
 ↓
cars
 ↓
Array
 ↓
index 1
 ↓
model
```

which becomes:

```text
$.cars[1].model
```

---

# Key Takeaways

1. `$` represents the root element.

2. `.` is used to access object properties in the notation used in these exercises.

3. `[index]` selects an item from an array.

4. Array indexing starts at `0`.

5. The root may be an object or an array.

6. If the root is an array, indexing can begin directly after `$`.

7. The JSON structure determines the order of the JSONPath.

8. I should build complex paths one level at a time.

The main principle is:

```text
Do not guess the JSONPath.

Read the JSON structure first, then follow that structure from the root to the value I want.
```
