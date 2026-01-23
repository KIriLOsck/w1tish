async function register_user(username, email, password) {
    const response = await fetch('http://localhost/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });
    
    if (response.status === 201) {

        const data = await response.json();
        localStorage.setItem("accessToken", data.access_token);
        window.location.replace("app.html"); 

    } else if (response.status === 409) {
        document.getElementById("error").textContent == "Вы ввели занятый логин/почту";                            
    } else { 
        console.log("Ошибка: ", response.status);
    }
}


async function login(username, password) {
    const response = await fetch('http://localhost/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (response.status === 422) {
        console.log("Виноват фронтендер");

    } else if (response.status === 404) { 
        //error_text.textContent = "Вы не зарегистрированы"; //не успевает отображаться
        create_registration_container();

    } else if (response.status === 500) {
        console.log("Виноват бэкэндер");

    } else if (response.status === 200) {                            
        const data = await response.json();
        localStorage.setItem("accessToken", data.access_token);
        window.location.replace("app.html");
    } else { 
        console.log("Error", response.status)
    }
}


async function getProtectedData() {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken != null) {

        const response = await fetch('http://localhost/api/data/', {
            method: "GET",
            headers: {
                'Content-Type': 'application/json', 
                'Access-Token': accessToken
            }
        });

        if (response.status === 401 || response.status === 422) { 
            console.log("Нужно обновить токен (refresh)");
            await refreshToken();

        } else if (response.status === 500) {
            console.log("Виноват бэкэндер")

        } else if (response.status === 404) {
            localStorage.removeItem("accessToken");
            window.location.replace("index.html");
            create_sign_in_container();
        } else {
            const data = await response.json();
            console.log(data)
            localStorage.setItem("nickname", data.nickname);
            localStorage.setItem("avatar", data.avatar_url);
            localStorage.setItem("chats", JSON.stringify(data.chats));
            localStorage.setItem("id", data.id);

            if (window.location.pathname == "/app.html") load_contacts(); load_profile();
        }
    } else {
        await refreshToken();
    }
}


async function refreshToken() {

    const response = await fetch('http://localhost/auth/refresh', {
        method: "POST",
        headers: { 'Content-Type': 'application/json' }
    });
    console.log(response.status)
    if (response.status === 200) {
        const data = await response.json();
        localStorage.setItem("accessToken", data.access_token);

    } else if (response.status === 500) {
        console.log("Iternal server error");
        // TODO сделай функцию которая будет показывать ошибку на фронте

    } else if (response.status === 422 || response.status === 401) {
        localStorage.removeItem("accessToken");
        window.location.replace("index.html");
        create_sign_in_container();
    }
}