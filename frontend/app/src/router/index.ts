import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import ManageAlerts from "../pages/Alerts/ManageAlerts.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/manage_alerts",
    name: "Manage Alerts",
    component: ManageAlerts,
  },
  {
    path: "/",
    redirect: "/manage_alerts",
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
