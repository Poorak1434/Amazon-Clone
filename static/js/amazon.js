document.addEventListener('DOMContentLoaded', function () {
    console.log('Amazon.in JavaScript initialized');

    // Back to top scroll listener
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Pincode Modal toggle
    const navLocationBtn = document.getElementById('navLocationBtn');
    const locationModal = document.getElementById('locationModal');
    const closeModalBtn = document.getElementById('closeModalBtn');

    if (navLocationBtn && locationModal) {
        navLocationBtn.addEventListener('click', function () {
            locationModal.style.display = 'flex';
        });
    }

    if (closeModalBtn && locationModal) {
        closeModalBtn.addEventListener('click', function () {
            locationModal.style.display = 'none';
        });
    }

    window.addEventListener('click', function (e) {
        if (e.target === locationModal) {
            locationModal.style.display = 'none';
        }
    });

    // Product Detail Image Thumbnail Switcher
    const thumbImages = document.querySelectorAll('.thumb-img');
    const mainDetailImg = document.getElementById('mainDetailImg');

    if (thumbImages.length > 0 && mainDetailImg) {
        thumbImages.forEach(function (thumb) {
            thumb.addEventListener('mouseenter', function () {
                thumbImages.forEach(t => t.classList.remove('active'));
                thumb.classList.add('active');
                mainDetailImg.src = thumb.dataset.largeUrl || thumb.src;
            });
        });
    }

    // AJAX Add to Cart
    const ajaxCartForms = document.querySelectorAll('.ajax-cart-form');
    ajaxCartForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            const actionUrl = form.getAttribute('action');

            fetch(actionUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update header cart count
                    const cartCountBadge = document.getElementById('cartCountBadge');
                    if (cartCountBadge) {
                        cartCountBadge.textContent = data.cart_count;
                    }

                    // Toast message
                    showToast(data.message || 'Added to Cart!');
                }
            })
            .catch(error => {
                console.error('Cart update failed:', error);
                form.submit(); // fallback to normal submit
            });
        });
    });

    // Toast Alert Helper
    function showToast(message) {
        let toastBox = document.getElementById('amazonToast');
        if (!toastBox) {
            toastBox = document.createElement('div');
            toastBox.id = 'amazonToast';
            toastBox.style.position = 'fixed';
            toastBox.style.bottom = '20px';
            toastBox.style.right = '20px';
            toastBox.style.backgroundColor = '#007600';
            toastBox.style.color = '#ffffff';
            toastBox.style.padding = '12px 20px';
            toastBox.style.borderRadius = '4px';
            toastBox.style.fontWeight = 'bold';
            toastBox.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
            toastBox.style.zIndex = '10000';
            toastBox.style.transition = 'opacity 0.3s';
            document.body.appendChild(toastBox);
        }
        toastBox.textContent = '✓ ' + message;
        toastBox.style.opacity = '1';
        toastBox.style.display = 'block';

        setTimeout(() => {
            toastBox.style.opacity = '0';
            setTimeout(() => { toastBox.style.display = 'none'; }, 300);
        }, 3000);
    }
});
