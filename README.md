# Obsidian Plugin Sync

A command-line tool for syncing Obsidian plugin development files to your Obsidian vault.

## Features

- Syncs your plugin's development files to your Obsidian vault with a single command
- Automatically detects plugin ID from manifest.json
- Optional build step before syncing
- Watch mode for automatic syncing on file changes
- No dependencies for basic functionality (watch mode requires the `watchdog` package)

## Installation

### Option 1: Clone and use directly

```bash
git clone https://github.com/wrale/obsidian-plugin-sync.git
cd obsidian-plugin-sync
chmod +x obsidian-plugin-sync.py
```

### Option 2: Install to ~/bin

```bash
curl -o ~/bin/obsidian-plugin-sync.py https://raw.githubusercontent.com/wrale/obsidian-plugin-sync/main/obsidian-plugin-sync.py
chmod +x ~/bin/obsidian-plugin-sync.py
```

## Usage

### Basic Usage

```bash
./obsidian-plugin-sync.py --source /path/to/plugin/dev --vault /path/to/vault
```

### Build Before Syncing

```bash
./obsidian-plugin-sync.py --source /path/to/plugin/dev --vault /path/to/vault --build
```

### Specify Plugin ID Manually

```bash
./obsidian-plugin-sync.py --source /path/to/plugin/dev --vault /path/to/vault --plugin-id your-plugin-id
```

### Watch for Changes

First, install the watchdog package:

```bash
pip install watchdog
```

Then run with the `--watch` flag:

```bash
./obsidian-plugin-sync.py --source /path/to/plugin/dev --vault /path/to/vault --build --watch
```

This will continuously watch for changes in your plugin files and automatically sync them to your Obsidian vault.

## How It Works

The tool performs the following steps:

1. Reads the plugin ID from manifest.json (or uses the one provided)
2. Optionally builds the plugin using `npm run build`
3. Copies the necessary files (main.js, manifest.json, styles.css) to your Obsidian vault's plugins directory
4. In watch mode, it continuously monitors for changes and repeats steps 2-3 when files are modified

## Benefits Over Manual File Copying

- **Time-saving**: No need to manually navigate directories and copy files
- **Consistency**: Always copies all required files
- **Automation**: Combined build and copy process
- **Continuous development**: Watch mode makes the development cycle faster

## Requirements

- Python 3.6 or higher
- For watch mode: `watchdog` package

## License

MIT
