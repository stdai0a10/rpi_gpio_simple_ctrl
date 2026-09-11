# Raspberry Pi GPIO Simple Controller

This context defines the vocabulary shared by the Raspberry Pi GPIO controller
and its user-facing web application.

## Frontend foundation

**Frontend shell**:
The initial web-interface boundary that identifies the project without
communicating with device-control services.
_Avoid_: control UI, GPIO dashboard

## GPIO configuration

**GPIO Function**:
A user-addressable named behavior whose definition maps to a BCM GPIO.
_Avoid_: Script, arbitrary pin command

**Function ID**:
A stable lowercase, hyphenated identifier for a GPIO Function,
such as `open-door`, `turn-on`, or `turn-off`.
_Avoid_: command name, GPIO command, Function name, GPIO number

**BCM GPIO Number**:
The Raspberry Pi SoC GPIO number referenced by a GPIO Function definition.
_Avoid_: Physical pin number, board pin
