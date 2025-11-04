#!/bin/bash

# Build macOS .app bundle with PyInstaller
echo "🔨 Building macOS application..."

# Clean previous builds
rm -rf build dist

# Build the app using the spec file
/Users/adithkrishnan/Desktop/fee-automate/.venv/bin/pyinstaller fee_tracker.spec --clean --noconfirm

# Check if build was successful
if [ -d "dist/FeeTracker.app" ]; then
    echo "✅ Application built successfully!"
    echo "📦 Location: dist/FeeTracker.app"
    echo ""
    echo "You can now:"
    echo "  1. Run it directly: open dist/FeeTracker.app"
    echo "  2. Create a DMG installer with: ./create_dmg.sh"
    echo "  3. Move it to /Applications folder"
else
    echo "❌ Build failed. Check the output above for errors."
    exit 1
fi
