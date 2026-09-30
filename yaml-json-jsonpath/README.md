# YAML, JSON and JSONPath

This directory contains my notes and practical exercises for working with YAML, JSON, and JSONPath.

These formats and query techniques are commonly encountered when working with configuration files and structured data.

---

## Topics Covered

### YAML

- YAML key-value pairs
- Lists
- Dictionaries
- Nested dictionaries
- Lists of dictionaries
- YAML indentation
- Understanding YAML structure
- Identifying indentation problems

### JSON

- JSON objects
- JSON arrays
- Key-value pairs
- Nested JSON structures
- Objects inside arrays
- Arrays inside objects

### JSONPath

- Root element `$`
- Accessing object properties
- Array indexing
- Navigating nested JSON
- Wildcards `[*]`
- Filter expressions `[?(...)]`
- Filtering using properties
- Comparison operators

---

## YAML Example

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

In this example:

- `Employees` is a key.
- The value of `Employees` is a list.
- Each item in the list is a dictionary.
- `Skills` is another list inside each employee dictionary.

---

## JSON Example

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

JSON uses:

- `{}` for objects
- `[]` for arrays
- `:` between a key and its value
- `,` to separate properties or array elements

---

## JSONPath Example

Given:

```json
{
  "employees": [
    {"name": "John", "age": 28},
    {"name": "Sarah", "age": 35},
    {"name": "Mike", "age": 24}
  ]
}
```

Access the first employee:

```text
$.employees[0]
```

Access Sarah's name:

```text
$.employees[1].name
```

Return all employee names:

```text
$.employees[*].name
```

Return the names of employees younger than 30:

```text
$.employees[?(@.age < 30)].name
```

---

## Important JSONPath Symbols

| Symbol | Meaning |
|---|---|
| `$` | Root element |
| `.` | Access a property |
| `[0]` | Access an array item by index |
| `[*]` | Select all items in an array |
| `?()` | Apply a filter |
| `@` | Current item being evaluated |
| `==` | Equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

---

## Key Lessons

### YAML indentation matters

Incorrect indentation can change the structure and meaning of YAML.

A YAML file may still be syntactically valid even when incorrect indentation causes data to appear at the wrong level.

Therefore, when troubleshooting YAML:

1. Inspect the indentation.
2. Identify the parent key.
3. Determine whether the value should be a dictionary or list.
4. Parse the YAML when possible.
5. Verify that the resulting structure matches the intended structure.

### JSONPath depends on the data structure

Before writing a JSONPath query, inspect whether the root is an object or an array.

If the root is an object:

```json
{
  "employees": []
}
```

A path may begin with:

```text
$.employees
```

If the root itself is an array:

```json
[
  {"name": "John"},
  {"name": "Sarah"}
]
```

A path can begin directly with an index or filter:

```text
$[0].name
```

or:

```text
$[?(@.name == "Sarah")].name
```

---

## Practical Files

This directory also contains YAML and JSON files created while practising the concepts, including examples involving:

- Fruits
- Lists
- Nested dictionaries
- Broken YAML indentation
- Cars and vehicles
- JSON arrays and objects

These exercises are intended to reinforce how structured data is represented and how JSONPath can be used to navigate it.

---

## Troubleshooting Approach

When working with YAML, JSON, or JSONPath:

```text
Inspect the data
      ↓
Identify the structure
      ↓
Determine whether you are working with an object or array
      ↓
Build the path one level at a time
      ↓
Apply indexes, wildcards, or filters where required
      ↓
Test the result
      ↓
Verify that the returned data is what you expected
```

The goal is not simply to memorise syntax, but to understand the structure of the data and construct the correct path from that structure.
