const form = document.getElementById("textForm");
const input = document.getElementById("textInput");
const output = document.getElementById("maskedOutput");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value;

    try {
        const response = await fetch("/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: text, prompt_type: "full_anonymization" }),
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        output.textContent = data.masked_text;
    } catch (err) {
        console.error("Error:", err);
        output.textContent = "Error processing text.";
    }
});
