async function register_user(username, email, password) {
    const response = await fetch('http://127.0.0.1/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });
    
    if (response.status === 201) {

        const data = await response.json();
        localStorage.setItem("accessToken", data.access_token);
        localStorage.setItem("refreshToken", data.refresh_token);

        window.location.replace("app.html"); 

    } else {                                            //TODO обработай ошибку 409 (пользователь уже существует)
        console.log("Ошибка: ", response.status)
    }
}

async function login(username, password) {
    const response = await fetch('http://127.0.0.1/api/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (response.status === 422) {
        console.log("Виноват фронтендер");

    } else if (response.status === 404) { 
        error_text.textContent = "Вы не зарегистрированы";
        create_registration_container();

    } else if (response.status === 500) {
        console.log("Виноват бэкэндер");

    } else if (response.status === 200) {                            
        const data = await response.json();
        localStorage.setItem("accessToken", data.access_token);
        localStorage.setItem("refreshToken", data.refresh_token);
        window.location.replace("app.html");
    } else { //TODO обработай 401 (неправильный логин или пароль)
        console.log("Error", response.status)
    }
}

async function getProtectedData() {
    const accessToken = localStorage.getItem("accessToken");
    if (refreshToken != null) {

        const response = await fetch('http://localhost/data/', {
            method: "GET",
            headers: {  'Content-Type': 'application/json', 
                        'Access-Token': accessToken}
        });

        if (response.status === 401 || response.status === 422) { 
            console.log("Нужно обновить токен (refresh)");
            await refreshToken();

        } else if (response.status === 500) {
            console.log("Виноват бэкэндер")

        } else {
            const data = await response.json();
            console.log(data)
            localStorage.setItem("nickname", data.nickname);
            localStorage.setItem("avatar", data.avatar_url);
            localStorage.setItem("chats", data.chats);  
            if (window.location.pathname == "/app.html") load_contacts_and_profile();
        }
    } else {
        await refreshToken();
    }
}

async function refreshToken() {
    const refreshToken = localStorage.getItem("refreshToken");

    if (refreshToken != null) {
        const response = await fetch('http://localhost/api/update_token', {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'token': refreshToken })
        });
        console.log(response.status)
        if (response.status === 200) {
            const data = await response.json();
            localStorage.setItem("accessToken", data.access_token);
            localStorage.setItem("refreshToken", data.refresh_token);

        } else if (response.status === 500) {
            console.log("Iternal server error");
            // TODO сделай функцию которая будет показывать ошибку на фронте
        }
    }
    if (window.location.pathname != "/index.html") window.location.replace("index.html");
    create_sign_in_container();
}