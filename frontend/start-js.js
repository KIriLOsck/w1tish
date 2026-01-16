if (localStorage.getItem("accessToken") != undefined) {
    await getProtectedData(localStorage.getItem("accessToken"))
} else if (localStorage.getItem("refresh_token") != undefined) {
    await refreshToken(localStorage.getItem("refresh_token"))
} else {create_sign_in_container()}
