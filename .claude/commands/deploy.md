# Deploy to Staging

Argument: $ARGUMENTS (optional: "main" to deploy to main)

Run the following steps in order. Stop and report on any failure.

1. Confirm there are no uncommitted changes: `git status`
2. Check only files below can be pushed to github
    starter_server.py (Your completed server file)
    starter_client.py (Your completed client file using the OpenAI API)
    server_config.json (Make sure the "llm_inference" path points to starter_server.py!)
    pyproject.toml
    uv.lock
    README.md
3. git commit then push
