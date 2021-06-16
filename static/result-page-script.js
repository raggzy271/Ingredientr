//  VARIABLES

// List of the ingredients
var ingrs = document.getElementsByClassName('ingr');

var getIngrsBtn = document.getElementById('get-ingrs');
var imgViewDiv = document.getElementById('img-view');
var ingrsViewDiv = document.getElementById('ingrs-view');


//FUNCTIONS

//  Function which will listen to clicks on getIngrsBtn
function getIngrs() {
    imgViewDiv.style.display = 'none';
    ingrsViewDiv.style.display = 'flex';
}


// ADDING EVENT LISTENERS

getIngrsBtn.addEventListener('click', getIngrs, false);


//  REPLACING UNDERSCORES THAT INGREDIENTS MAY HAVE BY SPACES

for(var i=ingrs.length-1; i>=0; i--) {
    ingrs[i].textContent = ingrs[i].textContent.replace(/_/g, " ");
}