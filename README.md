![TahubuSF](media/tahubusf-light.png)
GenAI product TahubuSF for Sitefinity - Product repo

## Claude Desktop use
To use the MCP server in Claude desktop you need open the `claude_desktop_config.json` file and include the following lines:  `chnage the dirtectory to wherever it is installed on your machine`

```json
{
    "mcpServers":{
        "TahubuSF": {
            "command": "uv",
            "args": [
                "--directory",
                "e:\\MCPSamples\\01-firstlesson",
                "run",
                "main.py"
            ]
        }
    }
}
```
