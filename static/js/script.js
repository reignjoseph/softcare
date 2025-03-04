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

    if (!username || !password) {
        alert("Please enter both username and password.");
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
            alert(`Login successful! The usertype is: ${data.usertype}`);
        } else {
            alert(`Login failed: ${data.message}`);
        }
    })
    .catch(error => console.error("Error:", error));
});
