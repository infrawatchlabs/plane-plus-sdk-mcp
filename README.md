<br />

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/plane-plus-lockup-light.svg">
    <img src=".github/assets/plane-plus-lockup-dark.svg" alt="Plane Plus SDK + MCP" width="460">
  </picture>
</p>

<h1 align="center">Plane Plus SDK + MCP</h1>
<p align="center">
  <b>Typed Python client and MCP server for
  <a href="https://github.com/eyriehq/plane-plus">Plane Plus</a> — built for
  AI agents.</b>
</p>
<p align="center">
  by <a href="https://eyriehq.com">EyrieHQ</a> · Apache-2.0
</p>

<p align="center">
  <a href="#quickstart--mcp-server"><b>MCP quickstart</b></a> •
  <a href="#quickstart--python-sdk"><b>SDK quickstart</b></a> •
  <a href="#configuration"><b>Config</b></a> •
  <a href="https://github.com/eyriehq/plane-plus"><b>Plane Plus fork</b></a>
</p>

---

## What is this?

Two things in one repo, sharing the same HTTP layer:

- **`plane_sdk`** — a typed Python client for the Plane Plus API. Covers
  projects, work items, cycles, modules, labels, states, pages, first-class
  epics, workspace wiki pages, page folders, intake, and members.
- **`mcp_server`** — a [FastMCP](https://github.com/jlowin/fastmcp) server
  that exposes every SDK method as an MCP tool so LLM agents (Claude Code,
  Claude Desktop, Cursor, Continue, etc.) can manage a Plane Plus workspace
  directly.

Designed for and supported against
[Plane Plus](https://github.com/eyriehq/plane-plus) — an AI-agent-first
fork of [Plane](https://plane.so). Assumes the Plane Plus
`/api/v1/` surface (API-key auth, markdown round-trip on pages, first-class
epics, page folders).

## Requirements

- Python **3.11+**
- A Plane workspace and an API key (Workspace Settings → API tokens)
- For the MCP server: an MCP-aware client such as Claude Code, Claude Desktop,
  or Cursor — **and** [`uv`](https://docs.astral.sh/uv/) installed (the
  recipes below use `uvx` for zero-install runs)

---

## Quickstart — MCP server

The recommended way to run the MCP server is via `uvx`, which fetches and runs
the latest release without polluting your global environment.

### Claude Code

Add to your `.claude.json` or workspace `.mcp.json`:

```json
{
  "mcpServers": {
    "plane": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/eyriehq/plane-plus-sdk-mcp.git",
        "plane-mcp"
      ],
      "env": {
        "PLANE_BASE_URL": "https://plane.example.com",
        "PLANE_API_KEY": "plane_api_...",
        "PLANE_WORKSPACE_SLUG": "my-workspace"
      }
    }
  }
}
```

Restart Claude Code. Verify with `/mcp` — you should see `plane` listed with
its tools enabled. Try a prompt like:

> List the work items in the "Engineering" project.

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "plane": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/eyriehq/plane-plus-sdk-mcp.git",
        "plane-mcp"
      ],
      "env": {
        "PLANE_BASE_URL": "https://plane.example.com",
        "PLANE_API_KEY": "plane_api_...",
        "PLANE_WORKSPACE_SLUG": "my-workspace"
      }
    }
  }
}
```

Fully quit and relaunch Claude Desktop. The Plane tools appear under the
hammer icon in the message composer.

### Cursor

Go to **Settings → MCP → Add new MCP server** and paste the equivalent JSON
(same shape as above). Cursor picks it up automatically.

### Other MCP clients

Any MCP-aware client can use the same command. The binary is `plane-mcp`,
installed as a `[project.scripts]` entry in the package metadata. If your
client expects stdio transport, that's what FastMCP exposes by default.

### Pinning a version

The examples above track `main`. For stability, pin to a tag:

```
"args": ["--from", "git+https://github.com/eyriehq/plane-plus-sdk-mcp.git@v1.0.0", "plane-mcp"]
```

Or to a specific commit:

```
"args": ["--from", "git+https://github.com/eyriehq/plane-plus-sdk-mcp.git@abcd123", "plane-mcp"]
```

To force a re-fetch after a new release: `uvx --refresh --from ...`.

---

## Quickstart — Python SDK

### Install

```bash
pip install git+https://github.com/eyriehq/plane-plus-sdk-mcp.git
```

Or with uv:

```bash
uv add git+https://github.com/eyriehq/plane-plus-sdk-mcp.git
```

### Use

```python
from plane_sdk import PlaneClient

client = PlaneClient(
    base_url="https://plane.example.com",
    api_key="plane_api_...",
    workspace_slug="my-workspace",
)

# Projects & work items
projects = client.list_projects()
project_id = projects[0]["id"]

work_item = client.create_work_item(
    project_id,
    name="Fix the metrics pipeline",
    priority="high",
)

# Parent / child linking
epic = client.create_work_item(project_id, name="Q2 launch")
client.create_work_item(
    project_id,
    name="Ship GCP collector",
    parent_id=epic["id"],
)

# Workspace wiki pages with markdown round-trip
page = client.create_workspace_page(
    name="Launch plan",
    description_html="# Goals\n\n- Fix metrics\n- Ship GCP",
    content_format="markdown",
)
md = client.get_workspace_page(page["id"], response_format="markdown")
print(md["description_markdown"])
```

The full resource surface:

| Mixin              | Covers                                                  |
| ------------------ | ------------------------------------------------------- |
| `ProjectsMixin`    | list, create, retrieve, update, delete projects         |
| `WorkItemsMixin`   | CRUD + `parent_id` for sub-items; comments; links; relations; activities |
| `StatesMixin`      | CRUD for workflow states                                |
| `LabelsMixin`      | CRUD for labels                                         |
| `ModulesMixin`     | CRUD + module/work-item association                     |
| `CyclesMixin`      | CRUD + cycle/work-item association, transfer           |
| `PagesMixin`       | project-scoped pages with markdown round-trip           |
| `WorkspacePagesMixin` | workspace-level wiki pages + folders                 |
| `MembersMixin`     | workspace & project members                             |
| `IntakeMixin`      | project intake / triage work items                      |
| `EpicsMixin`       | first-class epics + analytics                           |

---

## Configuration

The MCP server reads its configuration from environment variables:

| Variable               | Required | Example                                  |
| ---------------------- | -------- | ---------------------------------------- |
| `PLANE_BASE_URL`       | yes      | `https://plane.example.com`              |
| `PLANE_API_KEY`        | yes      | `plane_api_...`                          |
| `PLANE_WORKSPACE_SLUG` | yes      | `my-workspace`                           |

The SDK takes the same values as constructor arguments — no environment
reads. Integrators that want env-driven behavior can wrap `PlaneClient`
trivially:

```python
import os
from plane_sdk import PlaneClient

client = PlaneClient(
    base_url=os.environ["PLANE_BASE_URL"],
    api_key=os.environ["PLANE_API_KEY"],
    workspace_slug=os.environ["PLANE_WORKSPACE_SLUG"],
)
```

### Where do I get an API key?

In your Plane workspace:

1. Click your avatar → **Settings**.
2. Navigate to **API tokens**.
3. Create a token with the scope you need. Copy the value — you can't view
   it again after this screen.

API tokens are workspace-scoped and inherit the creating user's permissions.

---

## Development

Clone, install in editable mode, and run the MCP server against your instance:

```bash
git clone https://github.com/eyriehq/plane-plus-sdk-mcp.git
cd plane-sdk-mcp
uv sync
export PLANE_BASE_URL=https://plane.example.com
export PLANE_API_KEY=plane_api_...
export PLANE_WORKSPACE_SLUG=my-workspace
uv run plane-mcp
```

For an MCP client to use your local checkout instead of the released version,
point it at the directory:

```json
{
  "command": "uv",
  "args": ["--directory", "/path/to/plane-sdk-mcp", "run", "plane-mcp"],
  "env": { "PLANE_BASE_URL": "...", "PLANE_API_KEY": "...", "PLANE_WORKSPACE_SLUG": "..." }
}
```

### Running tests

*(to be added — PRs welcome)*

---

## Contributing

Pull requests are welcome. For large changes, open an issue first to discuss
scope.

By contributing, you agree that your contribution will be licensed under the
Apache License 2.0 (see [LICENSE](./LICENSE)).

## License

Apache License 2.0. See [LICENSE](./LICENSE).

## Related projects

- **[Plane Plus](https://github.com/eyriehq/plane-plus)** — an AI-agent-first
  fork of Plane. This SDK is the most direct way to drive it.
- **[Plane](https://plane.so)** — the upstream project this SDK is a client
  for. The core SDK surface works against any Plane instance.
- **[EyrieHQ](https://eyriehq.com)** — the observability platform that ships
  this SDK alongside Plane Plus.

---

<p align="center">
  <em>Built by <a href="https://eyriehq.com">EyrieHQ</a>.</em>
</p>
