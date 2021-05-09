<template>
  <br>
<!--  ALERT ACTION TOOLBAR -->
  <TheAlertActionToolbar
  :selected-alerts="selectedAlerts">
  </TheAlertActionToolbar>
  <br>
<!--    FILTER ALERTS TOOLBAR -->
  <TheFiltersToolbar></TheFiltersToolbar>
  <br>
<!--  ALERTS DATA TABLE-->
  <div class="card">
    <TheAlertsTable
        :alerts="alerts"
        @alert-select="alertSelect"
        @alert-unselect="alertUnselect"
        @alert-select-all="alertSelectAll"
        @alert-unselect-all="alertUnselectAll">
    </TheAlertsTable>
  </div>
</template>

<script>

import axios from 'axios';

import TheAlertActionToolbar from "@/components/TheAlertActionToolbar";
import TheFiltersToolbar from "@/components/TheFiltersToolbar";
import TheAlertsTable from "@/components/TheAlertsTable";

export default {
  components: {TheAlertsTable, TheFiltersToolbar, TheAlertActionToolbar},
  data() {
    return {
      alerts: [],
      appliedFilters: [],
      selectedAlerts: []
    }
  },
  async created() {
    // Fetch alerts from the backend API
    const response = await axios.get(`${process.env.VUE_APP_BACKEND_URL}/alert`).catch(error => {
      console.error(error);
    });

    if (response && response.status === 200) {
      this.alerts = response.data;
    }
  },
  computed: {
    tags: function () {
      let tags = [];
      let unique_tags = [];
      this.alerts.forEach(function(alert) {
        tags = tags.concat(alert.tags);
      });
      tags.forEach((tag) => {
        if (!unique_tags.includes(tag)) {
          unique_tags.push(tag);
        }
      });
      // todo: modify tags in alert object to be objects rather than a string
      // this will allow for proper filtering
      return unique_tags;
    }
  },
  methods: {
    alertSelect(alert) {
      this.selectedAlerts.push(alert)
    },
    alertUnselect(alert) {
      this.selectedAlerts = this.selectedAlerts.filter(a => a.id !== alert.id);
    },
    alertSelectAll(alerts){
      this.selectedAlerts = alerts;
    },
    alertUnselectAll(){
      this.selectedAlerts = [];
    },

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
a {
  color: #42b983;
}
</style>