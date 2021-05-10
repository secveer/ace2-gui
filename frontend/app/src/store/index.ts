import { createStore } from "vuex";

import modals from './modals'
import selectedAlerts from './selectedAlerts'

// todo: add selectedAlerts to store
// probably also want to add applied filters.

export default createStore({
  state: {},
  mutations: {},
  actions: {},
  modules: {modals, selectedAlerts},
});
