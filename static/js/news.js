const categories = [
    "business",
    "sports",
    "technology",
    "health",
    "entertainment"
];

async function loadCategory(category) {

    const container = document.getElementById(
        `${category}-container`
    );

    try {

        const response = await fetch(
            `/news/lazy/${category}/`
        );

        if (!response.ok) {
            throw new Error("Failed to load");
        }

        container.innerHTML = await response.text();

    } catch (error) {

        container.innerHTML =
            "<p>Unable to load news.</p>";

        console.error(error);

    }

}

async function loadHomepage() {

    for (const category of categories) {

        await loadCategory(category);

    }

}

document.addEventListener(
    "DOMContentLoaded",
    loadHomepage
);
