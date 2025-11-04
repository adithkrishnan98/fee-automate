#!/bin/bash

# Create a DMG installer for the macOS app
echo "📀 Creating DMG installer..."

# Check if the app exists
if [ ! -d "dist/FeeTracker.app" ]; then
    echo "❌ FeeTracker.app not found. Run ./build_app.sh first."
    exit 1
fi

# Create a temporary directory for the DMG contents
DMG_DIR="dist/dmg_temp"
rm -rf "$DMG_DIR"
mkdir -p "$DMG_DIR"

# Copy the app to the temp directory
cp -R "dist/FeeTracker.app" "$DMG_DIR/"

# Create a symbolic link to Applications folder
ln -s /Applications "$DMG_DIR/Applications"

# Create the DMG
DMG_NAME="FeeTracker-1.0.0.dmg"
rm -f "dist/$DMG_NAME"

echo "Creating DMG file..."
hdiutil create -volname "Fee Tracker" \
    -srcfolder "$DMG_DIR" \
    -ov -format UDZO \
    "dist/$DMG_NAME"

# Clean up
rm -rf "$DMG_DIR"

if [ -f "dist/$DMG_NAME" ]; then
    echo "✅ DMG created successfully!"
    echo "📦 Location: dist/$DMG_NAME"
    echo ""
    echo "You can now:"
    echo "  1. Double-click the DMG to mount it"
    echo "  2. Drag FeeTracker.app to the Applications folder"
    echo "  3. Distribute the DMG file"
else
    echo "❌ DMG creation failed."
    exit 1
fi
