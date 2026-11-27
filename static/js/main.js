// General UI helpers for Shiva Commercial Institute
function togglePasswordField(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  if (input.type === "password") {
    input.type = "text";
    if (btn) btn.textContent = "Hide";
  } else {
    input.type = "password";
    if (btn) btn.textContent = "Show";
  }
}

function previewAdmissionPhoto(input) {
  const box = document.getElementById("photoPreviewBox");
  const hiddenInput = document.getElementById("capturedPhotoData");
  if (!box || !input.files || !input.files[0]) return;
  if (hiddenInput) hiddenInput.value = "";
  const reader = new FileReader();
  reader.onload = function (e) {
    box.innerHTML = `<img src="${e.target.result}" alt="Candidate Photo">`;
  };
  reader.readAsDataURL(input.files[0]);
}

let activeCameraStream = null;

async function openAdmissionCamera() {
  const camWrap = document.getElementById("liveCameraContainer");
  const video = document.getElementById("cameraVideo");
  const statusEl = document.getElementById("cameraStatusText");
  if (!camWrap || !video) return;

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert("Live camera is not supported in this browser. Please upload a photo file instead.");
    return;
  }

  try {
    stopAdmissionCamera();
    activeCameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user", width: { ideal: 480 }, height: { ideal: 560 } },
      audio: false
    });
    video.srcObject = activeCameraStream;
    camWrap.classList.remove("d-none");
    if (statusEl) statusEl.textContent = "Camera active — click Capture Photo.";
  } catch (err) {
    if (statusEl) statusEl.textContent = "Camera permission denied or no webcam detected.";
    alert("Could not access camera: " + err.message);
  }
}

function captureAdmissionPhoto() {
  const video = document.getElementById("cameraVideo");
  const canvas = document.getElementById("cameraCanvas");
  const box = document.getElementById("photoPreviewBox");
  const hiddenInput = document.getElementById("capturedPhotoData");
  const fileInput = document.getElementById("photoFileInput");
  const statusEl = document.getElementById("cameraStatusText");
  if (!video || !canvas || !box || !hiddenInput) return;

  const w = video.videoWidth || 360;
  const h = video.videoHeight || 420;
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, w, h);

  const dataUrl = canvas.toDataURL("image/jpeg", 0.9);
  hiddenInput.value = dataUrl;
  if (fileInput) fileInput.value = "";
  box.innerHTML = `<img src="${dataUrl}" alt="Captured Candidate Photo">`;
  if (statusEl) statusEl.textContent = "Photo captured from live camera!";
  stopAdmissionCamera();
}

function stopAdmissionCamera() {
  const camWrap = document.getElementById("liveCameraContainer");
  const video = document.getElementById("cameraVideo");
  if (activeCameraStream) {
    activeCameraStream.getTracks().forEach((t) => t.stop());
    activeCameraStream = null;
  }
  if (video) video.srcObject = null;
  if (camWrap) camWrap.classList.add("d-none");
}

function copyIntimationMessage(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => {
      alert("Fee intimation message copied! You can paste it into WhatsApp or SMS.");
    });
  } else {
    prompt("Copy this fee intimation message:", text);
  }
}
