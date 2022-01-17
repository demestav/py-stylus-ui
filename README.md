# py-stylus-ui
Map a Wacom stylus tablet to specific area on the screen.

## Installation
`python -m pip install py-stylus-ui`

## Usage
Resize the window to the area that you want to map and click the button. The stylus now will work only within those boundaries.

## How it works
It is wrapper around `xsetwacom` command that defines the `MapToOutput`.

## Why
In cases where the result on the screen has to closely match the physical movement of the hand, e.g taking notes, it may be desirable to adjust the effective area on the screen to achieve this.

## Planned features
- Save different areas (profiles)
- Switch between profiles through a shortcut. This will allow to map the tablet buttons to iterate through profiles.
- Different aspect ratios
- Tablet rotation
- 1:1 mapping
- ...
