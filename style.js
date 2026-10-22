const feedbackForm = document.getElementById("feedbackForm");
const successMessage = document.getElementById("successMessage");

feedbackForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const category = document.getElementById("category").value;
    const message = document.getElementById("message").value.trim();

    if (!name || !email || !category || !message) {
        alert("Please complete all required fields.");
        return;
    }

    successMessage.style.display = "block";

    feedbackForm.reset();

    successMessage.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
});