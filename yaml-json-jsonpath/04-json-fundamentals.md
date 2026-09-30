# JSON Fundamentals

## What is JSON?

JSON represents structured data using objects, arrays, keys, and values.

The concepts we learned with YAML also appear in JSON, but JSON uses different syntax.

For example, this YAML:

```yaml
Color: Blue
Model: Corvette
```

can be represented in JSON as:

```json
{
  "Color": "Blue",
  "Model": "Corvette"
}
```

---

## JSON Objects

A JSON object is enclosed in curly braces:

```text
{ }
```

Example:

```json
{
  "Color": "Blue",
  "Model": "Corvette"
}
```

This object contains two key-value pairs:

```text
Color → Blue
Model → Corvette
```

The general structure is:

```json
{
  "key": "value"
}
```

---

## Keys and Values

In:

```json
{
  "Color": "Blue"
}
```

`"Color"` is the key.

`"Blue"` is the value.

The colon `:` separates the key from its value:

```text
"Color" : "Blue"
    ↑     ↑
   key   value
```

---

## Separating Multiple Properties

When an object contains multiple properties, a comma separates them.

Example:

```json
{
  "Color": "Blue",
  "Model": "Corvette"
}
```

Notice:

```text
"Color": "Blue",
                 ↑
               comma
```

The comma tells us that another property follows.

---

# JSON Arrays

A JSON array represents a collection of values.

Arrays use square brackets:

```text
[ ]
```

For example:

```json
[
  "car",
  "bus",
  "truck",
  "bike"
]
```

This array contains four elements:

```text
car
bus
truck
bike
```

---

## Array Indexes

Items in an array can be identified by their position.

The first item is at index `0`.

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
Index 0 → car
Index 1 → bus
Index 2 → truck
Index 3 → bike
```

This is called **zero-based indexing**.

This becomes particularly important when working with JSONPath.

---

# Object vs Array

The opening character gives an immediate clue about the JSON structure.

An object begins with:

```text
{
```

An array begins with:

```text
[
```

For example:

```json
{
  "Color": "Blue",
  "Model": "Corvette"
}
```

is an object.

While:

```json
[
  "car",
  "bus",
  "truck",
  "bike"
]
```

is an array.

A useful recognition rule is:

```text
{ } → Object

[ ] → Array
```

---

# Arrays Inside Objects

A JSON object can contain an array.

Example:

```json
{
  "cars": [
    "Corvette",
    "BMW",
    "Toyota"
  ]
}
```

Here:

```text
Root
 ↓
Object
 ↓
cars
 ↓
Array
 ├── Corvette
 ├── BMW
 └── Toyota
```

`cars` is a key whose value is an array.

---

# Objects Inside Arrays

An array can also contain objects.

Example:

```json
[
  {
    "name": "John",
    "age": 28
  },
  {
    "name": "Sarah",
    "age": 35
  }
]
```

The root is an array.

Each item in the array is an object.

The structure is:

```text
Root
 ↓
Array
 ├── Object
 │    ├── name: John
 │    └── age: 28
 │
 └── Object
      ├── name: Sarah
      └── age: 35
```

---

# Array of Objects Inside an Object

A common JSON structure combines objects and arrays.

Example:

```json
{
  "employees": [
    {
      "name": "John",
      "age": 28
    },
    {
      "name": "Sarah",
      "age": 35
    }
  ]
}
```

Let's identify the structure one level at a time.

First:

```text
{
```

tells us that the root is an object.

Then:

```text
"employees":
```

is a key.

Its value starts with:

```text
[
```

so its value is an array.

Each element starts with:

```text
{
```

so each array element is an object.

Therefore:

```text
Root
 ↓
Object
 ↓
employees
 ↓
Array
 ├── Object
 │    ├── name
 │    └── age
 │
 └── Object
      ├── name
      └── age
```

---

# Nested JSON

JSON structures can contain several levels.

Example:

```json
{
  "company": {
    "employees": [
      {
        "name": "John",
        "skills": [
          "Linux",
          "Docker"
        ]
      },
      {
        "name": "Sarah",
        "skills": [
          "Python",
          "Kubernetes"
        ]
      }
    ]
  }
}
```

We can read this one level at a time:

```text
Root
 ↓
Object
 ↓
company
 ↓
Object
 ↓
employees
 ↓
Array
 ↓
Employee objects
 ↓
skills
 ↓
Array
```

More visually:

```text
company
  ↓
Object
  ↓
employees
  ↓
Array
  │
  ├── Object
  │    ├── name: John
  │    └── skills
  │          ↓
  │         Array
  │          ├── Linux
  │          └── Docker
  │
  └── Object
       ├── name: Sarah
       └── skills
             ↓
            Array
             ├── Python
             └── Kubernetes
```

Understanding this structure is important before trying to query it with JSONPath.

---

# YAML and JSON Structure Comparison

The same data can be represented using YAML or JSON.

## YAML

```yaml
Employees:
  - Name: John
    Role: Developer
  - Name: Sarah
    Role: Engineer
```

## JSON

```json
{
  "Employees": [
    {
      "Name": "John",
      "Role": "Developer"
    },
    {
      "Name": "Sarah",
      "Role": "Engineer"
    }
  ]
}
```

Although the syntax is different, the underlying structure is similar:

```text
Employees
    ↓
   List / Array
    ↓
Dictionaries / Objects
```

In the terminology we have used:

```text
YAML list       ↔ JSON array

YAML dictionary ↔ JSON object
```

---

# Important JSON Symbols

The main symbols we have worked with are:

| Symbol | Purpose |
|---|---|
| `{ }` | Object |
| `[ ]` | Array |
| `:` | Separates a key from its value |
| `,` | Separates properties or array elements |
| `" "` | Used around JSON strings |

For example:

```json
{
  "Color": "Blue",
  "Model": "Corvette"
}
```

contains:

```text
{ }  → object

:    → separates each key and value

,    → separates the properties

" "  → surrounds the strings
```

---

# Reading JSON Systematically

Instead of trying to understand a large JSON document all at once, I can inspect it one level at a time.

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

First ask:

```text
What is the root?
```

It begins with `{`, so:

```text
Root → Object
```

Next:

```text
What is inside the root?
```

There is a key called:

```text
cars
```

Its value begins with `[`, so:

```text
cars → Array
```

Next:

```text
What does the array contain?
```

Each item begins with `{`, so:

```text
Array → Objects
```

Each object then contains:

```text
model
color
```

Therefore:

```text
Root
 ↓
Object
 ↓
cars
 ↓
Array
 ↓
Objects
 ↓
model / color
```

This approach makes it easier to construct JSONPath queries later.

---

# Key Takeaways

1. JSON represents structured data.

2. `{ }` represents an object.

3. `[ ]` represents an array.

4. `:` separates a key from its value.

5. `,` separates properties or array elements.

6. Array indexing starts at `0`.

7. Arrays can contain objects.

8. Objects can contain arrays.

9. JSON can contain multiple levels of nested objects and arrays.

10. Before writing JSONPath, I should first understand the structure of the JSON.

A useful approach is:

```text
Look at the root
      ↓
Object or Array?
      ↓
Identify the key
      ↓
Inspect its value
      ↓
Object, Array, or simple value?
      ↓
Continue one level at a time
```

Once the structure is understood, navigating it with JSONPath becomes much easier.
