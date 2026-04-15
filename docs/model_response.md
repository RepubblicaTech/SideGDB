# SideGDB's Model responses

GDBMI responses have some kind of a unified structure. I don't really need the whole structure when individual dialogs and windows (breakpoints manager, variables window, etc.) just need the responses' `payload` most of the time.
Next up is a table of all GDBMI commands and their relative custom responses. Optional fields will be shown after the `***` in the JSON object

## Current thread info
### GDBMI Command: `-thread-info`

```json
{
  "current_thread": <current thread id>,
  
  "threads": [
    {
      "id": <thread id>,
      "state": <thread state according to GDB, running, stopped, ...>,
      "frame": {
        // TODO
      },
    },
    ...
  ]
}
```

# Breakpoints list
### GDBMI Command: `-break-list`

```json
[
  {
    "number": <breakpoint number>,
    "enabled": <True | False>,
    "addr": "0xffffffff80035f55",
    ***
    "func": "kstart",
    "file": "src/kernel/kernel.c",
    "fullPath": "/home/repubblicatech/Documenti/VSCode/purpleK2/src/kernel/kernel.c",
    "line": "149",
  },
  ...
]
```

# Breakpoint set
### GDBMI Command: `-break-insert <where>`

An object containing the same dict of a single item from the Breakpoints' list.
