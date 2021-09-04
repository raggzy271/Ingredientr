//  Replacing underscores that ingredients may have with spaces
(() => {
    const ingredients = document.getElementsByClassName('ingr');
    for(var i = ingredients.length - 1; i >= 0; i--) {
        ingredients[i].textContent = ingredients[i].textContent.replace(/_/g, " ");
    }
})();