// Universal image handler for both upload and preview pages
function handleImage(input) {
  const file = input.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const imgData = e.target.result;
      localStorage.setItem('capturedImage', imgData);
      window.location.href = 'estimatedescription.html'; // Redirect to the preview page
    };
    reader.readAsDataURL(file);
  }
}

// Called on window load of calorie-estimator.html to show the image
window.onload = function () {
  const preview = document.getElementById('preview');
  const image = localStorage.getItem('capturedImage');
  if (preview && image) {
    preview.src = image;
  }
};

// Triggers camera input on calorie-estimator page (Retake button)
function triggerCamera() {
  const cameraInput = document.getElementById('cameraInput');
  if (cameraInput) {
    cameraInput.click();
  }
}

// Update image preview if user retakes image
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

function showWarning(message) {
  const warningBox = document.getElementById("warningBox");
  warningBox.innerHTML = `
    <div class="warning-content">
      <span>${message}</span>
      <span style="cursor: pointer; font-weight: bold;" onclick="this.parentElement.parentElement.style.display='none'">X</span>
    </div>
  `;
  warningBox.style.display = "block";
}



function goToCaloriePage() {
  const description = document.getElementById('description').value.trim();
  if (!description) {
    showWarning("Must input description.");
    warningBox.style.display = "block";

    return;
  }
  localStorage.setItem('imageDescription', description); // Optional
  window.location.href = 'estimateshowcalorie.html';
}


