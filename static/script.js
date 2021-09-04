(() => {
    const uploadForm = document.getElementById('upload-form');
    const uploadInput = document.getElementById('upload-input');
    const imageToUpload = document.getElementById('image-to-upload');
    const uploadRegion = document.getElementById('upload-region'); // Also the drop region
    const dropMessage = document.getElementById('drop-message');
    const imagePreview = document.getElementById('image-preview');
    const removeImageBtn = document.getElementById('remove-image-btn');
    const loader = document.getElementById('loader');

    function imageSelected(imageFile) {
        const validExtensions = ['image/jpeg', 'image/jpg', 'image/png'];
        const MAX_SIZE = 10_000_000;
        const MAX_SIZE_STR = '10MB';

        //  Check if extension is valid i.e., file is a valid image
        if (!validExtensions.includes(imageFile.type)) {
            alert('Upload a .jpg/.jpeg or .png file only.');
        }
        //  Limit size of image file
        else if (imageFile.size > MAX_SIZE) {
            alert('Your file must be less than or equal to ' + MAX_SIZE_STR);
        }
        else {
            imageToUpload.src = URL.createObjectURL(imageFile);
            uploadRegion.style.display = 'none';
            imagePreview.style.display = 'flex';
        }
    }


    //  When a file is selected from the dialog
    uploadInput.addEventListener('change', () => {
        imageSelected(uploadInput.files[0])
    });


    //  Handling dragovers
    document.addEventListener('dragover', (event) => {
        event.preventDefault();
        const target = event.target;

        //  Check the WHOLE document if the region a file is dragged over is the upload region or one of its child nodes
        var draggingOverUploadRegion = target === uploadRegion;
        uploadRegion.childNodes.forEach((childNode) => {
            if (!draggingOverUploadRegion) {
                draggingOverUploadRegion = target == childNode;
            }
        });

        //  If it IS the upload region (or one of its children), then display the drop message, otherwise eh
        if (draggingOverUploadRegion) {
            dropMessage.style.display = 'flex';
        }
        else {
            dropMessage.style.display = 'none';
        }
    });


    //  Handling file drops
    uploadRegion.addEventListener('drop', (event) => {
        event.preventDefault();

        dropMessage.style.display = 'none';

        const droppedFiles = event.dataTransfer.files;

        if (droppedFiles.length) {  // If dropped from the operating system (File system)
            if (droppedFiles.length > 1) {
                alert('Upload only one file at a time.');
            }
            else {
                uploadInput.files = droppedFiles;
                imageSelected(droppedFiles[0]);
            }
        }
        else {  //  If dropped from somewhere else
            alert('There was an error processing your file.')
        }
    }, false);

    // To remove (deselect) the selected image
    removeImageBtn.addEventListener('click', () => {
        imageToUpload.src = '';
        uploadInput.value = '';
        uploadRegion.style.display = 'block';
        imagePreview.style.display = 'none';
    }, false);

    //  When form is to be submitted
    uploadForm.addEventListener('submit', (event) => {
        //  Validation - Only submit when an image is selected
        if (uploadInput.files.length === 1) {
            //  Showing the loader while processing; hide everything else
            imagePreview.style.display = 'none';
            loader.style.display = 'block';
        }
        else {
            alert('There was an error. Try again please.')
            event.preventDefault();
        }
    }, false);
})();