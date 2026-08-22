import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/styles/main.css';
import './assets/styles/markdown.css';

createApp(App).use(router).mount('#app');
