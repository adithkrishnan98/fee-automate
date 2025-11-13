#!/bin/bash

# Quick Build and Package Script for Fee Tracker
# This script builds the app and creates a DMG installer in one command

echo "🚀 Fee Tracker - Quick Build & Package"
echo "======================================"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is for macOS only."
    echo "For Windows builds, see build_windows.bat"
    exit 1
fi

# Step 1: Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Step 2: Build the .app bundle
echo ""
echo "🔨 Building macOS application..."
/Users/adithkrishnan/Desktop/fee-automate/.venv/bin/pyinstaller fee_tracker.spec --clean --noconfirm

# Check if build was successful
if [ ! -d "dist/FeeTracker.app" ]; then
    echo ""
    echo "❌ Build failed. Check the output above for errors."
    exit 1
fi

echo "✅ Application built successfully!"

# Step 3: Create DMG installer
echo ""
echo "📀 Creating DMG installer..."

# Create a temporary directory for the DMG contents
DMG_DIR="dist/dmg_temp"
rm -rf "$DMG_DIR"
mkdir -p "$DMG_DIR"

# Copy the app to the temp directory
cp -R "dist/FeeTracker.app" "$DMG_DIR/"

# Create a symbolic link to Applications folder
ln -s /Applications "$DMG_DIR/Applications"

# Get version from spec file or use default
VERSION="1.0.0"

# Create the DMG
DMG_NAME="FeeTracker-${VERSION}-macOS.dmg"
rm -f "dist/$DMG_NAME"

hdiutil create -volname "Fee Tracker" \
    -srcfolder "$DMG_DIR" \
    -ov -format UDZO \
    "dist/$DMG_NAME"

# Clean up temp directory
rm -rf "$DMG_DIR"

# Final summary
echo ""
echo "======================================"
echo "✅ BUILD COMPLETE!"
echo "======================================"
echo ""
echo "📦 Outputs:"
echo "   • Application: dist/FeeTracker.app"
echo "   • DMG Installer: dist/$DMG_NAME"
echo ""
echo "📊 File sizes:"
ls -lh dist/FeeTracker.app | awk '{print "   • .app bundle: " $5}'
ls -lh "dist/$DMG_NAME" | awk '{print "   • DMG file: " $5}'
echo ""
echo "🎯 Next steps:"
echo "   1. Test: open dist/FeeTracker.app"
echo "   2. Distribute: dist/$DMG_NAME"
echo ""
