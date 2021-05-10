<template>
  <br>
<!--  ALERT ACTION TOOLBAR -->
  <TheAlertActionToolbar/>
  <br>
<!--    FILTER ALERTS TOOLBAR -->
  <TheFilterToolbar/>
  <br>
<!--  ALERTS DATA TABLE-->
  <div class="card">
    <TheAlertsTable/>
  </div>
</template>

<script>
import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar";
import TheFilterToolbar from "@/components/Filters/TheFilterToolbar";
import TheAlertsTable from "@/components/Alerts/TheAlertsTable";

export default { components: { TheAlertsTable, TheFilterToolbar, TheAlertActionToolbar } }
</script>