// when the user scroll down, the header will be change the bg color
window.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    if (window.scrollY > 0) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// ==============================================================================

// Copyright Date
let time = document.querySelector(".time")
time.innerHTML = new Date().getFullYear() // 2024

// ==============================================================================

// Profile Icon Click Toggle
document.querySelector('.profile i').addEventListener('click', function (e) {
    e.stopPropagation(); // Prevent event from bubbling to document
    document.getElementById('subMenu').classList.toggle('open');
});

// ==============================================================================

// close the submenu anywhere
document.addEventListener('click', function (e) {
    const subMenu = document.getElementById('subMenu');
    const profileIcon = document.querySelector('.profile i');

    // If the click is outside the profile icon and submenu, close the submenu
    if (!subMenu.contains(e.target) && e.target !== profileIcon) {
        subMenu.classList.remove('open');
    }
});

// ==============================================================================
