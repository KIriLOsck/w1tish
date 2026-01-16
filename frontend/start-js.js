if (localStorage.getItem("accessToken") != "undefined") {
    console.log(localStorage.getItem("accessToken"))
    getProtectedData(localStorage.getItem("accessToken"));
} else if (localStorage.getItem("refresh_token") != "undefined") {
    console.log(localStorage.getItem("refresh_token"))
    refreshToken(localStorage.getItem("refresh_token"));
} else {create_sign_in_container()}
