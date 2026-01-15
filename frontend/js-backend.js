let accessToken = null;

async function login(username, password) {
    const response = await fetch('http://localhost:8000/auth', {
        method: 'POST',
        body: JSON.stringify({ username, password })
    });
    if (response.status === 422) {
        console.log("Виноват фронтендер")
    } else if (response.status === 404) { 
        registration_account()
    } else if (response.status === 505) {
        console.log("Виноват бэкэндер")
    } else {
        const data = await response.json();
    // Сохраняем access token только в памяти приложения
        accessToken = data.access_token;
        refresh_token = data.refresh_token
    }
    
    
}

async function getProtectedData() {
    const response = await fetch('http://localhost:8000/user/data', {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    });

    if (response.status === 401) {
        console.log("Нужно обновить токен (refresh)");
    // Здесь вызывается функция обновления токена через куку
        refreshToken()
    } else if (response.status === 422) {
        console.log("Виноват фронтендер")
    } else if (response.status === 500) {
        console.log("Виноват бэкэндер")
    } else {
        const data = await response.json();
        console.log(data);
    }
}

async function refreshToken() {
    const response = await fetch('http://localhost:8000/update_token', {
        headers: {
            'Authorization': `Bearer ${refresh_token}`
        }
    });

    if (response.status === 500) {
        console.log("Виноват бэкэндер")
    } else {
        const data = await response.json();
    // Сохраняем access token только в памяти приложения
        accessToken = data.access_token;
        refresh_token = data.refresh_token
    }
}