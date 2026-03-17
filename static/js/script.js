const analyzeBtn = document.getElementById("analyzeBtn");

analyzeBtn.addEventListener("click", function () {

    const ideaInput = document.getElementById("ideaInput");
    const ideaText = ideaInput.value;

    if (ideaText.trim() === "") {
        alert("Please enter an idea first");
        return;
    }

    // show loading animation
    document.getElementById("loading").style.display = "block";
    document.getElementById("result").style.display = "none";

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ idea: ideaText })
    })
    .then(response => response.json())
    .then(data => {

        // hide loading animation
        document.getElementById("loading").style.display = "none";
        document.getElementById("result").style.display = "block";

        document.getElementById("summary").innerText = data.summary;
        document.getElementById("techStack").innerText = data.tech_stack.join(", ");
        document.getElementById("steps").innerText = data.steps.join(" | ");
        document.getElementById("challenges").innerText = data.challenges.join(", ");

    });

});