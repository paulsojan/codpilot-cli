# CodPilot CLI

A multi agent CLI tool that integrates with GitHub that can help you to review pull requests, create new features, and suggest changes on your behalf — all from your terminal.

## Features

**Review PR** — Analyzes the pull request and posts inline comments with suggestions.

**Create Feature** — It can implements new features, then opens a draft pull request against the target repository.

**Suggest Changes** — Participate in GitHub Issue discussions, analyze the codebase and conversation, and post technical suggestions as comments.

## Available Commands

| Command                       | Description                   |
| ----------------------------- | ----------------------------- |
| `codpilot run`                | Run the agent                 |
| `codpilot reset-github-token` | Reset the stored GitHub token |
| `codpilot change-llm`         | Change the LLM model          |
| `codpilot --version, -v`      | Show the current version      |

`codpilot run` has the following options:

- Review PR
- Create Feature
- Suggest Changes

## Prerequisites

- Python 3.14+
- A GitHub personal access token
- An API key for at least one LLM provider (Gemini, OpenAI, or Anthropic)

## Installing locally

```bash
git clone https://github.com/paulsojan/codpilot-cli.git
cd codpilot-cli
pip install -e .
```

Verify the installation:

```bash
codpilot --version
```

## Usage

```bash
codpilot run
```

The interactive prompt will walk you through:

1. Selecting an agent (Review PR / Create Feature / Suggest Changes)
2. Entering the GitHub URL (PR, repository, or issue depending on the agent)
3. Choosing an LLM provider (Gemini / OpenAI / Anthropic)
4. Providing API credentials for github and LLM (cached in your system keychain for future runs)

## Supported Models

| Provider  | Model                        |
| --------- | ---------------------------- |
| Gemini    | `gemini-3-flash-preview`     |
| OpenAI    | `gpt-5-mini`                 |
| Anthropic | `claude-3-7-sonnet-20250219` |
