Convert the file to this template. For primary materials such as meat or potatoes, use `ingredients`. For sub items such as crispy or falafel, use `items`.

```js
{
  // Recipe name used as the primary identifier.
  "name": "Dish Name",

  // Optional explicit display name for the dish in the UI.
  // If omitted, it is derived from `name` by:
  //   - replacing underscores with spaces
  //   - removing unit suffixes like `_g`, `_ml`, `_buc`
  //   - converting to lowercase
  "display_name": "dish name",

  // Total weight of the dish (null if composite with multiple items)
  "weight_g": 0,

  // Price in RON
  "price_ron": 0,

  // For single dishes: map of ingredient keys to objects.
  // Keys are pure logical names WITHOUT unit suffixes.
  "ingredients": {
    "ingredient_1": {
      // Optional explicit display name for the ingredient.
      // If omitted, derived from the key by:
      //   - replacing underscores with spaces
      //   - converting to lowercase
      "display_name": "ingredient 1",

      // Unit of measure without quantity (e.g. "g", "ml", "buc").
      "unit": "g",

      // Numeric quantity in the given unit.
      "quantity": 0
    },
    "ingredient_2": {
      "display_name": "ingredient 2",
      "unit": "g",
      "quantity": 0
    },
    "ou": {
      "display_name": "ou",
      "unit": "buc",
      "quantity": 0
    },
    // Include only ingredients that are present
    "optional_ingredient": {
      "display_name": "optional ingredient",
      "unit": "g",
      "quantity": 0
    }
  },

  // For composite dishes like platou or menus (optional).
  // Same structure as `ingredients`, but semantically "items" are sub-recipes.
  "items": {
    "subitem_1": {
      "display_name": "subitem 1",
      "unit": "buc",
      "quantity": 0
    },
    "subitem_2": {
      "display_name": "subitem 2",
      "unit": "g",
      "quantity": 0
    }
    // Include all components of the platou/menu
  },

  // Total nutrition per portion or per platou
  "nutrition": {
    "kcal": 0,
    "proteine_g": 0,
    "grasimi_g": 0,
    "carbohidrati_g": 0
  },

  // Include all allergens, use "posibil" for uncertain
  "allergens": [
    "gluten",
    "ou",
    "lapte",
    "mustar",
    "soia",
    "posibil telina",
    "posibil susan"
  ]
}
```