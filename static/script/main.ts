document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.querySelector<HTMLSpanElement>("#toggle-password")
  const passwordField = document.querySelector<HTMLInputElement>(".password-field")
  const imageInput = document.getElementById("imageUpload") as HTMLInputElement
  const previewImg = document.getElementById("previewImg") as HTMLImageElement | null
  const previewContainer = document.getElementById("previewContainer") as HTMLDivElement | null
  const partnerBtn = document.querySelector<HTMLButtonElement>("#partnerBtn")
  const partnerCard = document.querySelector<HTMLDivElement>(".partner-card")

  console.log(partnerBtn) // Check if the button is selected
  console.log(partnerCard)
  if (!toggleBtn || !passwordField) return

  if (!partnerBtn || !partnerCard) {
    console.error("partnerBtn or partnerCard not found in the DOM.")
    return
  }

  partnerBtn.addEventListener("click", () => {
    // console.log("Clicked")
    alert("Hello")
    partnerCard.classList.toggle("active")
    partnerCard.classList.toggle("hide")
  })

  toggleBtn.addEventListener("click", () => {
    const isPassword = passwordField.type === "password"
    passwordField.type = isPassword ? "text" : "password"
    toggleBtn.textContent = isPassword ? "HIDE" : "SHOW"
  })

  imageInput.addEventListener("change", (event: Event) => {
    const target = event.target as HTMLInputElement
    if (target.files && target.files.length > 0) {
      const file = target.files[0]
      const reader = new FileReader()

      reader.onload = (e) => {
        if (previewImg) {
          previewImg.src = e.target?.result as string
        } else if (previewContainer) {
          const newImg = document.createElement("img")
          newImg.src = e.target?.result as string
          newImg.className = "w-[100px] h-[100px] rounded-xl object-cover"
          previewContainer.innerHTML = ""
          previewContainer.appendChild(newImg)
        }
      }

      reader.readAsDataURL(file)
    }
  })

  // partnerBtn!.addEventListener("click", () => {
  //   console.log("Clicked")
  //   partnerCard?.classList.add("active")
  //   partnerCard?.classList.remove("hide")
  // })
})
