// Universal image handler for both upload and preview pages
function handleImage(input) {
  const file = input.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const imgData = e.target.result;
      localStorage.setItem('capturedImage', imgData);
      window.location.href = 'estimatedescription.html'; // Redirect to preview
    };
    reader.readAsDataURL(file);
  }
}

// Trigger camera input
function triggerCamera() {
  const cameraInput = document.getElementById('cameraInput');
  if (cameraInput) cameraInput.click();
}

// Preview image if retaken
function previewImage(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const imgData = e.target.result;
      localStorage.setItem('capturedImage', imgData);
      const preview = document.getElementById('preview');
      if (preview) preview.src = imgData;
    };
    reader.readAsDataURL(file);
  }
}

// Show preview image on load
document.addEventListener("DOMContentLoaded", function () {
  const preview = document.getElementById('preview');
  const image = localStorage.getItem('capturedImage');
  if (preview && image) preview.src = image;

  const galleryInput = document.getElementById('galleryInput');
  if (galleryInput) {
    galleryInput.value = '';
    galleryInput.addEventListener('change', function () {
      if (this.files.length > 0) {
        const uploadForm = document.getElementById('uploadForm');
        if (uploadForm) uploadForm.submit();
      }
    });
  }
});

// Reset file input if navigating back
window.addEventListener('pageshow', function (event) {
  const input = document.getElementById('galleryInput');
  if ((event.persisted || performance.getEntriesByType("navigation")[0].type === "back_forward") && input) {
    input.value = '';
  }
});
