#!/bin/bash

echo "===== Creating virtual environment and providing instructions ====="

echo "IMPORTANT: Your Python installation is missing the '_ctypes' module, which is needed for Flask."
echo "To fix this issue, you need to:"
echo ""
echo "1. Install the required dependencies:"
echo "   - Install Homebrew (if not already installed):"
echo '     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
echo "   - Install libffi:"
echo "     brew install libffi"
echo ""
echo "2. Reinstall Python with _ctypes support:"
echo "   - Install pyenv:"
echo "     brew install pyenv"
echo "   - Add pyenv to your shell profile:"
echo '     echo '\''export PYENV_ROOT="$HOME/.pyenv"'\'' >> ~/.zshrc'
echo '     echo '\''export PATH="$PYENV_ROOT/bin:$PATH"'\'' >> ~/.zshrc'
echo '     echo '\''eval "$(pyenv init --path)"'\'' >> ~/.zshrc'
echo '     echo '\''eval "$(pyenv init -)"'\'' >> ~/.zshrc'
echo "   - Restart your terminal or run:"
echo "     source ~/.zshrc"
echo "   - Set environment variables for libffi:"
echo '     export LDFLAGS="-L/usr/local/opt/libffi/lib"'
echo '     export CPPFLAGS="-I/usr/local/opt/libffi/include"'
echo '     export PKG_CONFIG_PATH="/usr/local/opt/libffi/lib/pkgconfig"'
echo "   - Install Python 3.10 with pyenv:"
echo "     pyenv install 3.10.0"
echo "   - Set Python 3.10 as your local version:"
echo "     pyenv local 3.10.0"
echo ""
echo "3. Create a virtual environment with the fixed Python:"
echo "   python -m venv recommonder"
echo "   source recommonder/bin/activate"
echo "   pip install --upgrade pip"
echo "   pip install flask"
echo ""
echo "Would you like to proceed with creating a virtual environment using the current Python?"
echo "Note: Flask installation may fail due to the missing _ctypes module."
read -p "Proceed? (y/n): " proceed

if [[ $proceed != "y" && $proceed != "Y" ]]; then
    echo "Exiting. Please follow the instructions above to fix your Python installation."
    exit 0
fi

# Remove existing virtual environment if it exists
if [ -d "recommonder" ]; then
    echo "Removing existing recommonder virtual environment"
    rm -rf recommonder
fi

# Create a new virtual environment named "recommonder"
echo "Creating new virtual environment with python3"
python3 -m venv recommonder

# Activate the virtual environment
echo "Activating virtual environment"
source recommonder/bin/activate

# Upgrade pip
echo "Upgrading pip"
python -m pip install --upgrade pip

echo "===== Setup Complete ====="
echo "Virtual environment 'recommonder' is ready to use"
echo "To activate it manually, run: source recommonder/bin/activate"
echo "To deactivate it, run: deactivate"
echo ""
echo "To install Flask, you may need to fix the _ctypes issue first."
echo "Try running: pip install flask"