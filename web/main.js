async function resultsprocessing(){
    const searchInput = document.getElementById("searchInput");
    const results = await eel.search(searchInput.value)();
    console.log(results["List"]["Allergy MedicationMultivitamins"]);

    document.getElementById("results").innerText = results["Apriory"];
    const ScrollDiv = document.getElementById("Scroll")
    ScrollDiv.innerHTML = ""

    for (let i = 0; i < results["ListKeys"].length; i++) {
        
        const p = document.createElement("p")
        p.innerHTML = results["ListKeys"][i] + "  :  " + results["List"][results["ListKeys"][i]]
        ScrollDiv.appendChild(p)
        
    }
    
    
}

document.getElementById("search").addEventListener("click",resultsprocessing);