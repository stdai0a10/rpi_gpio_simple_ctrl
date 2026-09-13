# Product Specifications

This directory contains the functional and product requirements for the Raspberry Pi GPIO Simple Controller.

Product specifications describe:

> **What the system must do and what behavior users or external systems can rely on.**

They should avoid unnecessary implementation details.

## Purpose

Use product specifications to define:

* Features
* Functional behavior
* Business rules
* Validation rules
* User-visible behavior
* System constraints
* State transitions
* Error behavior
* Permissions and restrictions
* Required interactions between features

These documents should remain useful even if the implementation technology changes.

---

# What Belongs Here

Examples of appropriate product requirements:

```text
Users can create Functions.

Each Function can be independently enabled or disabled.

A disabled Function cannot be executed.

Function configuration must be validated before it is saved.

GPIO output state must only be treated as changed after the server confirms
the operation.

The UI supports System, Light, and Dark theme preferences.
```

These describe observable system behavior.

---

# What Does Not Normally Belong Here

Detailed presentation rules:

```text
The switch is 40px wide.
The dialog has a 16px border radius.
The active color is #6366F1.
```

These belong in:

```text
../design-docs/ui/
```

Implementation details:

```text
Use a Vue computed property.
Store Functions in a Python dictionary.
Use FastAPI dependency injection.
```

These belong in design or implementation documentation when they need to be documented.

External reference information belongs in:

```text
../references/
```

---

# Suggested Organization

Create specifications by product domain or feature rather than by individual implementation task.

For example:

```text
product-specs/
├── index.md
├── gpio.md
├── functions.md
├── system-status.md
├── logs.md
└── settings.md
```

Split documents further only when a specification becomes difficult to navigate.

Avoid excessive fragmentation.

---

# Recommended Specification Structure

A product specification may use the following structure where appropriate:

```markdown
# Feature Name

## Purpose

## Scope

## Terminology

## Requirements

## Behavior

## Validation

## Error Cases

## Constraints

## Related Specifications

## Related Design Documents
```

Not every document needs every section.

Prefer the smallest structure that clearly describes the feature.

---

# Requirement Language

Requirements should be precise enough that implementation and tests can determine whether they are satisfied.

Prefer:

```text
A Function must have a unique identifier.
```

over:

```text
Functions should probably have an identifier.
```

Prefer describing externally observable behavior over implementation details.

Use terms consistently across specifications.

When introducing an important domain term, define it before relying on it.

---

# Relationship to Tests

Product specifications define expected behavior.

Tests should verify that behavior where practical.

A specification should not be rewritten merely to match an incorrect implementation or failing test.

When behavior intentionally changes:

```text
Product Spec
    ↓
Tests
    ↓
Implementation
```

should be updated consistently.

---

# Relationship to Design Documents

Product specifications define **what**.

Design documents define **how**.

For example:

```text
product-specs/functions.md

Requirement:
Each Function can be independently enabled or disabled.
```

A related design document may define:

```text
../design-docs/ui/features/functions-ui-design-spec.md

Design:
The enabled state is controlled using a Switch displayed in the Functions
list and editor.
```

The design must satisfy the product requirement.

---

# Conflicts

If two product specifications define contradictory behavior:

1. Do not infer which one is newer or more important solely from the filename.
2. Identify the conflicting requirements.
3. Resolve the conflict before implementing dependent behavior.
4. Update the obsolete specification.

Design documents must not silently override product requirements.

---

# Maintenance

When modifying product behavior:

1. Find the relevant specification.
2. Update the requirement before or together with the implementation.
3. Update related tests.
4. Update related design documents if the design also changes.
5. Avoid leaving obsolete requirements in active specifications.

Git history should normally be used to inspect previous versions instead of keeping multiple active copies of the same specification.

---

# Naming

Prefer lowercase `kebab-case` filenames representing stable product concepts.

Examples:

```text
gpio.md
functions.md
system-status.md
settings.md
```

Avoid task-oriented names such as:

```text
fix-functions-v2.md
new-gpio-page.md
changes-september.md
```

Task-specific planning belongs outside the product specification itself.
