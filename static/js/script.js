const analyzeBtn = document.getElementById("analyzeBtn");

analyzeBtn.addEventListener("click", function() {

    const ideaInput = document.getElementById("ideaInput");
    const ideaText = ideaInput.value;

    console.log("User Idea:", ideaText);

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ idea: ideaText })
    });

});