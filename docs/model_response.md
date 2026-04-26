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
        // the frame as-is from -thread-info
      },
    },
    ...
  ]
}
```

# Breakpoint set
### GDBMI Command: `-break-insert <where>`

```json
{
  "number": <breakpoint number>,
  "enabled": True | False,
  "addr": <address of breakpoint>,
  ***
  "where": <function name, taken from "func", "at"> | None,
  "source": <source file path, taken from "file">,
  "sourceFullPath": <actual source path, if present> | None,
  "line": <line of breakpoint> | None,
}
```

# Breakpoints list
### GDBMI Command: `-break-list`

```json
[
  <the same object from the breakpoint set command>
  ,
  ...
]
```
