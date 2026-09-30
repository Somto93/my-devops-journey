# JSONPath Nested Data

## Overview

Real JSON data often contains multiple levels of objects and arrays.

To navigate nested JSON with JSONPath, I should not try to memorise the entire path.

Instead, I should:

```text
Start at the root
      ↓
Identify the next property
      ↓
Determine whether its value is an object or array
      ↓
Navigate to the next level
      ↓
Repeat until I reach the required value
```

---

# Nested Objects and Arrays

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

The structure is:

```text
Root
 ↓
Object
 ↓
cars
 ↓
Array
 ├── Object
 │    ├── model: Corvette
 │    └── color: Blue
 │
 └── Object
      ├── model: BMW
      └── color: Black
```

To retrieve BMW:

```text
$.cars[1].model
```

Breakdown:

```text
$          → root
.cars      → cars array
[1]        → second object
.model     → model property
```

Result:

```text
BMW
```

---

# Navigating Several Levels

Consider:

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

Before constructing a JSONPath, I can map the structure:

```text
Root
 ↓
company
 ↓
Object
 ↓
employees
 ↓
Array
 ├── Employee 0
 │    ├── name
 │    └── skills → Array
 │
 └── Employee 1
      ├── name
      └── skills → Array
```

---

# Retrieving Sarah's Name

Sarah is the second employee.

Because indexing starts at `0`:

```text
John  → index 0
Sarah → index 1
```

Therefore:

```text
$.company.employees[1].name
```

Breakdown:

```text
$                   → root
.company            → company object
.employees          → employees array
[1]                 → Sarah's object
.name               → name
```

Result:

```text
Sarah
```

---

# Navigating an Array Inside an Array Item

Each employee has a `skills` array.

For John:

```json
{
  "name": "John",
  "skills": [
    "Linux",
    "Docker"
  ]
}
```

The indexes are:

```text
skills[0] → Linux
skills[1] → Docker
```

To retrieve Docker:

```text
$.company.employees[0].skills[1]
```

Breakdown:

```text
$                   → root
.company            → company
.employees          → employees array
[0]                 → John
.skills             → John's skills array
[1]                 → Docker
```

Result:

```text
Docker
```

---

# Retrieving Kubernetes

Sarah is employee index `1`.

Her skills are:

```text
skills[0] → Python
skills[1] → Kubernetes
```

Therefore:

```text
$.company.employees[1].skills[1]
```

Result:

```text
Kubernetes
```

The navigation can be visualised as:

```text
$
↓
company
↓
employees
↓
[1]
↓
skills
↓
[1]
↓
Kubernetes
```

---

# Every Array Requires Its Own Index

This is an important lesson.

Consider:

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
      }
    ]
  }
}
```

There are two arrays involved:

```text
employees → Array
skills    → Array
```

Therefore, if I want one specific skill from one specific employee, both arrays need to be navigated.

Example:

```text
$.company.employees[0].skills[1]
```

Here:

```text
employees[0] → first employee
skills[1]    → second skill
```

---

# Objects Use Properties, Arrays Use Indexes

A useful rule is:

```text
Object → property name

Array → index
```

For:

```json
{
  "company": {
    "employees": [
      {
        "name": "John"
      }
    ]
  }
}
```

the navigation is:

```text
$             → root object
.company      → object property
.employees    → object property containing an array
[0]           → array index
.name         → object property
```

This produces:

```text
$.company.employees[0].name
```

---

# Building the Path Visually

Suppose I want `Docker` from:

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

I can first trace the route:

```text
Root
 ↓
company
 ↓
employees
 ↓
John
 ↓
skills
 ↓
Docker
```

Then translate each step into JSONPath syntax:

```text
Root        → $
company     → .company
employees   → .employees
John        → [0]
skills      → .skills
Docker      → [1]
```

Combine them:

```text
$.company.employees[0].skills[1]
```

---

# More Complex Nested Example

Consider:

```json
{
  "company": "TechCorp",
  "departments": [
    {
      "name": "DevOps",
      "employees": [
        {
          "name": "John",
          "salary": 75000
        },
        {
          "name": "Sarah",
          "salary": 90000
        }
      ]
    },
    {
      "name": "Security",
      "employees": [
        {
          "name": "Mike",
          "salary": 85000
        },
        {
          "name": "David",
          "salary": 95000
        }
      ]
    }
  ]
}
```

The structure is:

```text
Root
 ↓
Object
 ├── company: TechCorp
 │
 └── departments
       ↓
      Array
       │
       ├── [0] DevOps
       │      ↓
       │    employees
       │      ↓
       │     Array
       │      ├── [0] John
       │      └── [1] Sarah
       │
       └── [1] Security
              ↓
            employees
              ↓
             Array
              ├── [0] Mike
              └── [1] David
```

---

# Retrieving David Using Indexes

David is located in:

```text
Security → department index 1
David    → employee index 1
```

Therefore:

```text
$.departments[1].employees[1].name
```

Breakdown:

```text
$                    → root
.departments         → departments array
[1]                  → Security
.employees           → Security employees array
[1]                  → David
.name                → David's name
```

Result:

```text
David
```

---

# Retrieving Sarah's Salary

Sarah is in:

```text
DevOps → department index 0
Sarah  → employee index 1
```

Therefore:

```text
$.departments[0].employees[1].salary
```

Result:

```text
90000
```

---

# Index-Based Navigation

Indexes are useful when I know the exact position of an item.

For example:

```text
$.departments[1].employees[1].name
```

works because:

```text
departments[1] → Security
employees[1]   → David
```

However, indexes depend on the order of the array.

If the order changes, the same index may point to a different item.

This is one reason JSONPath filters are useful when I want to select an item based on one of its properties rather than its position.

Filters will be covered in the next section.

---

# Common Nested-Path Mistakes

## Mistake 1 — Missing a Closing Bracket

Incorrect:

```text
$.company.employees[0.skills[1]
```

Correct:

```text
$.company.employees[0].skills[1]
```

Every array index must have:

```text
[index]
```

including both:

```text
[
]
```

---

## Mistake 2 — Accessing the Property Before the Array Item

Given:

```json
[
  {
    "name": "John"
  },
  {
    "name": "Sarah"
  }
]
```

Incorrect reasoning:

```text
$.name[1]
```

The root is an array, so I must first select the array item:

```text
$[1].name
```

---

## Mistake 3 — Forgetting an Array Level

Given:

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
      }
    ]
  }
}
```

To reach Docker, I need to navigate both arrays:

```text
employees[0]
```

and:

```text
skills[1]
```

Therefore:

```text
$.company.employees[0].skills[1]
```

---

# A Reliable Method for Nested JSONPath

When a JSON structure becomes complicated, I can use this process.

## Step 1 — Find the root

Ask:

```text
Does the JSON begin with { or [ ?
```

---

## Step 2 — Identify the next level

If I am looking at an object:

```text
Use the property name.
```

If I am looking at an array:

```text
Use an index when selecting by position.
```

---

## Step 3 — Move One Level at a Time

Do not jump directly to the final value.

For example:

```text
$
```

then:

```text
$.company
```

then:

```text
$.company.employees
```

then:

```text
$.company.employees[0]
```

then:

```text
$.company.employees[0].skills
```

then:

```text
$.company.employees[0].skills[1]
```

---

## Step 4 — Verify Each Array Index

Remember:

```text
First item  → [0]
Second item → [1]
Third item  → [2]
```

---

## Step 5 — Read the Completed Path Backwards

For:

```text
$.departments[1].employees[1].name
```

I can verify:

```text
name
↑
employee index 1
↑
employees
↑
department index 1
↑
departments
↑
root
```

If each level exists in the JSON structure, the path makes sense.

---

# Key Takeaways

1. Nested JSONPath expressions should be built one level at a time.

2. Object properties are accessed by their property names.

3. Arrays are navigated using indexes when selecting by position.

4. Every array encountered may require its own index.

5. Array indexing begins at `0`.

6. The order of the JSON structure determines the order of the JSONPath.

7. A path such as:

```text
$.company.employees[1].skills[1]
```

is simply a sequence of navigation steps.

8. Index-based paths depend on the position of items in an array.

9. When position may change, filtering by a property can be more useful than relying on a fixed index.

The main troubleshooting principle remains:

```text
Inspect the structure first.

Then construct the JSONPath one level at a time.
```
