# CodPilot CLI

![codpilot](https://img.shields.io/pypi/v/codpilot)

A multi-agent CLI tool that integrates with GitHub to review pull requests, create new features, and suggest changes on your behalf — all from your terminal.

Built with [Google ADK](https://github.com/google/adk-python) and [GitHub MCP](https://github.com/github/github-mcp-server).

## Quick Install

```bash
pip install codpilot
```

## Key Features

**Review PR** — Analyzes a pull request and posts inline code review comments with suggestions.

**Create Feature** — Analyzes the existing codebase, implements a described feature, and opens a draft pull request.

**Suggest Changes** — Reads a GitHub Issue discussion, analyzes the codebase, and posts technical suggestions as comments.

## Available Commands

| Command                       | Description                   |
| ----------------------------- | ----------------------------- |
| `codpilot run`                | Run the agent                 |
| `codpilot reset-github-token` | Reset the stored GitHub token |
| `codpilot change-llm`         | Change the LLM model          |
| `codpilot --version, -v`      | Show the current version      |

## Prerequisites

- Python 3.14+
- A GitHub personal access token
- An API key for at least one LLM provider (Gemini, OpenAI, or Anthropic)

## Creating a GitHub Personal Access Token (Classic)

1. Go to [GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)](https://github.com/settings/tokens)
2. Click **Generate new token** > **Generate new token (classic)**

## Usage

```bash
codpilot run
```

The interactive prompt will walk you through:

1. Selecting an agent (Review PR / Create Feature / Suggest Changes)
2. Entering the GitHub URL (PR, repository, or issue depending on the agent)
3. Choosing an LLM provider (Gemini / OpenAI / Anthropic)
4. Providing API credentials for GitHub and the LLM (cached in your system keychain for future runs)

## Supported Models

| Provider  | Model                        |
| --------- | ---------------------------- |
| Gemini    | `gemini-3-flash-preview`     |
| OpenAI    | `gpt-5-mini`                 |
| Anthropic | `claude-3-7-sonnet-20250219` |

## Development Setup

```bash
git clone https://github.com/paulsojan/codpilot-cli.git
cd codpilot-cli
pip install -e .
```

Verify the installation:

```bash
codpilot --version
```
