// Récupérer tous les éléments "a" dans le menu
const menuItems = document.querySelectorAll('.menu-list a');

// Parcourir chaque élément "a" et vérifier si son href correspond à l'URL actuelle
menuItems.forEach(item => {
    if (item.href === window.location.href) {
    // Ajouter la classe "is-active" à l'élément correspondant à la page active
    item.classList.add('is-active');
    }
});