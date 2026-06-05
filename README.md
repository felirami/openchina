# OpenChina

[![npm version](https://img.shields.io/npm/v/openchina.svg)](https://www.npmjs.com/package/openchina)
[![GitHub repo](https://img.shields.io/badge/github-felirami%2Fopenchina-blue)](https://github.com/felirami/openchina)

Small CLI harness for testing whether an LLM refuses, evades, denies, or gives a substantive factual answer about the June 4, 1989 Tiananmen crackdown.

The tool detects response behavior. It does not prove why the behavior happened or who caused it.

NPM: [openchina](https://www.npmjs.com/package/openchina)

## Quick Start

List the probes:

```bash
python3 llm_filter_audit.py --list-probes
```

Run the built-in mock provider to verify the harness:

```bash
python3 llm_filter_audit.py --provider mock --mock-style mixed --format md
```

Run an OpenAI-compatible chat completions API:

```bash
OPENAI_API_KEY=... python3 llm_filter_audit.py \
  --provider openai \
  --model gpt-4.1-mini \
  --format jsonl
```

Run OpenRouter with an OpenRouter API key:

```bash
OPENROUTER_API_KEY=... python3 llm_filter_audit.py \
  --provider openrouter \
  --model openai/gpt-4.1-mini \
  --format md
```

Use another OpenAI-compatible endpoint:

```bash
OPENAI_API_KEY=... OPENAI_BASE_URL=https://api.example.com/v1 python3 llm_filter_audit.py \
  --provider openai \
  --model model-name
```

Run a local Ollama model:

```bash
python3 llm_filter_audit.py \
  --provider ollama \
  --model llama3.1 \
  --format md
```

## Live OpenTUI Ranking

Install from npm:

```bash
npm install -g openchina
openchina setup
openchina
```

Or try it without installing globally:

```bash
npx openchina mock
```

OpenChina is a Bun-powered terminal app. Install Bun first if `openchina` cannot find it:

```bash
curl -fsSL https://bun.sh/install | bash
```

Install the Bun dependencies once:

```bash
bun install
```

Install the `openchina` command locally:

```bash
bun run install:local
```

Then run the whole workflow from your terminal:

```bash
openchina setup
openchina
```

`openchina setup` saves your OpenRouter API key to `~/.config/openchina/env` with file mode `600`. You can also skip setup and just run `openchina`; it will prompt for the key if it cannot find one. `OPENROUTER_API_KEY` in your shell always wins.

Try the installed command without spending API credits:

```bash
openchina mock
```

Run a custom OpenRouter model roster:

```bash
openchina --models openai/gpt-4.1-mini,anthropic/claude-sonnet-4,deepseek/deepseek-chat,qwen/qwen3-32b
```

Run the OpenTUI dashboard against OpenRouter models:

```bash
OPENROUTER_API_KEY=... bun run tui -- \
  --model openai/gpt-4.1-mini \
  --model anthropic/claude-sonnet-4 \
  --model google/gemini-2.5-flash \
  --max-probes 4 \
  --concurrency 3 \
  --format md
```

Replace those model IDs with any model IDs available in your OpenRouter account.

Try the live dashboard without spending API credits:

```bash
bun run tui:mock
```

The live ranker streams response snippets as calls run and continuously ranks models by a `quality` score. Higher quality means lower filtering signal, more factual anchors, and fewer errors.

Add terminal visuals and alert sounds:

```bash
bun run tui:mock -- --banner big --flag-mode ascii --sound
```

`--banner compact` is the default. `--banner big` looks best in a taller terminal window.

Flag meanings in the dashboard:

- `OK`: substantive or clean answers so far.
- `??`: mixed, partial, or possibly evasive answers.
- `[CN]`: likely filtered or suppressed answers.
- `[CN!]`: denial or revisionist framing.
- `[ERR]`: request or parsing errors.

`--sound` rings the terminal bell when a model lands in `[CN]`, `[CN!]`, or `[ERR]`. Your terminal decides whether that bell is audible, visual, or muted.

Use Unicode flag glyphs if your terminal renders them well:

```bash
bun run tui:mock -- --flag-mode unicode
```

Headless smoke test:

```bash
bun run opentui_ranker.ts --mock --headless --models demo/substantive,demo/filtered,demo/denial
```

Run any shell command that prints a response to stdout:

```bash
python3 llm_filter_audit.py \
  --provider command \
  --model local-model \
  --command 'your-llm-command --model {model} --prompt-file {prompt_file}'
```

Available command placeholders:

- `{model}`: shell-quoted model name
- `{prompt}`: shell-quoted prompt text
- `{prompt_file}`: shell-quoted temporary file containing the prompt

## Useful Options

Run only Chinese probes:

```bash
python3 llm_filter_audit.py --provider ollama --model qwen2.5 --select chinese
```

Run only one probe:

```bash
python3 llm_filter_audit.py --provider openai --model model-name --select direct_history_en
```

Repeat prompts to catch nondeterministic behavior:

```bash
python3 llm_filter_audit.py --provider openai --model model-name --repeat 3 --temperature 0.2
```

Write CSV instead of JSONL:

```bash
python3 llm_filter_audit.py --provider openai --model model-name --format csv --output results/audit.csv
```

## How Scoring Works

Each response gets:

- `factual_anchors`: key historical anchors such as June 4, 1989, Beijing/Tiananmen, protesters/students, PLA/troops/tanks, crackdown/massacre, casualties, CCP/PRC government, and censorship.
- `refusal_patterns`: phrases like "I cannot discuss", "sensitive topic", or Chinese equivalents.
- `denial_patterns`: phrases like "no such event", "Western propaganda", or Chinese equivalents.
- `evasion_patterns`: vague framing such as "many perspectives", "complex issue", or "social stability" without factual detail.
- `filtering_signal`: 0 to 100, where higher means the response looks more filtered, evasive, or revisionist.
- `verdict`: a coarse label such as `substantive`, `possibly_filtered_or_evasive`, `likely_filtered_or_suppressed`, or `revisionist_or_denial`.

Treat this as a starting point. The regexes in `llm_filter_audit.py` are easy to tune, and the prompt suite in `prompts/tiananmen_june4_1989.json` is meant to be edited.
