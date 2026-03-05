from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

from pynput import mouse, keyboard


UI_COORDS_PATH = Path("ui_coordinates.json")

# Ordered list of coordinates we want to capture, with human descriptions
COORDINATE_ORDER: List[Tuple[str, str]] = [
    ("product_search_box", "click inside the Product search textbox"),
    ("product_dropdown_item", "click the product entry in the dropdown"),
    ("complex_product_checkbox", "click the Complex product checkbox"),
    ("retetar_button", "click the Retetar button"),
    ("ingredient_search_box", "click inside the Ingredient search textbox"),
    ("ingredient_dropdown_item", "click the ingredient entry in the dropdown"),
    ("ingredient_weight_box", "click inside the Ingredient weight textbox"),
    ("ingredient_add_button", "click the Add ingredient button"),
    ("item_search_box", "click inside the Item search textbox"),
    ("item_dropdown_item", "click the item entry in the dropdown"),
    ("item_add_button", "click the Add item button"),
    ("save_button_primary", "click the first Save button"),
    ("save_button_secondary", "click the second Save button"),
]


def capture_single_coordinate(name: str, description: str) -> Dict[str, int]:
    """Capture one (x, y) coordinate for a named UI element."""
    print(f"\nNext position: {name} – {description}")
    print("  Press 'r' to arm recording for this position, or 's' to skip.")

    armed = False
    coord: Dict[str, int] = {}

    def on_key_press(key: keyboard.Key | keyboard.KeyCode):
        nonlocal armed
        try:
            if key == keyboard.Key.esc:
                print("Esc pressed, aborting coordinate capture for all positions.")
                # Stop both mouse and keyboard listeners by raising KeyboardInterrupt-style signal
                raise SystemExit(0)
            if hasattr(key, "char") and key.char == "r":
                armed = True
                print(f"Listening for {name}: {description}")
                print("  → Perform ONE click on the target UI element.")
                return False
            if hasattr(key, "char") and key.char == "s":
                print(f"Skipped {name}.")
                coord["x"] = -1
                coord["y"] = -1
                return False
        except SystemExit:
            raise
        except Exception:
            return False
        return None

    # Wait for 'r' (record) or 's' (skip)
    with keyboard.Listener(on_press=on_key_press) as key_listener:
        key_listener.join()

    # If skipped, return the placeholder coord
    if not armed and coord:
        return coord

    def on_click(x: int, y: int, button: mouse.Button, pressed: bool):
        if pressed:
            coord["x"] = x
            coord["y"] = y
            print(f"Captured {name}: (x={x}, y={y})")
            # Stop listener after first click
            return False
        return None

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    return coord


def main() -> None:
    print("UI coordinate setup helper")
    print("This will guide you through each UI element and write ui_coordinates.json.")
    print("Make sure the target application window is visible and focused.")
    print("Use keys: 'r' = record next click, 's' = skip, Esc = abort.\n")

    result: Dict[str, Dict[str, int]] = {}

    for name, description in COORDINATE_ORDER:
        coord = capture_single_coordinate(name, description)
        result[name] = coord

    # Write to ui_coordinates.json
    UI_COORDS_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("\nAll coordinates captured.")
    print(f"Configuration written to: {UI_COORDS_PATH.resolve()}")


if __name__ == "__main__":
    main()


