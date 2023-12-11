function checkEnter(event) {
    if (event.key === "Enter") {
        createClusterFields();
    }
}

function createClusterFields() {
    const numberOfClusters = parseInt(document.getElementById("numclusters").value);
    const clusterInputsContainer = document.querySelector(".cluster-fields");

    clusterInputsContainer.innerHTML = "";

    for (let i = 1; i <= numberOfClusters; i++) {
        const label = document.createElement("label");
        label.setAttribute("for", "cluster" + i);
        label.textContent = "Enter Cluster Center " + i + ":";

        const input = document.createElement("input");
        input.type = "text";
        input.id = "cluster" + i;
        input.name = "cluster" + i;
        input.placeholder = "Cluster Center " + i;

        clusterInputsContainer.appendChild(label);
        clusterInputsContainer.appendChild(input);
    }
}

async function processKMeans() {
    const numClusters = document.getElementById("numclusters").value;
    const clusterPoints = [];

    for (let i = 1; i <= numClusters; i++) {
        const clusterPoint = document.getElementById("cluster" + i).value;
        clusterPoints.push(clusterPoint);
    }

    const results = await eel.perform_kmeans(numClusters, clusterPoints)();

    const outputContainer = document.querySelector(".output-container");
    outputContainer.innerHTML = ""; 

    results.forEach((result) => {
        const iterationDiv = document.createElement("div");
        iterationDiv.className = "iteration";

        const iterationHeader = document.createElement("h3");
        iterationHeader.textContent = result;

        iterationDiv.appendChild(iterationHeader);

        outputContainer.appendChild(iterationDiv);
    });
}

async function searchProducts() {
    const searchInput = document.getElementById("search-input").value;

    if (searchInput) {
        const recommendedProducts = await eel.search_products(searchInput)();
        const searchResults = document.getElementById("search-results");

        searchResults.innerHTML = "";

        if (recommendedProducts.length > 0) {
            recommendedProducts.forEach((product) => {
                const productElement = document.createElement("p");
                productElement.textContent = product;
                searchResults.appendChild(productElement);
            });
        } else {
            const noResultsElement = document.createElement("p");
            noResultsElement.textContent = "No recommended products in the same cluster.";
            searchResults.appendChild(noResultsElement);
        }
    }
}
