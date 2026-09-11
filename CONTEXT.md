# Raspberry Pi GPIO Simple Controller

This context defines the vocabulary for the Raspberry Pi GPIO controller
and its user-facing web application.

## Frontend foundation

**Frontend shell**:
The initial web-interface boundary that identifies the project without
communicating with device-control services.
_Avoid_: control UI, GPIO dashboard

## GPIO configuration

**Function ID**:
A stable lowercase, hyphenated identifier for a configured GPIO action,
such as `open-door`, `turn-on`, or `turn-off`.
_Avoid_: command name, GPIO command
