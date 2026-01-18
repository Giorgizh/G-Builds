document.querySelectorAll(".wishlist-btn").forEach(button => {
    button.addEventListener("click", () => {
        const productId = button.dataset.productId;
        const name = button.dataset.name;
        const price = button.dataset.price;
        const productType = button.dataset.productType;

        fetch("{{ url_for('add_to_wishlist') }}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token() if csrf_token else '' }}"
            },
            body: JSON.stringify({ product_id: productId, name: name, price: price, product_type: productType })
        })
        .then(res => res.json())
        .then(data => {
            if(data.success){
                const icon = button.querySelector("i");
                icon.classList.remove("fa-regular");
                icon.classList.add("fa-solid");
            } else {
                alert(data.message);
            }
        })
        .catch(err => console.error(err));
    });
});
