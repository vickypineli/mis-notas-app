import config from "@/config.js";



export async function login(user, password) {
    const settings = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user: user,
            password: password,
        }),

    };

    
    const response = await fetch(`${config.AUTH_PATH}/login`, settings);
    return response
}

