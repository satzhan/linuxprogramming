#!/usr/bin/env bash
# ==============================================================================
#  FINAL PROJECT SETUP SCRIPT
#  Run this ONCE at the start of the project.
#  It will create the folder structure you'll use for the whole project.
# ==============================================================================
#
#  HOW TO RUN THIS FILE:
#    1. Save this file as setup.sh in your home directory.
#    2. Open a terminal.
#    3. Type:     bash setup.sh
#    4. Press Enter.
#
#  After it runs, you will have a new folder called "mydaemon" with everything
#  you need to start Part 1.
# ==============================================================================

set -e  # stop the script if any command fails

echo "Setting up your mydaemon project..."

# Create the project folder and subfolders.
# This is your "fake FHS" (Filesystem Hierarchy Standard) tree --
# a miniature version of how real Linux systems organize daemons.
mkdir -p mydaemon/bin
mkdir -p mydaemon/etc
mkdir -p mydaemon/var/run
mkdir -p mydaemon/var/log
mkdir -p mydaemon/watched

# Create empty Python files that you'll fill in later.
touch mydaemon/bin/mydaemon.py
touch mydaemon/bin/mydaemonctl.py

# Create a simple config file.
cat > mydaemon/etc/mydaemon.conf << 'EOF'
# mydaemon configuration
# (you don't need to change this for the project)
CHECK_INTERVAL_SECONDS=5
EOF

# Create the empty log file so students don't hit "file not found" errors.
touch mydaemon/var/log/mydaemon.log

# Create a placeholder REPORT.md for Part 6.
cat > mydaemon/REPORT.md << 'EOF'
# My Daemon Project - Reflection Report

(You will fill this in during Part 6.)
EOF

echo ""
echo "Done! Your project folder is ready."
echo ""
echo "Your folder now looks like this:"
echo ""
echo "  mydaemon/"
echo "  |-- bin/"
echo "  |   |-- mydaemon.py        (empty - you will fill this in)"
echo "  |   |-- mydaemonctl.py     (empty - you will fill this in)"
echo "  |-- etc/"
echo "  |   |-- mydaemon.conf      (small config file)"
echo "  |-- var/"
echo "  |   |-- run/               (PID file will live here)"
echo "  |   |-- log/"
echo "  |       |-- mydaemon.log   (empty log file)"
echo "  |-- watched/               (the folder your daemon will watch)"
echo "  |-- REPORT.md              (your written reflection)"
echo ""
echo "Next step: open the handout and begin Part 1."
echo ""
