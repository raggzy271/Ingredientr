//  VARIABLES AND FUNCTIONS

var uploadForm = document.getElementById('upload-form');
var input = document.getElementById('upload-input');
var uploadRegion = document.getElementById('upload-region'); // Also the drop region
var dropMessage = document.getElementById('drop-message');
var imagePreview = document.getElementById('image-preview');
var loader = document.getElementById('loader');

function imageSelected(file) {
    imageToUpload = file;
    var url, validExtensions = ['image/jpeg', 'image/jpg', 'image/png'];

    //  Check if extension is valid i.e., file is a valid image

    if (validExtensions.includes(imageToUpload.type)) {
        url = URL.createObjectURL(imageToUpload);
        document.getElementById('toUpload').src = url;

        uploadRegion.style.display = 'none';
        imagePreview.style.display = 'flex';
    }
    else {
        alert('Upload a .jpg/.jpeg or .png file.');
    }
}

//  HANDLING IMAGE SELECTION (WHICH WILL BE UPLOADED) BY FILE DIALOG BOX

input.addEventListener('change', () => imageSelected(input.files[0]), false);

//  HANDLING DRAGGING OVER

document.addEventListener('dragover', (event) => {
    event.preventDefault();
    var targ = event.target;

    //  Check the WHOLE document if the region a file is dragged over is the upload region or one of its child nodes

    var draggingOverUploadRegion = targ === uploadRegion;

    uploadRegion.childNodes.forEach((currentValue) => {
        if (!draggingOverUploadRegion)
            draggingOverUploadRegion = targ == currentValue;
    });

    //  If it IS the upload region (or one of its children), then display the drop message, otherwise eh

    if (draggingOverUploadRegion) {
        dropMessage.style.display = 'flex';
    }
    else {
        dropMessage.style.display = 'none';
    }
}, false);

//  HANDLING DROPS (EITHER FROM OPERATING SYSTEM i.e., FILES OR WEB i.e., URLs)

uploadRegion.addEventListener('drop', (event) => {
    event.preventDefault();
    dropMessage.style.display = 'none';

    var dt = event.dataTransfer;
    var dropped = dt.files;

    if (dropped.length) {   //  If dropped from Files (OS)
        if (dropped.length > 1) {
            alert('Upload one file at a time.');
        }
        else {
            imageSelected(dropped[0]);
        }
    }
    else {  //  If dropped from WEB (a URL)
        var html = dt.getData('text/html'), match = html && /\bsrc="?([^"\s]+)"?\s*/.exec(html), url = match && match[1];

        if (url) {
            var img = new Image;
            var c = document.createElement("canvas");
            var ctx = c.getContext("2d");

            img.onload = function () {
                c.width = this.naturalWidth;     // update canvas size to match image
                c.height = this.naturalHeight;
                ctx.drawImage(this, 0, 0);       // draw in image
                c.toBlob(function (blob) {        // get content as PNG blob

                    // call our main function
                    imageSelected(blob);

                }, "image/png");
            };

            img.onerror = function () {
                alert("Error in uploading");
            }

            img.crossOrigin = "";              // if from different origin
            img.src = url;
        }
        else {
            alert('Error in uploading');
        }
    }
}, false);

//  WHEN THE CROSS IS CLICKED (SELECTED IMAGE IS UNDESIRED)

document.getElementById('cancel').addEventListener('click', () => {
    //  unselect the image
    imageToUpload = null;
    input.value = '';

    uploadRegion.style.display = 'block';
    imagePreview.style.display = 'none';
}, false);

//  HANDLING UPLOADS

uploadForm.addEventListener('submit', (event) => {
    //  Showing the loader while processing; hide everything else
    imagePreview.style.display = 'none';
    loader.style.display = 'block';
    
    //  Validation - Only submit when an image is selected
    //  Didn't use 'required' attribute with the input tag because it doesn't register when files are dropped
    if (!imageToUpload) {
        event.preventDefault();
    }

    //  There is no need to handle submissions when the user has uploaded through file dialog boxes. 
    //  Because on submitting then, it directly sends the image with the request to the 'action'
    //  We only need to handle when the user has selected his file through drag & drop (either from OS or WEB) - Manually sending POST requests

    else if (!input.value) {
        var formData = new FormData();
        formData.append('image', imageToUpload);

        //  Get CSRF token

        csrfToken = null;

        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();

                //  Does this cookie string begin with 'csrftoken'

                if (cookie.substring(0, 'csrftoken='.length) === ('csrftoken=')) {
                    csrfToken = decodeURIComponent(cookie.substring('csrftoken='.length));
                    break;
                }
            }
        }

        $.ajax({
            url: '',
            method: 'post',
            data: formdata,
            contentType: false,
            processData: false,
            dataType: 'json',
            success: function (response) {
                console.log(response);
            }
        });

        // var request = new XMLHttpRequest();
        // request.setRequestHeader('X-CSRF-Token', csrfToken);
        // request.open('POST', '');
        // request.send(formData);
    }
}, false);