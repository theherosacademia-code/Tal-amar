#!/bin/bash
# Claude Code toolkit - cloud environment setup script

S="npx -y skills@latest"

# 1. Agent skills (global, ~/.claude/skills)
$S add https://github.com/Leonxlnx/taste-skill --global --agent claude-code --skill '*' -y || true
$S add vercel-labs/skills --global --agent claude-code --skill find-skills -y || true

# 2. Plugins (user scope)
claude plugin marketplace add obra/superpowers-marketplace || true
claude plugin marketplace add snarktank/ralph || true
claude plugin install superpowers@superpowers-marketplace || true
claude plugin install ralph-skills@ralph-marketplace || true

# 3. MCP servers (user scope)
claude mcp add --scope user playwright npx @playwright/mcp@latest || true
claude mcp add --scope user --transport http context7 https://mcp.context7.com/mcp || true
claude mcp add --scope user --transport http firecrawl https://mcp.firecrawl.dev/v2/mcp || true

exit 0
