Convert the file to this template. For Primary materials such as meat or potatoes, use ingredients. for sub items such as crispy or falafel, use items.

```js
{
  "name": "Dish Name",
  "weight_g": 0,                  // Total weight of the dish (null if composite with multiple items)
  "price_ron": 0,                 // Price in RON
  "ingredients": {                // For single dishes
    "ingredient_1_g": 0,
    "ingredient_2_g": 0,
    "ou_buc": 0,                  // Example for countable items like eggs
    "optional_ingredient_g": 0    // Include only if present
  },
  "items": {                      // For composite dishes like platou or menus (optional)
    "subitem_1_buc": 0,
    "subitem_2_g": 0
    // Include all components of the platou/menu
  },
  "nutrition": {                  // Total nutrition per portion or per platou
    "kcal": 0,
    "proteine_g": 0,
    "grasimi_g": 0,
    "carbohidrati_g": 0
  },
  "allergens": [                  // Include all allergens, use "posibil" for uncertain
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