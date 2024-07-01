$(document).ready(function () {

    $('#menu').click(function () {
        $(this).toggleClass('fa-times');
        $('.navbar').toggleClass('nav-toggle');
    });


});
function success() {
    // Display a toast notification with a close button and a green linear gradient background
    Toastify({
        text: "Successfully Login 😊",
        duration: 3000, // 3 seconds
        gravity: "top", // `top` or `bottom`
        position: "center", // `left`, `center`, or `right`
        style: {
            background: "green",
            color: "WHite",
            border: "15px" // Green linear gradient background
        },
        stopOnFocus: true, // Stop timeout when focused
        close: true, // Show close button
    }).showToast();

}
function failure() {
    // Display a toast notification with a close button and a green linear gradient background
    Toastify({
        text: "Something Went Wrong 😞",
        duration: 3000, // 3 seconds
        gravity: "top", // `top` or `bottom`
        position: "center", // `left`, `center`, or `right`
        style: {
            background: "red",
            color: "WHite",
            border: "15px" // Green linear gradient background
        },
        stopOnFocus: true, // Stop timeout when focused
        close: true, // Show close button
    }).showToast();

}
