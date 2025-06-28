# GolfMCP Project Boilerplate

This directory serves as a starting template for new GolfMCP projects. Initialize a project using the `golf init <your-project-name>` command.
## About GolfMCP

GolfMCP is a Python framework designed to build MCP servers with minimal boilerplate. It allows you to define tools, resources, and prompts as simple Python files. These components are then automatically discovered and compiled into a runnable [FastMCP](https://github.com/fastmcp/fastmcp) server.

## Getting Started (After `golf init`)

Once you've initialized your new project from this boilerplate:

1.  **Navigate to your project directory:**
    ```bash
    cd your-project-name
    ```

2.  **Start the development server:**
    ```bash
    golf build dev  # For a development build
    # or
    golf build prod # For a production build
    
    golf run
    ```

## Project Structure

Your initialized GolfMCP project will typically have the following structure:

-   `tools/`: Directory for your tool implementations (Python files defining functions an LLM can call).
-   `resources/`: Directory for your resource implementations (Python files defining data an LLM can read).
-   `prompts/`: Directory for your prompt templates (Python files defining reusable conversation structures).
-   `golf.json`: The main configuration file for your project, including settings like the server name, port, and transport.
-   `pre_build.py`: (Optional) A Python script that can be used to run custom logic before the build process begins, such as configuring authentication.
-   `.env`: File to store environment-specific variables (e.g., API keys). This is created during `golf init`.

## Adding New Components

To add new functionalities:

-   **Tools**: Create a new `.py` file in the `tools/` directory.
-   **Resources**: Create a new `.py` file in the `resources/` directory.
-   **Prompts**: Create a new `.py` file in the `prompts/` directory.

Each Python file should generally define a single component. A module-level docstring in the file will be used as the description for the component. See the example files (e.g., `tools/hello.py`, `resources/info.py`) provided in this boilerplate for reference.

For shared functionality within a component subdirectory (e.g., `tools/payments/common.py`), you can use a `common.py` file.

## Documentation

For comprehensive details on the GolfMCP framework, including component specifications, advanced configurations, CLI commands, and more, please refer to the official documentation:

[https://docs.golf.dev](https://docs.golf.dev)

---

Happy Building! 

<div align="center">
Made with ❤️ in San Francisco
</div>