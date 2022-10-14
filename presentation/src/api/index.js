import axios from 'axios';

const instance = axios.create({
    // baseURL: 'https://peaceful-refuge-43675.herokuapp.com/api/',
    baseURL: 'http://127.0.0.1:5001/',
    
});


export default instance;