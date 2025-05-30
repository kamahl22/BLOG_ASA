# Diagnostic script for PyTeal installation
import sys
import os

print("Python path:")
for path in sys.path:
    print(f"  {path}")

print("\nTrying to import pyteal...")
try:
    import pyteal
    print(f"✓ PyTeal imported from: {pyteal.__file__}")
    print(f"✓ PyTeal directory contents:")
    pyteal_dir = os.path.dirname(pyteal.__file__)
    for item in os.listdir(pyteal_dir):
        print(f"    {item}")
except ImportError as e:
    print(f"✗ Failed to import pyteal: {e}")

print("\nChecking for local pyteal directory...")
if os.path.exists("pyteal"):
    print("⚠️  WARNING: Found local 'pyteal' directory - this might be causing conflicts!")
    print("Contents:")
    for item in os.listdir("pyteal"):
        print(f"    {item}")
else:
    print("✓ No local pyteal directory found")

print("\nTrying specific imports...")
try:
    from pyteal import compileTeal
    print("✓ compileTeal imported successfully")
except ImportError as e:
    print(f"✗ Failed to import compileTeal: {e}")

try:
    from pyteal import Mode
    print("✓ Mode imported successfully")
except ImportError as e:
    print(f"✗ Failed to import Mode: {e}")

# Try alternative import methods
print("\nTrying alternative imports...")
try:
    import pyteal.compiler
    print("✓ pyteal.compiler module exists")
except ImportError:
    print("✗ pyteal.compiler not found")

try:
    from pyteal.compiler import compileTeal, Mode
    print("✓ compileTeal and Mode imported from pyteal.compiler")
except ImportError as e:
    print(f"✗ Failed to import from pyteal.compiler: {e}")

try:
    from pyteal.ast import *
    from pyteal.compiler import *
    print("✓ Imported from pyteal.ast and pyteal.compiler")
except ImportError as e:
    print(f"✗ Failed to import from submodules: {e}")