const nawili = document.querySelector(".nawili");
const img = nawili.querySelector("img");

nawili.addEventListener("mousemove", (e) => {
  const rect = nawili.getBoundingClientRect();

  let x = e.clientX - rect.left;
  let y = e.clientY - rect.top;

  x = (x / rect.width) * 100;
  y = (y / rect.height) * 100;

  img.style.transformOrigin = `${x}% ${y}%`;
  img.style.transform = "scale(1.8)";
});

nawili.addEventListener("mouseleave", () => {
  img.style.transform = "scale(1)";
});
