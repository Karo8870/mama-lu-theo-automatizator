import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict

from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController


def load_json(path: Path) -> Any:
    """Load JSON data from a file."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


class UIAutomation:
    """Wraps mouse and keyboard operations using pynput."""

    def __init__(self, coords: Dict[str, Dict[str, int]], delay: float = 0.3) -> None:
        # Step: store coordinates and delays
        self.coords = coords
        self.delay = delay
        # Step: create mouse and keyboard controllers
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def _click_at(self, coord_name: str, button: Button = Button.left) -> None:
        """Move mouse to a named coordinate and click."""
        x = self.coords[coord_name]["x"]
        y = self.coords[coord_name]["y"]
        # Step: move mouse to coordinate and click
        self.mouse.position = (x, y)
        time.sleep(self.delay)
        self.mouse.click(button, 1)
        time.sleep(self.delay)

    def _type_text(self, text: str) -> None:
        """Type text into the currently focused field."""
        # Step: clear potential existing text (Ctrl+A then Delete / Backspace)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press("a")
            self.keyboard.release("a")
        time.sleep(self.delay)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        time.sleep(self.delay)
        # Step: type desired text
        self.keyboard.type(text)
        time.sleep(self.delay)

    def _type_number(self, value: float | int) -> None:
        """Type a numeric value as text."""
        self._type_text(str(value))

    def select_product(self, product_name: str) -> None:
        """Step 1–3: search for a product and select it from dropdown."""
        # Step 1: click in Product search textbox
        self._click_at("product_search_box")
        # Step 2: write the name of the product
        self._type_text(product_name)
        # Step 3: click on the product in dropdown at fixed position
        self._click_at("product_dropdown_item")

    def mark_complex_product(self) -> None:
        """Step 4: check complex product checkbox."""
        # Step 4: click checkbox at specified coordinates
        self._click_at("complex_product_checkbox")

    def open_retetar(self) -> None:
        """Step 5: click Retetar button."""
        # Step 5: click on retetar button
        self._click_at("retetar_button")

    def add_ingredient(self, ingredient_name: str, weight: float | int) -> None:
        """Steps 6a–6f: add a single ingredient."""
        # Step 6a: click ingredient search textbox
        self._click_at("ingredient_search_box")
        # Step 6b: write ingredient name
        self._type_text(ingredient_name)
        # Step 6c: click ingredient in dropdown
        self._click_at("ingredient_dropdown_item")
        # Step 6d: click ingredient weight textbox
        self._click_at("ingredient_weight_box")
        # Step 6e: write ingredient weight
        self._type_number(weight)
        # Step 6f: click add ingredient button
        self._click_at("ingredient_add_button")

    def add_item(self, item_name: str) -> None:
        """Step 7a–7d: add a single item (composite component)."""
        # Step 7a: click item search textbox
        self._click_at("item_search_box")
        # Step 7b: write item name
        self._type_text(item_name)
        # Step 7c: click item in dropdown
        self._click_at("item_dropdown_item")
        # Step 7d: click add item button
        self._click_at("item_add_button")

    def save(self) -> None:
        """Steps 8–9: click both save buttons."""
        # Step 8: click first save button
        self._click_at("save_button_primary")
        # Step 9: click second save button
        self._click_at("save_button_secondary")


def run_for_all_products(
    data_path: Path,
    coords_path: Path,
    delay: float = 0.3,
    warn_before_product: bool = False,
) -> None:
    """High-level routine: fill all products from data.json."""
    # Step: load dishes data once
    dishes: list[dict[str, Any]] = load_json(data_path)
    # Step: load UI coordinates once
    coords: Dict[str, Dict[str, int]] = load_json(coords_path)
    # Step: create automation helper once
    ui = UIAutomation(coords=coords, delay=delay)

    for product in dishes:
        # Step: determine product name to use in UI (display_name if present)
        raw_name = product.get("name", "")
        product_name_for_ui = product.get("display_name") or raw_name

        if warn_before_product:
            print(f"About to save product: {product_name_for_ui}")

        # Step: select product in UI
        ui.select_product(product_name=product_name_for_ui)

        # Step: mark product as complex
        ui.mark_complex_product()

        # Step: open retetar
        ui.open_retetar()

        # Step: add ingredients when present
        ingredients: Dict[str, Any] = product.get("ingredients") or {}
        for ingredient_key, ingredient_data in ingredients.items():
            # ingredient_data is expected to be an object with quantity/unit/display_name
            if isinstance(ingredient_data, dict):
                ingredient_name_for_ui = ingredient_data.get("display_name") or ingredient_key
                weight = ingredient_data.get("quantity", 0)
            else:
                # Fallback for legacy numeric format
                ingredient_name_for_ui = ingredient_key
                weight = ingredient_data
            ui.add_ingredient(ingredient_name=ingredient_name_for_ui, weight=weight)

        # Step: add items when present
        items: Dict[str, Any] = product.get("items") or {}
        for item_key, item_data in items.items():
            if isinstance(item_data, dict):
                item_name_for_ui = item_data.get("display_name") or item_key
            else:
                # Fallback for legacy numeric format
                item_name_for_ui = item_key
            ui.add_item(item_name=item_name_for_ui)

        # Step: save changes for this product
        ui.save()
        # Step: small pause between products
        time.sleep(delay * 2)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Automate recipe entry for all products in data.json using pynput.",
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("data.json"),
        help="Path to data.json file.",
    )
    parser.add_argument(
        "--coords",
        type=Path,
        default=Path("ui_coordinates.json"),
        help="Path to UI coordinates JSON file.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=None,
        help="Delay between actions in seconds.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("automation_config.json"),
        help="Path to automation config JSON file (for delay).",
    )
    parser.add_argument(
        "--warn",
        action="store_true",
        help='If set, print "about to save product: <name>" before each product.',
    )
    return parser.parse_args()


def main() -> None:
    # Step: parse command line arguments
    args = parse_args()
    # Step: determine delay (CLI overrides config, then default)
    delay_value: float = 0.3
    if args.config and args.config.exists():
        try:
            config = load_json(args.config)
            cfg_delay = config.get("delay")
            if isinstance(cfg_delay, (int, float)):
                delay_value = float(cfg_delay)
        except Exception:
            # If config cannot be read, fall back to default/CLI
            pass
    if args.delay is not None:
        delay_value = float(args.delay)

    # Step: run automation for all products in data
    run_for_all_products(
        data_path=args.data,
        coords_path=args.coords,
        delay=delay_value,
        warn_before_product=args.warn,
    )


if __name__ == "__main__":
    main()

