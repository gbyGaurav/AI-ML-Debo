# LinkedIn Learning Publisher MCP

A simple MCP server that converts daily learning into a LinkedIn post using Claude Desktop and Playwright.

## MCP Primitives

- Tool: `post_to_linkedin` — publishes the post on LinkedIn.
- Resource: `learnings://today/raw` — provides today's learning notes.
- Prompt: `format_linkedin_post` — formats learning into a professional LinkedIn post.

## Workflow

```text
Daily Learning
      ↓
Resource
(learnings://today/raw)
      ↓
Prompt
(format_linkedin_post)
      ↓
Claude generates the post
      ↓
Tool
(post_to_linkedin)
      ↓
Playwright
      ↓
LinkedIn
```

The Resource provides the learning content, the Prompt helps Claude format it into a LinkedIn post, and the Tool uses Playwright to publish the final content.

## Why Playwright?

Playwright is used to automate the LinkedIn browser interaction. The MCP Tool sends the generated post content to Playwright, which opens the logged-in LinkedIn session, enters the content, and publishes the post.

## Tech Stack

- Python
- FastMCP
- Playwright
- Claude Desktop
- MCP

## Project Structure

```text
linkedin-learning-publisher/
├── server.py
├── README.md
├── manifest.json
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── uv.lock
```

## Demo

Watch Demo Video => https://drive.google.com/file/d/1_Y8xXJgu1wAxmMjHJVc5BZOLrvolV4mj/view

## Example

```text
User: Post today's learning on LinkedIn.

Claude:
1. Reads today's learning from the Resource.
2. Uses the Prompt to format the content.
3. Calls post_to_linkedin.
4. Playwright publishes the post on LinkedIn.
```

## Key Learning

This project helped me understand how MCP Tools, Resources, and Prompts work together to create a practical AI workflow and perform a real-world action.

## Scope

The server is designed for local use with Claude Desktop and requires a logged-in LinkedIn session.