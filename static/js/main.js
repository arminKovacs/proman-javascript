import { dom } from "./dom.js";

// This function is to initialize the application
function init() {
    // init data
    dom.init();
    // loads the boards to the screen
    dom.loadBoards();
    checkForUser()
}


function checkForUser() {
    function setPageIfLoggedIn (user) {
        $("#login").hide();
        $("#registration").hide();
        $("#navbar-text").html(`Logged in as ${user}!`);
        $("#logout").removeAttr("hidden").show();
    }


    if (sessionStorage.getItem("user") !== null) {
        setPageIfLoggedIn(sessionStorage.getItem("user"))
    }else {
        $.ajax({
            type: "GET",
            url: "/get_current_user",
            success: function (user) {
                console.log(user);
            if (user['user'][0]) {
                    sessionStorage.setItem("user", user['user'][0]);
                    sessionStorage.setItem("user_id", user['user'][1]);
                    setPageIfLoggedIn(user[0]);
                }

            }
        });
    }
}

init();
