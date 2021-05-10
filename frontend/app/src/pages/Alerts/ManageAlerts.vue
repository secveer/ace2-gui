<template>
  <br>
<!--  ALERT ACTION TOOLBAR -->
  <TheAlertActionToolbar></TheAlertActionToolbar>
  <br>
<!--    FILTER ALERTS TOOLBAR -->
  <TheFilterToolbar></TheFilterToolbar>
  <br>
<!--  ALERTS DATA TABLE-->
  <div class="card">
    <TheAlertsTable></TheAlertsTable>
  </div>
</template>

<script>
import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar";
import TheFilterToolbar from "@/components/Filters/TheFilterToolbar";
import TheAlertsTable from "@/components/Alerts/TheAlertsTable";

export default { components: { TheAlertsTable, TheFilterToolbar, TheAlertActionToolbar } }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
a {
  color: #42b983;
}
</style>