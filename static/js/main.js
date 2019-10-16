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
        console.log("Check for user");
        $("#login").hide();
        $("#registration").hide();
        $("#navbar-text").html(`Logged in as ${user}!`);
        $("#logout").removeAttr("hidden").show();
    }


    if (sessionStorage.getItem("user") !== null) {
        setPageIfLoggedIn(sessionStorage.getItem("user"))
    }else {
        let a = "a";
        console.log("getting user from main.js");
        $.ajax({
            type: "GET",
            url: "/get_current_user",
            success: function (user) {
                if (user.username) {
                    sessionStorage.setItem("user", user.username);
                    setPageIfLoggedIn(user.username)
                    console.log(user.username)
                }

            }
        });
    }
}

init();
