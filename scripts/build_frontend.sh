#!/bin/bash
# Proper Angular build script to prevent file name mismatches

set -e  # Exit on any error

echo "🔨 Building Angular Frontend"
echo "=" * 40

# Navigate to Angular project
cd app/frontend-dev

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/
rm -rf ../frontend-built/*

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build Angular project
echo "🏗️  Building Angular project..."
npm run build

# Verify build succeeded
if [ ! -d "dist/aoc-map/browser" ]; then
    echo "❌ Angular build failed - dist directory not found"
    exit 1
fi

# Copy built files to frontend-built
echo "📦 Copying built files..."
cp -r dist/aoc-map/browser/* ../frontend-built/

# Verify consistency
echo "🔍 Verifying build consistency..."
cd ../frontend-built

# Check that referenced files actually exist
MAIN_JS=$(grep -o 'main-[^"]*\.js' index.html | head -1)
POLYFILLS_JS=$(grep -o 'polyfills-[^"]*\.js' index.html | head -1)
STYLES_CSS=$(grep -o 'styles-[^"]*\.css' index.html | head -1)

echo "📋 Checking file references:"
echo "  - $MAIN_JS: $([ -f "$MAIN_JS" ] && echo "✅ EXISTS" || echo "❌ MISSING")"
echo "  - $POLYFILLS_JS: $([ -f "$POLYFILLS_JS" ] && echo "✅ EXISTS" || echo "❌ MISSING")"  
echo "  - $STYLES_CSS: $([ -f "$STYLES_CSS" ] && echo "✅ EXISTS" || echo "❌ MISSING")"

# Fail if any referenced file is missing
if [ ! -f "$MAIN_JS" ] || [ ! -f "$POLYFILLS_JS" ] || [ ! -f "$STYLES_CSS" ]; then
    echo "❌ Build consistency check failed!"
    exit 1
fi

echo "✅ Frontend build completed successfully!"
echo "📁 Output: app/frontend-built/"
echo "🔗 Files and references are consistent"
