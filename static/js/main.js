document.addEventListener("DOMContentLoaded", function () {
    var toggleBtn = document.querySelector("#toggle-password");
    var passwordField = document.querySelector(".password-field");
    var imageInput = document.getElementById("imageUpload");
    var previewImg = document.getElementById("previewImg");
    var previewContainer = document.getElementById("previewContainer");
    var partnerBtn = document.querySelector("#partnerBtn");
    var partnerCard = document.querySelector(".partner-card");
    console.log(partnerBtn); // Check if the button is selected
    console.log(partnerCard);
    if (!toggleBtn || !passwordField)
        return;
    if (!partnerBtn || !partnerCard) {
        console.error("partnerBtn or partnerCard not found in the DOM.");
        return;
    }
    partnerBtn.addEventListener("click", function () {
        // console.log("Clicked")
        alert("Hello");
        partnerCard.classList.toggle("active");
        partnerCard.classList.toggle("hide");
    });
    toggleBtn.addEventListener("click", function () {
        var isPassword = passwordField.type === "password";
        passwordField.type = isPassword ? "text" : "password";
        toggleBtn.textContent = isPassword ? "HIDE" : "SHOW";
    });
    imageInput.addEventListener("change", function (event) {
        var target = event.target;
        if (target.files && target.files.length > 0) {
            var file = target.files[0];
            var reader = new FileReader();
            reader.onload = function (e) {
                var _a, _b;
                if (previewImg) {
                    previewImg.src = (_a = e.target) === null || _a === void 0 ? void 0 : _a.result;
                }
                else if (previewContainer) {
                    var newImg = document.createElement("img");
                    newImg.src = (_b = e.target) === null || _b === void 0 ? void 0 : _b.result;
                    newImg.className = "w-[100px] h-[100px] rounded-xl object-cover";
                    previewContainer.innerHTML = "";
                    previewContainer.appendChild(newImg);
                }
            };
            reader.readAsDataURL(file);
        }
    });
    // partnerBtn!.addEventListener("click", () => {
    //   console.log("Clicked")
    //   partnerCard?.classList.add("active")
    //   partnerCard?.classList.remove("hide")
    // })
});
