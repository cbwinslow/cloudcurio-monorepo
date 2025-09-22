# Dockerfile for MCP Server with BlackArch Tools

FROM node:18-alpine

# Install system dependencies
RUN apk add --no-cache \
    curl \
    wget \
    git \
    bash \
    python3 \
    py3-pip \
    && rm -rf /var/cache/apk/*

# Create working directory
WORKDIR /app

# Copy MCP server files
# In a real implementation, you would copy the actual MCP server files here
# For now, we'll create a simple placeholder

# Install MCP server dependencies
RUN npm install express cors mcp-server

# Create a simple MCP server
RUN echo 'const express = require("express");
const cors = require("cors");
const { createServer } = require("mcp-server");

const app = express();
app.use(cors());
app.use(express.json());

// Create MCP server
const server = createServer({
  name: "BlackArch MCP Server",
  version: "1.0.0",
  description: "MCP Server with BlackArch Linux tools integration"
});

// Register BlackArch tools as MCP tools
server.registerTool({
  name: "nmap-scan",
  description: "Perform network scanning with Nmap",
  inputSchema: {
    type: "object",
    properties: {
      target: { type: "string" },
      options: { type: "string" }
    },
    required: ["target"]
  },
  execute: async (input) => {
    // In a real implementation, this would execute nmap
    return {
      result: `Nmap scan results for ${input.target}`,
      command: `nmap ${input.options || ""} ${input.target}`
    };
  }
});

server.registerTool({
  name: "whois-lookup",
  description: "Perform WHOIS lookup",
  inputSchema: {
    type: "object",
    properties: {
      domain: { type: "string" }
    },
    required: ["domain"]
  },
  execute: async (input) => {
    // In a real implementation, this would execute whois
    return {
      result: `WHOIS information for ${input.domain}`,
      command: `whois ${input.domain}`
    };
  }
});

// Mount MCP server routes
app.use("/mcp", server.router);

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`BlackArch MCP Server running on port ${PORT}`);
});' > index.js

# Expose port
EXPOSE 3000

# Start the application
CMD ["node", "index.js"]