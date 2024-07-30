function previewFile() {
    const preview = document.getElementById('preview');
    const file = document.getElementById('fileInput').files[0];
    const reader = new FileReader();

    reader.addEventListener('load', function () {
        // convert image file to base64 string
        preview.src = reader.result;
        preview.style.display = 'block';
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}

const dropContainer = document.getElementById("dropcontainer")
const fileInput = document.getElementById("images")

dropContainer.addEventListener("dragover", (e) => {
  // prevent default to allow drop
  e.preventDefault()
}, false)

dropContainer.addEventListener("dragenter", () => {
  dropContainer.classList.add("drag-active")
})

dropContainer.addEventListener("dragleave", () => {
  dropContainer.classList.remove("drag-active")
})

dropContainer.addEventListener("drop", (e) => {
  e.preventDefault()
  dropContainer.classList.remove("drag-active")
  fileInput.files = e.dataTransfer.files
})