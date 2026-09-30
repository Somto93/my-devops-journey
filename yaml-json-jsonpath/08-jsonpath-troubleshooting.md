# JSONPath Troubleshooting

## Overview

When a JSONPath expression does not return the expected result, I should avoid randomly changing the query.

A better troubleshooting process is:

```text
Inspect the JSON
      ↓
Identify the root structure
      ↓
Trace the path one level at a time
      ↓
Check indexes, properties, wildcards, or filters
      ↓
Check syntax
      ↓
Test the expression
      ↓
Compare actual output with expected output
```

The goal is to identify which part of the path is incorrect.

---

# 1. Inspect the JSON Before Writing the Path

Before constructing JSONPath, first inspect the data.

For example:

```json
{
  "employees": [
    {"name": "John", "age": 28},
    {"name": "Sarah", "age": 35}
  ]
}
```

The structure is:

```text
Root
 ↓
Object
 ↓
employees
 ↓
Array
 ↓
Objects
```

Therefore, a path can begin with:

```text
$.employees
```

However, consider:

```json
[
  {"name": "John", "age": 28},
  {"name": "Sarah", "age": 35}
]
```

Now the structure is:

```text
Root
 ↓
Array
 ↓
Objects
```

There is no `employees` property.

Therefore, the path must begin directly from the root array:

```text
$[0]
```

or with a filter such as:

```text
$[?(@.age > 30)]
```

---

# 2. Check Whether the Root Is an Object or Array

This is one of the first things to check.

```text
{ } → Object

[ ] → Array
```

If the root is:

```json
{
  "cars": []
}
```

I can navigate using:

```text
$.cars
```

If the root is:

```json
[
  "car",
  "bus"
]
```

I can navigate directly using:

```text
$[0]
```

A common mistake is inventing a property that does not exist.

---

# 3. Remember Zero-Based Indexing

Array indexes begin at `0`.

For:

```json
[
  "car",
  "bus",
  "truck",
  "bike"
]
```

the positions are:

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

returns:

```text
car
```

and:

```text
$[3]
```

returns:

```text
bike
```

If I accidentally think the first item is index `1`, every subsequent selection may be incorrect.

---

# 4. Follow the Structure in the Correct Order

Consider:

```json
[
  {"name": "John"},
  {"name": "Sarah"}
]
```

Suppose I want Sarah's name.

Incorrect:

```text
$.name[1]
```

This tries to access `name` before selecting an object from the array.

Correct:

```text
$[1].name
```

The actual structure is:

```text
Root array
    ↓
Index 1
    ↓
Object
    ↓
name
```

Therefore, the JSONPath must follow that same order.

---

# 5. Check Every Opening and Closing Bracket

JSONPath expressions can fail because of a missing bracket.

For example:

```text
$.company.employees[0.skills[1]
```

is missing the closing bracket after `0`.

Correct:

```text
$.company.employees[0].skills[1]
```

Whenever I use:

```text
[
```

I should check that the corresponding:

```text
]
```

exists.

---

# 6. Check Filter Parentheses and Brackets

A filter follows the pattern:

```text
[?(@.property operator value)]
```

Notice how it begins:

```text
[?(
```

and ends:

```text
)]
```

For example:

```text
[?(@.age > 30)]
```

During practice, a query similar to this was written:

```text
$.departments[1].employees[?(@salary > 85000].name
```

There were two syntax problems.

First:

```text
@salary
```

should be:

```text
@.salary
```

Second, the filter needed to close with:

```text
)]
```

The corrected path was:

```text
$.departments[1].employees[?(@.salary > 85000)].name
```

---

# 7. Remember the Dot After `@`

Inside a filter:

```text
@
```

represents the current item.

To access one of its properties, use:

```text
@.property
```

For example:

```text
@.age
```

```text
@.name
```

```text
@.salary
```

Therefore:

```text
[?(@.salary > 85000)]
```

is the pattern we practised.

---

# 8. Check the Comparison Operator

Sometimes the path is correct but the comparison operator does not match the requirement.

Suppose the requirement says:

```text
price of 70000 or less
```

This:

```text
@.price < 70000
```

does not include `70000`.

The correct condition is:

```text
@.price <= 70000
```

Similarly:

```text
salary of 90000 or more
```

requires:

```text
@.salary >= 90000
```

not:

```text
@.salary > 90000
```

The operators are:

```text
==  → equal to
>   → greater than
<   → less than
>=  → greater than or equal to
<=  → less than or equal to
```

---

# 9. Index, Wildcard, or Filter?

When troubleshooting, check whether I chose the correct selection method.

## Index

Use when selecting by position:

```text
$.employees[1]
```

Meaning:

```text
second employee
```

---

## Wildcard

Use when selecting every item:

```text
$.employees[*]
```

Meaning:

```text
all employees
```

---

## Filter

Use when selecting based on a condition:

```text
$.employees[?(@.age < 30)]
```

Meaning:

```text
employees whose age is less than 30
```

A useful decision rule is:

```text
Specific position?
      ↓
    [index]

Every item?
      ↓
      [*]

Items matching a condition?
      ↓
    [?(...)]
```

---

# 10. Do Not Add an Unnecessary Wildcard Before a Filter

Consider the root-level array:

```json
[
  {"name": "John", "age": 28},
  {"name": "Sarah", "age": 35},
  {"name": "Mike", "age": 24}
]
```

To return the names of people younger than 30, in the notation we practised use:

```text
$[?(@.age < 30)].name
```

The filter is applied directly to the root array.

I do not need to first select everything using:

```text
$[*]
```

and then apply the filter.

---

# 11. Check Which Level the Filter Applies To

Filters need to be applied to the array containing the objects I want to evaluate.

Consider:

```json
{
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

If I want to filter employees based on salary, I first need to reach an `employees` array.

For example:

```text
$.departments[1].employees
```

Then apply the filter:

```text
$.departments[1].employees[?(@.salary > 85000)]
```

Then retrieve the property I need:

```text
$.departments[1].employees[?(@.salary > 85000)].name
```

---

# 12. Build Complex Paths in Smaller Pieces

If a long JSONPath is difficult to understand, break it down.

For example:

```text
$.departments[1].employees[?(@.salary > 85000)].name
```

Start with:

```text
$
```

Then:

```text
$.departments
```

Then:

```text
$.departments[1]
```

Then:

```text
$.departments[1].employees
```

Then:

```text
$.departments[1].employees[?(@.salary > 85000)]
```

Finally:

```text
$.departments[1].employees[?(@.salary > 85000)].name
```

This makes it easier to identify the exact level where something goes wrong.

---

# 13. Indexes Can Become Incorrect When Data Order Changes

Consider:

```json
{
  "employees": [
    {"name": "John"},
    {"name": "Sarah"}
  ]
}
```

This:

```text
$.employees[1].name
```

returns Sarah because Sarah currently occupies index `1`.

But if the array changes to:

```json
{
  "employees": [
    {"name": "Sarah"},
    {"name": "John"}
  ]
}
```

then:

```text
$.employees[1].name
```

returns John.

If I specifically want Sarah based on her name, a filter can be more appropriate:

```text
$.employees[?(@.name == "Sarah")].name
```

The choice depends on whether the requirement refers to a position or to a property.

---

# 14. Wildcards at Multiple Levels

Consider:

```json
{
  "employees": [
    {
      "name": "John",
      "skills": ["Linux", "Docker"]
    },
    {
      "name": "Sarah",
      "skills": ["Python", "Kubernetes"]
    }
  ]
}
```

This:

```text
$.employees[*].skills
```

selects the `skills` property for every employee.

To select the individual skill items in the notation we practised:

```text
$.employees[*].skills[*]
```

Breakdown:

```text
$.employees       → employees array

[*]               → every employee

.skills           → each employee's skills array

[*]               → every skill
```

Result conceptually:

```text
Linux
Docker
Python
Kubernetes
```

---

# 15. Selecting the Same Position from Every Nested Array

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

This combines:

```text
[*] → every employee

[1] → second skill from each employee
```

---

# 16. Understand Tool Differences

During our practical work, we attempted:

```bash
cat vehicles.json | jpath '$[0]'
```

on the local machine.

The shell reported that:

```text
jpath
```

was not installed.

This did not mean the JSONPath expression itself was wrong.

It meant the local environment did not contain the same JSONPath command used in the lab environment.

This is an important troubleshooting distinction:

```text
Query problem
```

is different from:

```text
Tool/environment problem
```

Before changing a query, first determine whether the required command actually exists.

---

# 17. Check Whether the Tool Exists

A command can be checked using:

```bash
which jpath
```

If there is no result, the command may not be installed or available through the current `PATH`.

The important troubleshooting principle is:

```text
Do not change a correct query simply because the required tool is unavailable.
```

First identify whether the problem is:

```text
JSON data
JSONPath syntax
JSONPath logic
tool availability
or
environment configuration
```

---

# 18. JSONPath Implementations Can Differ

Another important practical lesson is that JSONPath implementations may support different syntax or features.

For example, a particular JSONPath expression may work in one implementation but not in another.

Therefore, when working in a lab or production environment:

```text
Understand the intended query
        ↓
Know which JSONPath implementation is being used
        ↓
Use syntax supported by that implementation
        ↓
Test the expression
        ↓
Verify the output
```

This is especially important when moving between local tools, training environments, scripts, and other systems.

---

# 19. Troubleshooting No Results

If a JSONPath returns no matching data, do not immediately assume the tool is broken.

Check:

```text
1. Is the root correct?

2. Does the property actually exist?

3. Is the property name spelled correctly?

4. Is the array index correct?

5. Is the filter applied to the correct array?

6. Is the comparison operator correct?

7. Does any item actually satisfy the condition?

8. Are all brackets and parentheses closed?

9. Is the syntax supported by the JSONPath implementation?
```

For example:

```text
$.employees[?(@.age > 100)].name
```

may return no results simply because nobody has an age greater than `100`.

That is different from a syntax error.

---

# 20. Troubleshooting Unexpected Results

Sometimes a query returns data, but not the data I expected.

This is similar to the YAML indentation lesson:

```text
Successful execution does not automatically mean correct logic.
```

For example:

```text
$.employees[1].name
```

may successfully return a name.

But I still need to ask:

```text
Is index 1 actually the employee I intended to select?
```

Therefore, verification matters even when the command succeeds.

---

# A Systematic JSONPath Troubleshooting Workflow

When a JSONPath does not behave as expected, I can use this workflow.

## Step 1 — Inspect the JSON

Identify:

```text
Objects
Arrays
Properties
Indexes
Nested levels
```

---

## Step 2 — Identify the Root

Ask:

```text
Does the document begin with { or [ ?
```

Then determine:

```text
Object or Array?
```

---

## Step 3 — Identify the Target

Be clear about exactly what I want.

For example:

```text
David's name
```

or:

```text
all employees earning more than 85000
```

---

## Step 4 — Trace the Route

Example:

```text
Root
 ↓
departments
 ↓
Security
 ↓
employees
 ↓
salary > 85000
 ↓
name
```

---

## Step 5 — Translate the Route into JSONPath

The route above could become:

```text
$.departments[1].employees[?(@.salary > 85000)].name
```

---

## Step 6 — Check the Syntax

Verify:

```text
$
.
[index]
[*]
[?(...)]
@.property
```

and make sure brackets and parentheses are balanced.

---

## Step 7 — Check the Logic

Ask:

```text
Should this be > or >=?

Should this be < or <=?

Should I use an index, wildcard, or filter?
```

---

## Step 8 — Test

Run the expression using the available JSONPath tool.

---

## Step 9 — Inspect the Output

Do not stop because the command executed successfully.

Ask:

```text
Is this actually the expected data?
```

---

## Step 10 — Change Only What the Evidence Shows Is Wrong

Avoid randomly rewriting the entire path.

If:

```text
$.departments[1]
```

already reaches the correct department, keep it.

Continue testing the next part.

This helps isolate the failing section.

---

# Troubleshooting Mental Model

A useful mental model is:

```text
JSON DATA
   ↓
What is the structure?
   ↓
ROOT
   ↓
Object or Array?
   ↓
NAVIGATION
   ↓
Property or Index?
   ↓
SELECTION
   ↓
Index, Wildcard, or Filter?
   ↓
SYNTAX
   ↓
Are brackets and parentheses correct?
   ↓
TOOL
   ↓
Does the environment support the command/syntax?
   ↓
OUTPUT
   ↓
Does the result match the requirement?
```

---

# Key Takeaways

1. Inspect the JSON before writing or changing JSONPath.

2. Determine whether the root is an object or array.

3. Follow the actual JSON structure in order.

4. Remember that array indexing starts at `0`.

5. Check every opening and closing bracket.

6. Filters follow the pattern:

```text
[?(@.property operator value)]
```

7. Use `@.property`, not `@property`, in the filter notation we practised.

8. Choose the correct comparison operator.

9. Use indexes for positions, wildcards for all items, and filters for conditions.

10. Apply filters at the level containing the items being evaluated.

11. Build long JSONPath expressions one level at a time.

12. Distinguish a JSONPath problem from a missing-tool or environment problem.

13. JSONPath implementations can differ.

14. A successful query can still return the wrong logical result.

15. Always verify the output against the requirement.

The overall troubleshooting principle is:

```text
Inspect
   ↓
Understand the structure
   ↓
Build the path
   ↓
Test
   ↓
Observe
   ↓
Change only what the evidence shows is wrong
   ↓
Verify
```

This is the same general troubleshooting approach that can be applied across DevOps tools and systems.
