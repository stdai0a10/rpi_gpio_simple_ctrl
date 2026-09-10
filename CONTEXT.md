# Raspberry Pi GPIO Simple Control

This context defines the user-facing GPIO control concepts shared across the project.

## Language

**GPIO Function**:
A user-addressable named behavior whose definition maps to a BCM GPIO.
_Avoid_: Script, arbitrary pin command

**Function ID**:
The lowercase hyphenated identifier of a GPIO Function, such as `door-lock`.
_Avoid_: Function name, GPIO number

**BCM GPIO Number**:
The Raspberry Pi SoC GPIO number referenced by a GPIO Function definition.
_Avoid_: Physical pin number, board pin
