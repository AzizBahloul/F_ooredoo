#build.sh
 
set -e  # Exit on error

echo "========================================"
echo "F_ooredoo Package Build Script"
echo "Version 1.0.0"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "setup.py" ] || [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: setup.py or pyproject.toml not found!${NC}"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Step 1: Clean previous builds
echo -e "${YELLOW}Step 1: Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.egg-info fuckooredoo.egg-info
echo -e "${GREEN}✓ Clean complete${NC}"
echo ""

# Step 2: Install/upgrade build tools
echo -e "${YELLOW}Step 2: Installing/upgrading build tools...${NC}"
pip install --upgrade pip setuptools wheel twine build
echo -e "${GREEN}✓ Build tools ready${NC}"
echo ""

# Step 3: Build the package
echo -e "${YELLOW}Step 3: Building distribution packages...${NC}"
python -m build
echo -e "${GREEN}✓ Build complete${NC}"
echo ""

# Step 4: Verify the packages
echo -e "${YELLOW}Step 4: Verifying packages...${NC}"
python -m twine check dist/*
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Package verification passed${NC}"
else
    echo -e "${RED}✗ Package verification failed${NC}"
    exit 1
fi
echo ""

# Display results
echo "========================================"
echo -e "${GREEN}Build Successful!${NC}"
echo "========================================"
echo ""
echo "Generated files:"
ls -lh dist/
echo ""
echo "Next steps:"
echo "  1. Test on Test PyPI:"
echo "     python -m twine upload --repository testpypi dist/*"
echo ""
echo "  2. Publish to Production PyPI:"
echo "     python -m twine upload dist/*"
echo ""
echo "See PUBLISHING.md for detailed instructions."
