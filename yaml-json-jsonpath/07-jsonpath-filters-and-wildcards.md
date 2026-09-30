# JSONPath Filters and Wildcards

## Overview

JSONPath can do more than select data using fixed array indexes.

It can also:

- Select every item in an array using a wildcard.
- Filter array items based on a condition.
- Compare property values.
- Return a specific property from the matching items.

These techniques are useful when I do not know the exact array position of the data I want.

---

# Why Use Filters?

Consider:

```json
{
  "employees": [
    {"name": "John", "age": 28},
    {"name": "Sarah", "age": 35},
    {"name": "Mike", "age": 24}
  ]
}
```

If I know Sarah is at index `1`, I could use:

```text
$.employees[1].name
```

Result:

```text
Sarah
```

However, this depends on Sarah remaining at index `1`.

If the order changes, the same index could return another employee.

Instead, I can search based on a property:

```text
$.employees[?(@.name == "Sarah")].name
```

This selects the employee whose `name` is `Sarah`.

---

# Basic Filter Syntax

A filter follows this general pattern:

```text
[?(@.property operator value)]
```

For example:

```text
[?(@.age > 30)]
```

The main parts are:

```text
[?(                    → start filter

@                      → current item

.age                   → property of the current item

> 30                   → condition

)]                     → close filter
```

---

# The `@` Symbol

Inside a filter:

```text
@
```

represents the **current item being evaluated**.

Consider:

```json
{
  "employees": [
    {"name": "John", "age": 28},
    {"name": "Sarah", "age": 35},
    {"name": "Mike", "age": 24}
  ]
}
```

For:

```text
$.employees[?(@.age > 30)]
```

JSONPath evaluates each employee.

Conceptually:

```text
John
@.age → 28
28 > 30 → false

Sarah
@.age → 35
35 > 30 → true

Mike
@.age → 24
24 > 30 → false
```

Therefore, Sarah matches the condition.

---

# Filtering by a Number

To find employees older than 30:

```text
$.employees[?(@.age > 30)]
```

To return only their names:

```text
$.employees[?(@.age > 30)].name
```

Result:

```text
Sarah
```

---

# Less Than

To find employees younger than 30:

```text
$.employees[?(@.age < 30)].name
```

For our data:

```text
John  → 28 < 30 → true
Sarah → 35 < 30 → false
Mike  → 24 < 30 → true
```

Result:

```text
John
Mike
```

---

# Equality

To find an employee whose age is exactly `28`:

```text
$.employees[?(@.age == 28)]
```

To return the employee's name:

```text
$.employees[?(@.age == 28)].name
```

Result:

```text
John
```

---

# Filtering Strings

Filters can also compare string properties.

Example:

```text
$.employees[?(@.name == "Sarah")]
```

To return Sarah's age:

```text
$.employees[?(@.name == "Sarah")].age
```

Result:

```text
35
```

Notice that the string value is written as:

```text
"Sarah"
```

---

# Comparison Operators

The comparison operators we practised include:

| Operator | Meaning |
|---|---|
| `==` | Equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

Examples:

```text
@.age == 28
```

```text
@.age > 30
```

```text
@.age < 30
```

```text
@.age >= 30
```

```text
@.age <= 30
```

---

# Greater Than vs Greater Than or Equal To

This distinction is important.

Consider:

```json
{
  "cars": [
    {"model": "Corvette", "price": 85000},
    {"model": "BMW", "price": 70000},
    {"model": "Toyota", "price": 35000},
    {"model": "Mercedes", "price": 90000}
  ]
}
```

This:

```text
$.cars[?(@.price > 70000)].model
```

means:

```text
price must be greater than 70000
```

Matches:

```text
Corvette
Mercedes
```

BMW does not match because:

```text
70000 > 70000
```

is false.

---

## Greater Than or Equal To

This:

```text
$.cars[?(@.price >= 70000)].model
```

includes values exactly equal to `70000`.

Therefore, BMW would also match.

The same distinction applies to:

```text
<
```

and:

```text
<=
```

---

# Less Than or Equal To

To return models costing `70000` or less:

```text
$.cars[?(@.price <= 70000)].model
```

Matches:

```text
BMW
Toyota
```

If I wrote:

```text
$.cars[?(@.price < 70000)].model
```

BMW would not match because its price is exactly `70000`.

---

# Root-Level Array Filters

A filter does not always follow a named property.

Sometimes the root itself is an array.

Consider:

```json
[
  {"name": "John", "age": 28},
  {"name": "Sarah", "age": 35},
  {"name": "Mike", "age": 24}
]
```

There is no `employees` key.

Therefore, to find everyone younger than 30:

```text
$[?(@.age < 30)].name
```

Result:

```text
John
Mike
```

---

# Root Array vs Named Array

Compare these two structures.

## Named Array

```json
{
  "employees": [
    {"name": "John", "age": 28},
    {"name": "Sarah", "age": 35}
  ]
}
```

Filter:

```text
$.employees[?(@.age >= 30)].name
```

---

## Root Array

```json
[
  {"name": "John", "age": 28},
  {"name": "Sarah", "age": 35}
]
```

Filter:

```text
$[?(@.age >= 30)].name
```

The difference exists because the second JSON document does not contain an `employees` key.

---

# Do Not Add an Unnecessary Wildcard Before a Filter

For a root-level array:

```json
[
  {"name": "John", "age": 28},
  {"name": "Sarah", "age": 35},
  {"name": "Mike", "age": 24}
]
```

To filter the root array directly, use:

```text
$[?(@.age < 30)].name
```

In the notation used in these exercises, I do not need to first write:

```text
$[*]
```

The filter itself evaluates the items in the array.

---

# Wildcards

The wildcard:

```text
*
```

means to select all items at that level.

When used with an array:

```text
[*]
```

means:

```text
select every item in the array
```

---

# Selecting All Array Items

Consider:

```json
{
  "cars": [
    {"model": "Corvette", "price": 85000},
    {"model": "BMW", "price": 70000},
    {"model": "Toyota", "price": 35000}
  ]
}
```

To select all cars:

```text
$.cars[*]
```

To return all model names:

```text
$.cars[*].model
```

Result:

```text
Corvette
BMW
Toyota
```

---

# Selecting All Values of a Property

To return all car prices:

```text
$.cars[*].price
```

Result:

```text
85000
70000
35000
```

The path can be read as:

```text
$          → root
.cars      → cars array
[*]        → every car
.price     → price of each car
```

---

# Wildcards with Nested Arrays

Consider:

```json
{
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
```

To access each employee's `skills` property:

```text
$.employees[*].skills
```

Conceptually, this selects the skills lists for all employees.

To select all the individual skills in the notation we practised:

```text
$.employees[*].skills[*]
```

This means:

```text
$                  → root
.employees         → employees array
[*]                → every employee
.skills            → each employee's skills array
[*]                → every skill
```

The individual skills are:

```text
Linux
Docker
Python
Kubernetes
```

---

# Selecting the Same Array Position from Every Item

The wildcard and an index can also be combined.

To return the first skill of every employee:

```text
$.employees[*].skills[0]
```

Result:

```text
Linux
Python
```

To return the second skill:

```text
$.employees[*].skills[1]
```

Result:

```text
Docker
Kubernetes
```

Here:

```text
[*]
```

means every employee, while:

```text
[1]
```

means the second skill for each employee.

---

# Combining Filters with Nested Data

Consider:

```json
{
  "company": "TechCorp",
  "departments": [
    {
      "name": "DevOps",
      "employees": [
        {"name": "John", "salary": 75000},
        {"name": "Sarah", "salary": 90000}
      ]
    },
    {
      "name": "Security",
      "employees": [
        {"name": "Mike", "salary": 85000},
        {"name": "David", "salary": 95000}
      ]
    }
  ]
}
```

We can combine navigation with filtering.

---

# Filter Employees Inside a Specific Department

If I already know that Security is at index `1`, I can navigate there first:

```text
$.departments[1].employees
```

Then filter the employees:

```text
$.departments[1].employees[?(@.salary > 85000)]
```

Then retrieve their names:

```text
$.departments[1].employees[?(@.salary > 85000)].name
```

For Security:

```text
Mike  → 85000 > 85000 → false
David → 95000 > 85000 → true
```

Result:

```text
David
```

---

# Filtering with `>=`

For DevOps:

```text
$.departments[0].employees[?(@.salary >= 90000)].name
```

DevOps contains:

```text
John  → 75000 >= 90000 → false
Sarah → 90000 >= 90000 → true
```

Result:

```text
Sarah
```

This demonstrates why the difference between:

```text
>
```

and:

```text
>=
```

matters.

---

# Filtering the Department Instead of Using Its Index

Indexes depend on position.

Instead of:

```text
$.departments[1]
```

I can select the department based on its name:

```text
$.departments[?(@.name == "Security")]
```

Then navigate to its employees:

```text
$.departments[?(@.name == "Security")].employees
```

To return every employee name in the selected department:

```text
$.departments[?(@.name == "Security")].employees[*].name
```

Result:

```text
Mike
David
```

This combines:

```text
filter
  +
nested navigation
  +
wildcard
  +
property selection
```

---

# Understanding the Combined Expression

Consider:

```text
$.departments[?(@.name == "Security")].employees[*].name
```

Break it down:

```text
$                                      → root

.departments                           → departments array

[?(@.name == "Security")]              → find Security

.employees                             → its employees array

[*]                                    → every employee

.name                                  → each employee's name
```

This is easier to understand when read one section at a time.

---

# Common Filter Syntax Mistakes

## Mistake 1 — Forgetting the Dot After `@`

Incorrect:

```text
[?(@salary > 85000)]
```

Correct:

```text
[?(@.salary > 85000)]
```

The property is accessed from the current item using:

```text
@.salary
```

---

## Mistake 2 — Not Closing the Filter Correctly

A filter beginning with:

```text
[?(
```

needs to close with:

```text
)]
```

Correct:

```text
[?(@.salary > 85000)]
```

A useful pattern to remember is:

```text
[?(@.property operator value)]
```

---

## Mistake 3 — Using `<` When `<=` Is Required

If the requirement says:

```text
70000 or less
```

then:

```text
< 70000
```

is not enough.

Use:

```text
<= 70000
```

Similarly:

```text
90000 or more
```

requires:

```text
>= 90000
```

---

## Mistake 4 — Filtering the Wrong Level

A filter must be applied to the array containing the items I want to evaluate.

For:

```json
{
  "employees": [
    {"name": "John", "age": 28},
    {"name": "Sarah", "age": 35}
  ]
}
```

I want to evaluate each item inside:

```text
employees
```

Therefore:

```text
$.employees[?(@.age > 30)]
```

The structure tells me where the filter belongs.

---

# Index vs Wildcard vs Filter

These three concepts solve different problems.

## Index

Use an index when I want an item at a specific position:

```text
$.employees[0]
```

Meaning:

```text
Give me the first employee.
```

---

## Wildcard

Use a wildcard when I want every item:

```text
$.employees[*]
```

Meaning:

```text
Give me every employee.
```

---

## Filter

Use a filter when I want items matching a condition:

```text
$.employees[?(@.age < 30)]
```

Meaning:

```text
Give me employees whose age is below 30.
```

A useful comparison is:

```text
[index]     → specific position

[*]         → every item

[?(...)]    → items matching a condition
```

---

# Choosing the Correct Technique

Before writing the JSONPath, ask what the requirement actually says.

If it says:

```text
the second employee
```

think:

```text
index
```

If it says:

```text
all employees
```

think:

```text
wildcard
```

If it says:

```text
employees younger than 30
```

think:

```text
filter
```

If it says:

```text
the employee named Mike
```

think:

```text
filter based on name
```

---

# JSONPath Implementations

One practical lesson from our exercises is that JSONPath tools can differ in the exact syntax or features they support.

For example, a JSONPath expression supported by one implementation may not necessarily behave identically in another tool.

Therefore, when working in a specific environment such as a lab, I should:

```text
Understand the intended JSONPath
        ↓
Use the syntax supported by the tool
        ↓
Test the expression
        ↓
Inspect the output
```

I should not assume that every JSONPath implementation supports every possible expression in exactly the same way.

---

# Key Takeaways

1. `[*]` selects every item in an array.

2. `[?(...)]` filters items based on a condition.

3. `@` represents the current item being evaluated inside a filter.

4. `@.property` accesses a property of the current item.

5. `==` checks equality.

6. `>` and `<` perform greater-than and less-than comparisons.

7. `>=` and `<=` include the boundary value.

8. Filters can be used on named arrays or directly on a root-level array.

9. Wildcards can be used at multiple levels of nested arrays.

10. Filters can be combined with nested navigation and wildcards.

11. Fixed indexes depend on array order, while filters can select items based on their properties.

12. JSONPath implementations may differ, so expressions should be tested in the actual tool being used.

A useful decision process is:

```text
Inspect the JSON
      ↓
Find the array containing the target data
      ↓
Do I need one position, every item, or matching items?
      ↓
Index        Wildcard        Filter
[index]        [*]          [?(...)]
      ↓
Navigate to the required property
      ↓
Test
      ↓
Verify the output
```
