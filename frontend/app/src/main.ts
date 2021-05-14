import { createApp } from "vue";
import App from "./App.vue";
import PrimeVue from "primevue/config";

import router from "./router";
import store from "./store";

import "primeflex/primeflex.css";
import "primeicons/primeicons.css";
import "primevue/resources/primevue.min.css";
import "primevue/resources/themes/saga-blue/theme.css";

const app = createApp(App).use(store).use(router).use(PrimeVue);

app.mount("#app");
