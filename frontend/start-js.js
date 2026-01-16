if (localStorage.getItem("accessToken")) { //здесь он вернёт true потому что строка не пуста (undefined)
    await getProtectedData(localStorage.getItem("accessToken"));
} else if (localStorage.getItem("refresh_token")) {
    await refreshToken(localStorage.getItem("refresh_token"));
} else create_sign_in_container();
