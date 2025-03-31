function checkGrammar() {
    const sentence = document.getElementById("sentence").value;
    fetch("http://127.0.0.1:5002/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sentence: sentence })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = 
            data.valid ? "Sentence is grammatically correct!" : "Sentence is incorrect: " + (data.error || "Invalid structure.");
    })
    .catch(error => console.error("Error:", error));
}