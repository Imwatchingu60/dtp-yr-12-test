function selectedSeasons() {
    const values = [];
    const boxes = document.querySelectorAll('input[name="season"]:checked');

    for (const box of boxes) {
        values.push(box.value);
    }

    return values;
}

const quickSearch = document.querySelector("#quick-search");

if (quickSearch !== null) {
    const flowerRows = document.querySelectorAll("body > div");
    const flowerCount = document.querySelector(".filter-count");

    quickSearch.addEventListener("input", () => {
        const searchText = quickSearch.value.trim().toLowerCase();
        let visibleCount = 0;

        for (const row of flowerRows) {
            const rowText = row.textContent.toLowerCase();
            const matches = rowText.includes(searchText);
            row.hidden = !matches;

            if (matches) {
                visibleCount++;
            }
        }

        const noun = visibleCount === 1 ? "flower" : "flowers";
        flowerCount.textContent = visibleCount + " " + noun + " shown";
    });
}

const flowerForm = document.querySelector(".flower-form");

if (flowerForm !== null) {
    const nameInput = document.querySelector("#name");
    const latinInput = document.querySelector("#latin");
    const colourInput = document.querySelector("#colour_id");
    const categoryInput = document.querySelector("#category_id");
    const sunlightInput = document.querySelector("#sunlight");
    const wateringInput = document.querySelector("#watering");
    const difficultyInput = document.querySelector("#difficulty");

    const previewName = document.querySelector("#preview-name");
    const previewLatin = document.querySelector("#preview-latin");
    const previewColour = document.querySelector("#preview-colour");
    const previewCategory = document.querySelector("#preview-category");
    const previewSeason = document.querySelector("#preview-season");
    const previewSunlight = document.querySelector("#preview-sunlight");
    const previewWatering = document.querySelector("#preview-watering");
    const previewDifficulty = document.querySelector("#preview-difficulty");

    function updatePreviewLists() {
        const colourName = colourInput.options[colourInput.selectedIndex].textContent.trim();
        const categoryName = categoryInput.options[categoryInput.selectedIndex].textContent.trim();

        previewColour.textContent = colourInput.value ? colourName : "Not selected";
        previewCategory.textContent = categoryInput.value ? categoryName : "Not selected";
        previewSunlight.textContent = sunlightInput.value;
        previewWatering.textContent = wateringInput.value;
        previewDifficulty.textContent = difficultyInput.value;
    }

    function updatePreview() {
        const flowerName = nameInput.value.trim();
        const latinName = latinInput.value.trim();
        const seasons = selectedSeasons();

        previewName.textContent = flowerName || "Flower name";
        previewLatin.textContent = latinName || "Latin name";
        previewSeason.textContent = seasons.length === 0
            ? "Not selected"
            : seasons.join(", ");

        updatePreviewLists();
    }

    flowerForm.addEventListener("input", updatePreview);

    updatePreview();
}
