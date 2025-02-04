document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.querySelector<HTMLSpanElement>("#toggle-password");
    const passwordField = document.querySelector<HTMLInputElement>(".password-field");
  
    if (!toggleBtn || !passwordField) return;
  
    toggleBtn.addEventListener("click", () => {
      const isPassword = passwordField.type === "password";
      passwordField.type = isPassword ? "text" : "password";
      toggleBtn.textContent = isPassword ? "HIDE" : "SHOW";
    });
  });
  