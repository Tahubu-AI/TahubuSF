![TahubuSF](media/tahubusf-light.png)

GenAI product TahubuSF for Sitefinity - Product repo

## MCP server setup

To run the MCP server, you need to have Python 3.10 or higher installed on your machine. You can download it from the official website: [Python Downloads](https://www.python.org/downloads/).

In VS Code, you need to create a new Python environment. You can do this by opening the terminal in VS Code and running the following command:

```bash
python -m venv venv
```

This will create a new virtual environment named `venv`. You can activate the virtual environment by running the following command:

- On Windows:

```bash
.venv/Scripts/Activate.ps1
```

- On macOS and Linux:

```bash
source venv/bin/activate
```

Next, you need to install `uv`. You can follow the instructions in the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

After activating the virtual environment and installing `uv`, you should see `(venv)` at the beginning of your terminal prompt. This indicates that you are now working within the virtual environment.

```bash
pip install -r requirements.txt
```

## Run the MCP server

To run the MCP server, navigate to the directory where the `main.py` file is located and run the following command:

```bash
mcp dev main.py
```

## Claude Desktop use

To use the MCP server in Claude desktop you need open the `claude_desktop_config.json` file and include the following lines:  `change the directory to wherever it is installed on your machine`

```json
{
    "mcpServers":{
        "TahubuSF": {
            "command": "uv",
            "args": [
                "--directory",
                "e:\\TahubuSF",
                "run",
                "main.py"
            ]
        }
    }
}
```
