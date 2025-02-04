document.addEventListener("DOMContentLoaded", function () {
    var toggleBtn = document.querySelector("#toggle-password");
    var passwordField = document.querySelector(".password-field");
    if (!toggleBtn || !passwordField)
        return;
    toggleBtn.addEventListener("click", function () {
        var isPassword = passwordField.type === "password";
        passwordField.type = isPassword ? "text" : "password";
        toggleBtn.textContent = isPassword ? "HIDE" : "SHOW";
    });
});
