# Design Documents

This directory contains design documentation for the Raspberry Pi GPIO Simple Controller.

Design documents describe **how product requirements are represented, structured, or implemented**.

Product requirements themselves belong in:

```text
../product-specs/
```

## Structure

The current organization is:

```text
design-docs/
└── ui/
    ├── web-ui-design-spec.md
    ├── color-theme-spec.md
    └── features/
        └── functions-ui-design-spec.md
```

Additional design categories may be introduced when needed, for example:

```text
design-docs/
├── ui/
├── backend/
└── protocols/
```

Do not create empty category directories in advance.

---

# UI Design

UI-related design documents are stored under:

```text
ui/
```

## `ui/web-ui-design-spec.md`

Defines the project-wide Web UI design system and interaction principles.

It covers shared concerns such as:

* Application shell
* Responsive layout
* Mobile-first behavior
* Navigation
* Typography
* Spacing
* Shared components
* Touch targets
* Dialogs
* Toasts
* Loading states
* Accessibility
* General responsive behavior

Feature-specific documents should follow these global rules unless they explicitly define an approved exception.

---

## `ui/color-theme-spec.md`

Defines the shared visual color system.

It covers:

* Primary colors
* Neutral palette
* Semantic colors
* Light theme
* Dark theme
* Surface hierarchy
* Text colors
* Borders
* Focus states
* Disabled states
* Status colors
* Theme tokens

Components should use semantic theme tokens rather than hard-coded colors wherever practical.

If a visual example conflicts with the color specification, the documented theme tokens are authoritative unless the specification itself is updated.

---

# Feature-specific UI Design

Feature-specific UI specifications are stored under:

```text
ui/features/
```

These documents define the UI behavior and presentation of an individual feature.

Example:

```text
ui/features/functions-ui-design-spec.md
```

A feature UI specification may define:

* Page layout
* Feature-specific components
* Dialog behavior
* Editing workflow
* Validation presentation
* Responsive behavior
* Feature-specific interactions

It should not redefine global UI rules unnecessarily.

Instead, it should inherit from:

```text
ui/web-ui-design-spec.md
ui/color-theme-spec.md
```

and document only feature-specific behavior or explicit exceptions.

---

# Product Specs vs Design Docs

Keep functional requirements separate from design decisions.

Example:

```text
"A Function can be enabled or disabled."
```

belongs in:

```text
../product-specs/functions.md
```

while:

```text
"The enabled state is represented by a Switch in the Functions list."
```

belongs in:

```text
ui/features/functions-ui-design-spec.md
```

Another example:

```text
"The system supports Light, Dark, and System themes."
```

may be a product requirement.

The exact colors, tokens, contrast relationships, and component appearance belong in the UI design documentation.

---

# Design Document Rules

When creating or modifying a design document:

1. Identify the product requirement being implemented.
2. Avoid duplicating functional requirements unless necessary for context.
3. Link to related product specifications when available.
4. Reuse global design rules instead of redefining them.
5. Clearly document intentional exceptions.
6. Update the design document when the implemented design materially changes.

If the implementation and an authoritative design document disagree, do not silently treat the implementation as correct. Determine whether the implementation or the document needs to be updated.

---

# Naming

Prefer descriptive lowercase `kebab-case` filenames.

Examples:

```text
web-ui-design-spec.md
color-theme-spec.md
functions-ui-design-spec.md
gpio-ui-design-spec.md
device-protocol.md
```
