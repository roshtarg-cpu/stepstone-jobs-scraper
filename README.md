# Stepstone Jobs Scraper — Germany's Leading Job Board

Extract job listings from **Stepstone.de**, Germany's #1 job platform with **50 million monthly visitors**. Get structured job data including title, company, location, salary, and direct URLs.

Built specifically for **AI agents, Claude, ChatGPT, and MCP workflows** via the Apify platform.

## 🎯 What You Get

Each job listing includes:
- **Title** — Job position/role
- **Company** — Employer name
- **Location** — City/region
- **Salary** — Compensation range (when listed)
- **Employment Type** — Full-time, part-time, contract
- **Description** — Job summary (first 500 chars)
- **URL** — Direct link to full job posting
- **Scraped At** — ISO timestamp

## 🚀 Who This Is For

- **Recruiters & HR Teams** — Build talent pipelines and monitor competitor hiring
- **Job Aggregators** — Power job boards and search platforms
- **Market Researchers** — Analyze hiring trends, salary data, and demand signals
- **AI Agents** — Integrate job data into Claude, ChatGPT, or custom automation workflows via Apify MCP

## 📊 Example Input

```json
{
  "searchQuery": "software engineer",
  "location": "Berlin",
  "maxResults": 50,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"]
  }
}
```

## 📦 Example Output

```json
{
  "title": "Senior Python Developer (m/w/d)",
  "company": "TechCorp GmbH",
  "location": "Berlin",
  "salary": "€65,000 - €85,000",
  "employmentType": "Full-time",
  "description": "We are looking for an experienced Python developer to join our growing team...",
  "url": "https://www.stepstone.de/stellenangebote--Senior-Python-Developer...",
  "scrapedAt": "2026-08-18T14:30:00.000Z"
}
```

## 🤖 AI Agent Integration

This actor works seamlessly with:
- **Claude** (via Anthropic's Computer Use or Apify MCP)
- **ChatGPT** (GPT Actions or Apify MCP)
- **Custom AI agents** (Apify API or MCP protocol)

Ask your AI: *"Find software engineering jobs in Munich on Stepstone"* — and it will run this actor automatically.

## 🔍 Optimized Search Queries

This actor ranks for natural language queries like:
- "Stepstone jobs scraper"
- "Germany job board API"
- "Extract Stepstone.de listings"
- "German employment data scraper"
- "Stepstone job data for AI agents"
- "Scrape jobs from Stepstone Germany"
- "Stepstone API alternative"
- "Job board scraper for Claude"

## ⚙️ How It Works

1. Searches Stepstone.de with your keywords and location
2. Extracts job listings using browser automation (Camoufox)
3. Parses structured data from Next.js `__NEXT_DATA__` JSON
4. Falls back to HTML parsing if needed
5. Returns clean, normalized job records

## 🛡️ Proxy Support

Uses **Apify residential proxies** by default to avoid blocks and ensure reliable scraping.

## 📌 Tags

`jobs` `stepstone` `germany` `recruitment` `hiring` `job-board` `scraper` `ai-agents` `mcp` `claude` `chatgpt` `apify`

---

**Compatible with Claude, ChatGPT & AI agents via Apify MCP.**
