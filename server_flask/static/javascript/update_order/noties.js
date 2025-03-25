
const notesDisplay = document.getElementById("notesDisplay");
const notesInput = document.getElementById("notesInput");
const notesHidden = document.getElementById("notesHidden");

notesDisplay.addEventListener("click", function () {
  notesDisplay.classList.add("d-none");
  notesInput.classList.remove("d-none");
  notesInput.focus();
});

notesInput.addEventListener("blur", function () {
  const value = notesInput.value.trim();
  notesDisplay.textContent = value;
  notesHidden.value = value;

  notesInput.classList.add("d-none");
  notesDisplay.classList.remove("d-none");
});