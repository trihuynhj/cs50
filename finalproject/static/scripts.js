function imgError(image) {
    image.onerror = "";
    image.src = "https://memegenerator.net/img/instances/75462543/sorry.jpg"

    document.getElementById("message").innerHTML = "Could not display the chosen image URL. As an apology, please accept this cat:<br>(Note that the chosen image has still been successfully sent to the receiver's email address.)"
    return true;
}