document.getElementById("loginBtn").addEventListener("click", function() {
    this.classList.add("clicked");
});

function togglePassword() {
    let passwordField = document.getElementById("password");
    let hideIcon = document.getElementById("hideIcon");
    let showIcon = document.getElementById("showIcon");

    if (passwordField.type === "password") {
        passwordField.type = "text";   
        hideIcon.style.display = "none";
        showIcon.style.display = "inline"; 
    } else {
        passwordField.type = "password"; 
        hideIcon.style.display = "inline";
        showIcon.style.display = "none"; 
    }
}
document.getElementById("loginBtn").addEventListener("click", function() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let promptContainer = document.querySelector(".handling_prompt"); // Get the prompt container

    // Clear previous messages
    promptContainer.innerHTML = "";

    if (!username || !password) {
        promptContainer.innerHTML = `<p style="text-align:center;background: antiquewhite;color: red;">⚠️ Please enter both username and password.</p>`;
        return;
    }

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json().catch(() => { throw new Error("Invalid JSON response") }))
    .then(data => {
        if (data.success) {
            promptContainer.innerHTML = `<p style="text-align:center;background: aliceblue; color: green;">✅ Login successful!</p>`;

            // Redirect based on user type
            if (data.usertype === "Admin") {
                window.location.href = `/admin/${username}`;
            } else if (data.usertype === "Local") {
                window.location.href = `/local/${username}`;
            } else {
                promptContainer.innerHTML += `<p style="text-align:center;background: antiquewhite; color: red;">⚠️ Unknown usertype.</p>`;
            }
        } else {
            promptContainer.innerHTML = `<p style="text-align:center;background: antiquewhite; color: red;">❌ Login failed: ${data.message}</p>`;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        promptContainer.innerHTML = `<p style="color: red;">⚠️ An error occurred. Please try again later.</p>`;
    });
});