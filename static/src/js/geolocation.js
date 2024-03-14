odoo.define('hangry.geolocation', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function () {
        // Bind a function to the click event of a button
        $('.my-button').click(function () {
            // Call a JavaScript function
            myFunction();
        });
    });

    // Define your JavaScript function
    function myFunction() {
        console.log('Button clicked!');
        // Your JavaScript code here
    }
});
