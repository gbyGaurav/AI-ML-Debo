# LinkedIn Learning Publisher MCP

A simple MCP server that converts daily learning into a LinkedIn post using Claude Desktop and Playwright.

## MCP Primitives

- Tool: `post_to_linkedin` — publishes the post on LinkedIn.
- Resource: `learnings://today/raw` — provides today's learning notes.
- Prompt: `format_linkedin_post` — formats learning into a professional LinkedIn post.

## Workflow

Learning Notes → Resource → Prompt → Tool → LinkedIn

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
├── daily_notes.txt
├── README.md
├── pyproject.toml
├── requirements.txt
└── .gitignore
Demo

Watch Demo Video