// compressing files on client side (and hopefully on server too)
function compressImage(file, previewElementId, inputElementId, quality=0.8){
    if (!file) return;
    const img = new Image();
    img.src = URL.createObjectURL(file);
    img.onload = function(){
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const MAX_SIZE = 300;
        let targetWidth = img.width;
        let targetHeight = img.height;
        if (targetWidth > MAX_SIZE || targetHeight > MAX_SIZE){
            if (targetWidth > targetHeight){ // альбом (e.g. 1920x1080)
                targetHeight = Math.round((targetHeight * MAX_SIZE) / targetWidth);
                targetWidth = MAX_SIZE;
            }
            else{ // верт (e.g. 1080x1920)
                targetWidth = Math.round((targetWidth * MAX_SIZE) / targetHeight);
                targetHeight = MAX_SIZE;
            }
        }
        canvas.width = targetWidth;
        canvas.height = targetHeight;
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(function(blob){
            // shoutout to google
            const compressedUrl = URL.createObjectURL(blob);
            document.getElementById(previewElementId).src = compressedUrl;

            const compressedFile = new File([blob], file.name, {
                type:'image/jpeg',
                lastModified:Date.now()
            })

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(compressedFile);

            document.getElementById(inputElementId).files = dataTransfer.files;
        }, 'image/jpeg', quality)
    }
}