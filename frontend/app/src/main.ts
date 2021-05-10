import { createApp } from "vue";
import App from "./App.vue";
import Button from "primevue/button";
import Calendar from "primevue/calendar";
import Chips from "primevue/chips";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import Dialog from "primevue/dialog";
import Dropdown from "primevue/dropdown";
import InputText from "primevue/inputtext";
import Menubar from "primevue/menubar";
import MultiSelect from "primevue/multiselect";
import PrimeVue from "primevue/config";
import RadioButton from "primevue/radiobutton";
import TabPanel from "primevue/tabpanel";
import TabView from "primevue/tabview";
import Tag from "primevue/tag";
import Textarea from "primevue/textarea";
import Toolbar from "primevue/toolbar";

import router from "./router";
import store from "./store";

import "primeflex/primeflex.css";
import "primeicons/primeicons.css";
import "primevue/resources/primevue.min.css";
import "primevue/resources/themes/saga-blue/theme.css";

const app = createApp(App).use(store).use(router).use(PrimeVue);
app.component("Button", Button);
app.component("Calendar", Calendar);
app.component("Chips", Chips);
app.component("Column", Column);
app.component("DataTable", DataTable);
app.component("Dialog", Dialog);
app.component("Dropdown", Dropdown);
app.component("InputText", InputText);
app.component("Menubar", Menubar);
app.component("MultiSelect", MultiSelect);
app.component("RadioButton", RadioButton);
app.component("TabPanel", TabPanel);
app.component("TabView", TabView);
app.component("Tag", Tag);
app.component("Textarea", Textarea);
app.component("Toolbar", Toolbar);

app.mount("#app");
