import { createApp } from "vue";
import App from "./App.vue";
import PrimeVue from 'primevue/config';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import MultiSelect from 'primevue/multiselect';
import router from "./router";
import store from "./store";


import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

const app = createApp(App).use(store).use(router).use(PrimeVue);
app.component('Button', Button);
app.component('InputText', InputText);
app.component('MultiSelect', MultiSelect);
app.component('DataTable', DataTable);
app.component('Column', Column);
app.mount("#app");