"""
Holiday Panic Factory - Asset Folder Creator
Run this script to automatically create the asset directory structure.

Usage:
    python create_asset_folders.py
"""

import os

def create_asset_structure():
    """Create all necessary asset directories"""

    # Base assets directory
    base_dir = "assets"

    # Define directory structure
    directories = [
        "assets",
        "assets/backgrounds",
        "assets/characters",
        "assets/toys",
        "assets/wrapping",
        "assets/bows",
        "assets/sounds",
        "assets/sounds/music",
        "assets/sounds/sfx",
        "assets/ui",
        "assets/ui/icons",
    ]

    print("Creating asset directory structure...")
    print("=" * 50)

    created_count = 0
    skipped_count = 0

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created: {directory}")
            created_count += 1
        else:
            print(f"  Skipped: {directory} (already exists)")
            skipped_count += 1

    print("=" * 50)
    print(f"\nSummary:")
    print(f"  Created: {created_count} folders")
    print(f"  Skipped: {skipped_count} folders (already existed)")
    print(f"\nAsset structure is ready!")
    print(f"\nNext steps:")
    print(f"  1. Place your sprite files in the appropriate folders")
    print(f"  2. See ASSET_ORGANIZATION.md for file name requirements")
    print(f"  3. Run the game: python main.py")

    # Create a helpful README in the assets folder
    readme_path = os.path.join(base_dir, "README.txt")
    if not os.path.exists(readme_path):
        with open(readme_path, 'w') as f:
            f.write("Holiday Panic Factory - Asset Directory\n")
            f.write("=" * 50 + "\n\n")
            f.write("Place your game assets in the appropriate folders:\n\n")
            f.write("backgrounds/  - Background images (1280x720 PNG)\n")
            f.write("characters/   - Character sprites (elf head, etc.)\n")
            f.write("toys/         - Toy sprites (good/bad variants)\n")
            f.write("wrapping/     - Wrapping paper sprites\n")
            f.write("bows/         - Bow/ribbon sprites\n")
            f.write("sounds/music/ - Background music (.ogg files)\n")
            f.write("sounds/sfx/   - Sound effects (.wav files)\n")
            f.write("ui/           - UI elements and icons\n\n")
            f.write("See ../ASSET_ORGANIZATION.md for detailed requirements.\n")
        print(f"\n✓ Created: {readme_path}")


if __name__ == "__main__":
    try:
        create_asset_structure()
    except Exception as e:
        print(f"\nError creating folders: {e}")
        print("Please check your permissions and try again.")
