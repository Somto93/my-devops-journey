# YAML Indentation

## Why Indentation Matters

Indentation is important in YAML because it determines the relationship between data.

Unlike formats that rely heavily on brackets, YAML uses indentation to show which values belong under which keys.

For example:

```yaml
Banana:
  Calories: 105
  Fat: 0.4
  Carbs: 27
```

Here:

```text
Banana
   ↓
Dictionary
   ├── Calories: 105
   ├── Fat: 0.4
   └── Carbs: 27
```

`Calories`, `Fat`, and `Carbs` are aligned at the same indentation level, so they belong to the same dictionary.

---

## Indentation Shows Parent-Child Relationships

Consider:

```yaml
Employee:
  Name: John
  Role: Developer
  Skills:
    - Linux
    - Docker
```

The indentation tells us:

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

`Name`, `Role`, and `Skills` belong to `Employee`.

`Linux` and `Docker` belong to `Skills`.

---

# Our Broken YAML Experiment

During the practical exercise, we created `broken.yaml`.

It contained:

```yaml
Fruits:
  - Banana:
      Calories: 105
      Fat: 0.4
    Carbs: 27
```

At first glance, it might look as though `Carbs` belongs to `Banana`.

However, look carefully at the indentation:

```yaml
  - Banana:
      Calories: 105
      Fat: 0.4
    Carbs: 27
```

`Carbs` is not aligned with `Calories` and `Fat`.

Therefore, it does not belong inside the `Banana` dictionary.

---

## Testing the YAML

We used Python with PyYAML to inspect how the file was actually interpreted:

```bash
python3 -c "import yaml; print(yaml.safe_load(open('broken.yaml')))"
```

The result was:

```text
{'Fruits': [{'Banana': {'Calories': 105, 'Fat': 0.4}, 'Carbs': 27}]}
```

This was an important result.

The YAML parser did **not** reject the file.

Instead, it interpreted the structure differently from what we intended.

---

# Understanding the Parsed Structure

The parser interpreted:

```yaml
Fruits:
  - Banana:
      Calories: 105
      Fat: 0.4
    Carbs: 27
```

as approximately:

```text
Fruits
  ↓
List
  ↓
Dictionary
  ├── Banana
  │     ↓
  │   Dictionary
  │     ├── Calories: 105
  │     └── Fat: 0.4
  │
  └── Carbs: 27
```

This means `Carbs` became a sibling of `Banana`.

It was **not** part of the dictionary stored under `Banana`.

---

## Verifying the Banana Dictionary

We then specifically inspected the value stored under `Banana`:

```bash
python3 -c "import yaml; d=yaml.safe_load(open('broken.yaml')); print(d['Fruits'][0]['Banana'])"
```

The result was:

```text
{'Calories': 105, 'Fat': 0.4}
```

`Carbs` was missing.

This confirmed that the indentation had changed the structure.

---

# Correcting the Indentation

We corrected the YAML to:

```yaml
Fruits:
  - Banana:
      Calories: 105
      Fat: 0.4
      Carbs: 27
```

Now `Calories`, `Fat`, and `Carbs` are aligned.

The intended structure is:

```text
Fruits
  ↓
List
  ↓
Banana
  ↓
Dictionary
  ├── Calories: 105
  ├── Fat: 0.4
  └── Carbs: 27
```

When we parsed the corrected file, the `Banana` dictionary contained:

```text
{'Calories': 105, 'Fat': 0.4, 'Carbs': 27}
```

This was the structure we intended.

---

# Important Lesson: Valid Does Not Always Mean Correct

One of the most important lessons from this exercise was:

```text
Valid YAML ≠ Correct YAML structure
```

A YAML file can be syntactically valid while representing the wrong data structure.

This can be more difficult to troubleshoot than a simple syntax error.

If YAML is invalid, a parser may immediately report an error.

But if YAML is valid with incorrect indentation, the application may accept the file and behave differently from what was expected.

Therefore, I should not only ask:

```text
Is this YAML valid?
```

I should also ask:

```text
Does the parsed structure match what I intended?
```

---

# How to Troubleshoot YAML Indentation

When YAML behaves unexpectedly, I can troubleshoot it systematically.

## Step 1 — Inspect the indentation

Look at which keys and values are aligned.

Example:

```yaml
Banana:
  Calories: 105
  Fat: 0.4
Carbs: 27
```

Ask:

```text
Is Carbs actually at the same level as Calories and Fat?
```

---

## Step 2 — Identify the parent

For every value, ask:

```text
What key does this value belong to?
```

For example:

```yaml
Skills:
  - Linux
  - Docker
```

`Linux` and `Docker` belong to `Skills`.

---

## Step 3 — Look for list markers

Remember:

```text
-
```

indicates a list item.

Example:

```yaml
Employees:
  - Name: John
  - Name: Sarah
```

The `-` tells us that `Employees` contains a list.

---

## Step 4 — Parse the YAML

If the structure is unclear, use a parser.

For our practical files, we used Python and PyYAML:

```bash
python3 -c "import yaml; print(yaml.safe_load(open('broken.yaml')))"
```

This lets us see the structure that the computer actually understands.

---

## Step 5 — Inspect a Specific Part

Instead of printing the entire structure, I can inspect a particular value.

For example:

```bash
python3 -c "import yaml; d=yaml.safe_load(open('broken.yaml')); print(d['Fruits'][0]['Banana'])"
```

This helped us confirm exactly what was stored under `Banana`.

---

## Step 6 — Correct the Structure

After identifying the problem, fix the indentation:

```yaml
Fruits:
  - Banana:
      Calories: 105
      Fat: 0.4
      Carbs: 27
```

---

## Step 7 — Verify Again

Parse the YAML again after making the change.

The troubleshooting process becomes:

```text
Inspect
   ↓
Form an idea of the structure
   ↓
Parse
   ↓
Compare actual vs intended structure
   ↓
Correct indentation
   ↓
Parse again
   ↓
Verify
```

---

# Indentation and Lists of Dictionaries

Indentation becomes especially important when lists and dictionaries are combined.

Correct:

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
   ├── Dictionary
   │     ├── Name
   │     ├── Role
   │     └── Skills → List
   │
   └── Dictionary
         ├── Name
         ├── Role
         └── Skills → List
```

Notice that:

```yaml
Name:
Role:
Skills:
```

are aligned because they belong to the same employee dictionary.

The skill items are indented further because they belong under `Skills`.

---

# Key Takeaways

1. YAML uses indentation to represent structure.

2. Items at the same indentation level generally belong at the same structural level.

3. `-` identifies list items.

4. Incorrect indentation can change which dictionary a value belongs to.

5. Incorrect indentation does not always cause a syntax error.

6. A YAML file can be valid but still represent the wrong structure.

7. Parsing the YAML allows me to inspect what the computer actually understands.

8. After making a correction, I should verify the structure again.

A useful troubleshooting principle is:

```text
Do not assume that "valid" means "correct."

Inspect the structure, test it, and verify that the result matches the intended data.
```
