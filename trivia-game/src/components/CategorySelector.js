import { useState, useEffect } from "react";
import axios from "axios";

function CategorySelector({ selectedCategory, setSelectedCategory }) {
  const [allCategories, setAllCategories] = useState({});

  useEffect(() => {
    axios
      .get("https://the-trivia-api.com/api/categories")
      .then((res) => setAllCategories(res.data))
      .catch((err) => console.error("Failed to load categories:", err));
  }, []);

  return (
    <div className="category-selector">
      <label htmlFor="category">Select Category:</label>
      <select
        id="category"
        value={selectedCategory}
        onChange={(e) => setSelectedCategory(e.target.value)}
      >
        {/* Default option */}
        <option value="">Any Category</option>

        {/* API-driven categories */}
        {Object.entries(allCategories).map(([friendlyName, slugList]) => (
          <option key={friendlyName} value={slugList[0]}>
            {friendlyName}
          </option>
        ))}
      </select>
    </div>
  );
}

export default CategorySelector;
