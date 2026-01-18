function changeImage(linkElement) {
    const mainImage = document.getElementById("mainImage");
    const clickedImg = linkElement.querySelector("img");


    document.querySelectorAll(".down a").forEach(a => {
        a.classList.remove("active");
    });


    linkElement.classList.add("active");


    mainImage.style.transform = "translateX(-30px)";
    mainImage.style.opacity = "0";

    setTimeout(() => {
        mainImage.src = clickedImg.src;

        mainImage.style.transform = "translateX(0)";
        mainImage.style.opacity = "1";
    }, 200);
}


window.onload = () => {
    const firstLink = document.querySelector(".down a");
    if (firstLink) firstLink.classList.add("active");
};