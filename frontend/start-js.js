if (localStorage.getItem("accessToken") != undefined) {
    getProtectedData(localStorage.getItem("accessToken"));
} else if (localStorage.getItem("refresh_token") != undefined) {
    refreshToken(localStorage.getItem("refresh_token"));
} else {create_sign_in_container()}
