const popup = document.getElementById("popup");
const openBtns = document.querySelectorAll(".openBtn");
const closeBtn = document.getElementById("closeBtn");

openBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    document.getElementById("popup-title").innerText = "Profile " + btn.dataset.id;
    document.getElementById("popup-name").innerText = "Name : " + btn.dataset.name;
    document.getElementById("popup-role").innerText = "Role : " + btn.dataset.role;
    document.getElementById("popup-email").innerText = "Email : " + btn.dataset.email;
    popup.style.display = "flex";
  });
});

closeBtn.addEventListener("click", () => {
  popup.style.display = "none";
});

window.addEventListener("click", (e) => {
  if (e.target == popup) popup.style.display = "none";
});
document.querySelectorAll(".openBtn").forEach(btn => {
  btn.addEventListener("click", () => {
    const id = btn.dataset.id;
    const name = btn.dataset.name;
    const role = btn.dataset.role;
    const email = btn.dataset.email;

    document.getElementById("popup-name").textContent = "Name: " + name;
    document.getElementById("popup-role").textContent = "Role: " + role;
    document.getElementById("popup-email").textContent = "Email: " + email;


    document.getElementById("popup-delete").href = `/delete_profile/${id}`;

    document.getElementById("popup").style.display = "flex";
  });
});
