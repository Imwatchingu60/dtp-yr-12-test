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

const particleCanvas = document.querySelector("#particle-canvas");
const particleContext = particleCanvas.getContext("2d");
const particles = [];
const particleCount = 100;
const linkDistance = 110;
const initialSpeed = 1;
const gravity = 100;
const gravityLimit = 0.1;
const damping = 0.999;
const dampingThreshold = 0.1;
let mouseX = -1000;
let mouseY = -1000;

function makeParticles() {
    particleCanvas.width = window.innerWidth;
    particleCanvas.height = window.innerHeight;

    particles.length = 0;

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * particleCanvas.width,
            y: Math.random() * particleCanvas.height,
            dx: (Math.random() - 0.5) * initialSpeed,
            dy: (Math.random() - 0.5) * initialSpeed
        });
    }
}

function drawLine(x1, y1, x2, y2, opacity) {
    particleContext.beginPath();
    particleContext.moveTo(x1, y1);
    particleContext.lineTo(x2, y2);
    particleContext.strokeStyle = "rgba(62, 107, 62, " + opacity + ")";
    particleContext.stroke();
}

function animateParticles() {
    particleContext.clearRect(0, 0, particleCanvas.width, particleCanvas.height);

    for (const particle of particles) {
        const mouseDx = mouseX - particle.x;
        const mouseDy = mouseY - particle.y;
        const mouseDistance = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy);

        if (mouseDistance && mouseDistance > 0) {
            const force = Math.min(gravityLimit, gravity / mouseDistance**2);
            particle.dx += mouseDx / mouseDistance * force;
            particle.dy += mouseDy / mouseDistance * force;
            if(Math.sqrt(particle.dx**2 + particle.dy**2) > dampingThreshold) {
                particle.dx *= damping;
                particle.dy *= damping;
            }
        }

        particle.x += particle.dx;
        particle.y += particle.dy;

        if (particle.x < 0 || particle.x > particleCanvas.width) {
            particle.dx = -particle.dx;
        }
        if (particle.y < 0 || particle.y > particleCanvas.height) {
            particle.dy = -particle.dy;
        }
    }

    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
            const first = particles[i];
            const second = particles[j];
            const lineDx = first.x - second.x;
            const lineDy = first.y - second.y;
            const distance = Math.sqrt(lineDx * lineDx + lineDy * lineDy);

            if (distance < linkDistance) {
                const opacity = (1 - distance / linkDistance) * 0.35;
                drawLine(first.x, first.y, second.x, second.y, opacity);
            }
        }
    }

    for (const particle of particles) {
        const mouseDx = mouseX - particle.x;
        const mouseDy = mouseY - particle.y;
        const mouseDistance = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy);
        if (mouseDistance < linkDistance) {
            const opacity = (1 - mouseDistance / linkDistance) * 0.55;
            drawLine(mouseX, mouseY, particle.x, particle.y, opacity);
        }

        particleContext.beginPath();
        particleContext.arc(particle.x, particle.y, 2, 0, Math.PI * 2);
        particleContext.fillStyle = "#6b8a6b";
        particleContext.fill();
    }

    requestAnimationFrame(animateParticles);
}

window.addEventListener("mousemove", (event) => {
    mouseX = event.clientX;
    mouseY = event.clientY;
});

window.addEventListener("mouseleave", () => {
    mouseX = -1000;
    mouseY = -1000;
});

window.addEventListener("resize", makeParticles);

makeParticles();
animateParticles();