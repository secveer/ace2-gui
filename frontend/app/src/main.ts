import { createApp } from "vue";
import App from "./App.vue";
import PrimeVue from 'primevue/config';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import MultiSelect from 'primevue/multiselect';
import Toolbar from 'primevue/toolbar';
import Dialog from 'primevue/dialog';
import SplitButton from 'primevue/splitbutton';
import Menubar from 'primevue/menubar';
import Tag from 'primevue/tag';
import Badge from 'primevue/badge';
import Calendar from 'primevue/calendar';
import Checkbox from 'primevue/checkbox';
import Dropdown from 'primevue/dropdown';
import RadioButton from 'primevue/radiobutton';
import Divider from 'primevue/divider';
import Textarea from 'primevue/textarea';
import Chips from 'primevue/chips';

import AutoComplete from 'primevue/autocomplete';



import router from "./router";
import store from "./store";


import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';

const app = createApp(App).use(store).use(router).use(PrimeVue);
app.component('Button', Button);
app.component('InputText', InputText);
app.component('MultiSelect', MultiSelect);
app.component('DataTable', DataTable);
app.component('SplitButton', SplitButton);
app.component('Dialog', Dialog);
app.component('Menubar', Menubar);
app.component('Checkbox', Checkbox);
app.component('AutoComplete', AutoComplete);
app.component('RadioButton', RadioButton);
app.component('Chips', Chips);
app.component('Dropdown', Dropdown);
app.component('Calendar', Calendar);
app.component('Divider', Divider);
app.component('Tag', Tag);
app.component('Textarea', Textarea);
app.component('Toolbar', Toolbar);
app.component('Badge', Badge);
app.component('Column', Column);

app.mount("#app");