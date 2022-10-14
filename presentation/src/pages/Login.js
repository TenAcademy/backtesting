import React, { useState } from 'react'
import "./Login.css"
import axiosInstance from '../api';





let changeForm = (e) => {

    let switchCtn = document.querySelector("#switch-cnt");
    let switchC1 = document.querySelector("#switch-c1");
    let switchC2 = document.querySelector("#switch-c2");
    let switchCircle = document.querySelectorAll(".switch__circle");
    let switchBtn = document.querySelectorAll(".switch-btn");
    let aContainer = document.querySelector("#a-container");
    let bContainer = document.querySelector("#b-container");
    let allButtons = document.querySelectorAll(".submit");

    switchCtn.classList.add("is-gx");
    setTimeout(function(){
        switchCtn.classList.remove("is-gx");
    }, 1500)

    switchCtn.classList.toggle("is-txr");
    switchCircle[0].classList.toggle("is-txr");
    switchCircle[1].classList.toggle("is-txr");

    switchC1.classList.toggle("is-hidden");
    switchC2.classList.toggle("is-hidden");
    aContainer.classList.toggle("is-txl");
    bContainer.classList.toggle("is-txl");
    bContainer.classList.toggle("is-z200");
}


const Login = () => {
    const [msg, setmsg] = useState("")

    const login = async (e)=>{

        e.preventDefault()
        let email = document.querySelector("#email").value
        let password = document.querySelector("#password").value
    
        let user={
            "email":email,
            "password":password
        }
    
        let result = await axiosInstance.post("/userSession",user)
        let success = result.data.Success
    
        if(success){
            // window.alert("Success")
            window.localStorage.clear()
            window.localStorage("user",email)
            window.location="/"
        }
        else{
            // window.alert("error")
            setmsg("Wrong user name / password")
        }
    
    }
    
    const signup = async (e)=>{

        e.preventDefault()
        let name = document.querySelector("#fullName").value
        let email = document.querySelector("#newEmail").value
        let password = document.querySelector("#newPassword").value
    
        let user={
            "fullName":name,
            "email":email,
            "password":password
        }

        let response = await axiosInstance.post("/register",user)

        let data = response.data
        if(data.Success){

            window.location="/"
        }
        else{
            window.alert("Error handling your request")
        }
    
    }

    return (
        <div>

            <div class="main">
                <div class="container a-container" id="a-container">
                    <form class="form" id="a-form" onSubmit={signup} method="" action="">
                        <h2 class="form_title title">Create Account</h2>
                        <input class="form__input" type="text" required id="fullName" placeholder="Name"/>
                        <input class="form__input" type="text" required id="newEmail" placeholder="Email"/>
                        <input class="form__input" type="password" required id="newPassword" placeholder="Password"/>
                        <button class="form__button button submit">SIGN UP</button>
                    </form>
                </div>
                <div class="container b-container" id="b-container">
                    <form class="form" id="b-form" onSubmit={login} method="" action="">
                        <h2 class="form_title title">Sign in to Website</h2>
                        <p style={{"color":"red"}}>{msg}</p>
                        <input class="form__input" id="email" required type="text" placeholder="Email"/>
                        <input class="form__input" id="password" required type="password" placeholder="Password"/>
                        <button class="form__button button submit">SIGN IN</button>
                    </form>
                </div>
                <div class="switch" id="switch-cnt">
                    <div class="switch__circle"></div>
                    <div class="switch__circle switch__circle--t"></div>
                    <div class="switch__container" id="switch-c1">
                        <h2 class="switch__title title">Welcome Back !</h2>
                        <p class="switch__description description">To keep connected with us please login with your personal info</p>
                        <button class="switch__button button switch-btn" onClick={changeForm}>SIGN IN</button>
                    </div>
                    <div class="switch__container is-hidden" id="switch-c2">
                        <h2 class="switch__title title">Hello Friend !</h2>
                        <p class="switch__description description">Enter your personal details and start journey with us</p>
                        <button class="switch__button button switch-btn" onClick={changeForm}>SIGN UP</button>
                    </div>
                </div>
            </div>

        </div>
            )
}

export default Login