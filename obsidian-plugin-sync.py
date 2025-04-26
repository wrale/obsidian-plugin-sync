#!/usr/bin/env python3
"""
Obsidian Plugin Sync Tool

This script helps sync plugin files from a development directory to an Obsidian vault.
Usage:
    obsidian-plugin-sync.py --source /path/to/plugin/dev --vault /path/to/vault [--plugin-id plugin-id] [--build]
"""

import argparse
import json
import os
import shutil
import subprocess
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Sync Obsidian plugin development files to a vault")
    parser.add_argument("--source", required=True, help="Source directory of the plugin development")
    parser.add_argument("--vault", required=True, help="Target Obsidian vault directory")
    parser.add_argument("--plugin-id", help="Plugin ID (will read from manifest.json if not provided)")
    parser.add_argument("--build", action="store_true", help="Run npm build before syncing")
    parser.add_argument("--watch", action="store_true", help="Watch for changes and auto-sync (requires watchdog package)")
    return parser.parse_args()


def get_plugin_id(source_dir):
    """Get plugin ID from manifest.json"""
    manifest_path = os.path.join(source_dir, "manifest.json")
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
            return manifest.get("id")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading manifest.json: {e}")
        return None


def build_plugin(source_dir):
    """Run npm build in the source directory"""
    print("Building plugin...")
    try:
        # Use subprocess.run with shell=True to handle npm commands
        result = subprocess.run(
            "npm run build",
            shell=True,
            cwd=source_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Build failed with error: {result.stderr}")
            return False
        
        print("Build successful!")
        return True
    except Exception as e:
        print(f"Error running build: {e}")
        return False


def sync_files(source_dir, target_dir):
    """Copy necessary files from source to target"""
    files_to_copy = ["main.js", "manifest.json", "styles.css"]
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    copied_files = []
    for file in files_to_copy:
        source_file = os.path.join(source_dir, file)
        if os.path.exists(source_file):
            try:
                shutil.copy2(source_file, target_dir)
                copied_files.append(file)
            except Exception as e:
                print(f"Error copying {file}: {e}")
    
    return copied_files


def watch_for_changes(source_dir, target_dir, build=False):
    """Watch for file changes and sync automatically"""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("Watchdog package is required for file watching. Install with 'pip install watchdog'.")
        return

    class ChangeHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.is_directory:
                return
            
            filename = os.path.basename(event.src_path)
            # Only sync if the file is one we care about
            if filename in ["main.js", "styles.css", "manifest.json"] or event.src_path.endswith(".ts"):
                print(f"Change detected in {filename}")
                if build and (filename.endswith(".ts") or filename == "manifest.json"):
                    build_plugin(source_dir)
                
                copied = sync_files(source_dir, target_dir)
                if copied:
                    print(f"Synced files: {', '.join(copied)}")
                    print(f"Sync completed at {time.strftime('%H:%M:%S')}")
                    print("---")

    import time
    print(f"Watching for changes in {source_dir}")
    print("Press Ctrl+C to stop")
    print("---")
    
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    args = parse_args()
    source_dir = os.path.abspath(args.source)
    vault_dir = os.path.abspath(args.vault)
    
    # Verify source directory exists
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory {source_dir} does not exist.")
        sys.exit(1)
    
    # Verify vault directory exists
    if not os.path.isdir(vault_dir):
        print(f"Error: Vault directory {vault_dir} does not exist.")
        sys.exit(1)
    
    # Get plugin ID
    plugin_id = args.plugin_id or get_plugin_id(source_dir)
    if not plugin_id:
        print("Error: Could not determine plugin ID. Please provide it with --plugin-id.")
        sys.exit(1)
    
    # Build if requested
    if args.build:
        if not build_plugin(source_dir):
            sys.exit(1)
    
    # Determine target directory
    plugins_dir = os.path.join(vault_dir, ".obsidian", "plugins")
    target_dir = os.path.join(plugins_dir, plugin_id)
    
    if args.watch:
        watch_for_changes(source_dir, target_dir, args.build)
    else:
        # Sync files
        copied_files = sync_files(source_dir, target_dir)
        
        if copied_files:
            print(f"Successfully copied {', '.join(copied_files)} to {target_dir}")
            print("Plugin sync complete! Please reload or enable the plugin in Obsidian.")
        else:
            print("No files were copied. Please ensure the required files exist in the source directory.")


if __name__ == "__main__":
    main()
