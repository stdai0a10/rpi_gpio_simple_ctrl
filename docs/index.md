# Project Documentation

This directory contains the persistent documentation for the Raspberry Pi GPIO Simple Controller project.

The documentation is organized by purpose. Before making changes, read the documents relevant to the affected area instead of scanning the entire `docs/` directory.

## Directory Structure

```text
docs/
├── agents/
├── design-docs/
├── product-specs/
└── references/
```

## Documentation Categories

### `agents/`

Agent-managed project information.

Current files include:

* `domain.md`
* `issue-tracker.md`
* `triage-labels.md`

Files in this directory are created or maintained by project Skills.

Do not move, rename, reorganize, or repurpose files under `docs/agents/` unless explicitly required by the Skill responsible for them.

---

### `design-docs/`

Technical and user-interface design documentation.

Use this directory for documents that describe **how a requirement is designed or implemented**.

Examples:

* UI structure and interaction design
* Theme and design-system specifications
* Feature-specific UI design
* Backend architecture
* Protocol design
* Significant implementation design decisions

See:

* [`design-docs/index.md`](design-docs/index.md)

---

### `product-specs/`

Product and functional requirements.

Use this directory for documents that describe **what the system must do**, including:

* Functional behavior
* User-visible behavior
* Business rules
* Validation rules
* Feature requirements
* Constraints that are part of the product definition

Implementation details and UI presentation rules should normally not be defined here unless they are themselves product requirements.

See:

* [`product-specs/index.md`](product-specs/index.md)

---

### `references/`

Supporting reference material.

Use this directory for information that helps understand or implement the project but is not itself a project requirement or design specification.

Examples:

* External protocol notes
* Hardware reference material
* Third-party API notes
* Research notes
* Compatibility information

Reference documents must not silently override product specifications or design documents.

---

## Documentation Responsibility

A useful rule when deciding where information belongs:

```text
What must the product do?
→ product-specs/

How should it be designed or implemented?
→ design-docs/

What external or supporting information is useful?
→ references/

What information is maintained by project Skills?
→ agents/
```

## Source of Truth

When documents overlap, prefer the document whose responsibility most directly matches the subject.

For example:

```text
Functional behavior
→ product-specs/

UI presentation and interaction
→ design-docs/ui/

External technical information
→ references/
```

If two authoritative project documents contradict each other, do not silently choose one. Identify the conflict and resolve it before implementation.

## Documentation Maintenance

When a code change modifies documented behavior:

1. Update the relevant product specification if functional behavior changes.
2. Update the relevant design document if implementation or UI design changes.
3. Keep links between related documents valid.
4. Avoid duplicating the same authoritative rule across multiple documents.
5. Prefer linking to the authoritative document instead of copying its contents.

## File Naming

Prefer lowercase `kebab-case` names for new documentation files.

Example:

```text
functions-ui-design-spec.md
gpio-control.md
device-protocol.md
```

Existing files may be renamed separately when appropriate.
