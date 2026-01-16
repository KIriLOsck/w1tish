async function registration(username, email, password) {
    const response = await fetch('http://127.0.0.1:8000/reg', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    })
    
    if (response.status === 200) {
        await login(username, password)
    } else {
        console.log("Ошибка: ", response.status)
    }
}

async function login(username, password) {
    const response = await fetch('http://127.0.0.1:8000/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    if (response.status === 422) {
        console.log("Виноват фронтендер")
    } else if (response.status === 404) { 
        error_text.textContent = "Вы не зарегистрированы"
        create_registration_container()
    } else if (response.status === 505) {
        console.log("Виноват бэкэндер")
    } else {
        const data = await response.json();
    // Сохраняем access token только в памяти приложения
        localStorage.setItem("accessToken", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        await getProtectedData(localStorage.getItem("accessToken"))
    }
}

async function getProtectedData(token) {
    const response = await fetch('http://localhost:8000/user/data', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token }) //проверяй не undefined ли токен
    });

    if (response.status === 401 || response.status === 422) { //422 это когда токена нету куттулу а не когда его надо обновить исправляй давай
        console.log("Нужно обновить токен (refresh)");
    // Здесь вызывается функция обновления токена через куку
        await refreshToken(localStorage.getItem("refresh_token"))
    } else if (response.status === 500) {
        console.log("Виноват бэкэндер") // TODO обработать ошибку 422 как ошибку фронтендера
    } else {
        const data = await response.json();
        console.log(data);
    }
}

async function refreshToken(refresh_token) {
    const response = await fetch('http://localhost:8000/update_token', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh_token })
        
    });

    if (response.status === 500) {
        console.log("Виноват бэкэндер")
    } else if (response.status === 422 || response.status === 401) { //опять же 401 это протухший токен а 422 критическая ошибка фронтенда
        create_sign_in_container()
    } else {
        const data = await response.json();
    // Сохраняем access token только в памяти приложения
        localStorage.setItem("accessToken", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        await getProtectedData(localStorage.getItem("accessToken"))}
}