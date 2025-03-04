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
