# SideGDB's Model responses

I don't really need all of the things that GDBMI gives me as a response. So I'm just going to make some simpler JSONs as responses that are processed by the model, that are given to the controller. Next up is a table of all of the commands and their relative custom responses.

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
        <big frame with info e.g. current address, function name, file, line, etc.
        (this comes directly from pyGDBMI)>
      },
    },
    ...
  ]
}
```
