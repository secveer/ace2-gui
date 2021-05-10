<template>
  <DataTable :value="alerts"
             :globalFilterFields="[ 'alert_date',
                                      'disposition',
                                      'disposition_by',
                                      'event_date',
                                      'name',
                                      'owner',
                                      'queue',
                                      'remediated_by',
                                      'remediated_date',
                                      'remediation_status',
                                      'type']"
             :paginator="true"
             :resizableColumns="true"
             :rows="10"
             :rowsPerPageOptions="[5,10,50]"
             :sortOrder="1"
             columnResizeMode="fit"
             currentPageReportTemplate="Showing {first} to {last} of {totalRecords}"
             dataKey="id"
             paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
             ref="dt"
             removableSort
             responsiveLayout="scroll"
             sortField="name"
             v-model:expandedRows="expandedRows"
             v-model:filters="alertTableFilters"
             v-model:selection="selectedRows"
             @row-select="alertSelect($event.data)"
             @row-unselect="alertUnselect($event.data)"
             @row-select-all="alertSelectAll"
             @row-unselect-all="alertUnselectAll">

    <!--        ALERT TABLE TOOLBAR-->
    <template #header>
      <Toolbar style="border: none">
        <template #left>
          <MultiSelect :modelValue="selectedColumns"
                       :options="columns"
                       optionLabel="header"
                       @update:modelValue="onToggle"
                       placeholder="Select Columns"/>
        </template>
        <template #right>
            <span class="p-input-icon-left p-m-1">
              <i class="pi pi-search"/>
              <InputText v-model="alertTableFilters['global'].value" placeholder="Search in table"/>
          </span>
          <!--            CLEAR TABLE FILTERS -->
          <Button icon="pi pi-refresh" class="p-button-rounded p-m-1" @click="resetAlertTableFilters()"/>
          <!--            EXPORT TABLE -->
          <Button class="p-button-rounded p-m-1" icon="pi pi-download" @click="exportCSV($event)"/>

        </template>

      </Toolbar>
    </template>
    <!-- DROPDOWN COLUMN-->
    <Column id="alert-expand" :expander="true" headerStyle="width: 3rem"/>
    <!--      CHECKBOX COLUMN -->
    <Column id="alert-select" selectionMode="multiple" headerStyle="width: 3em"/>
    <!--      DATA COLUMN -->
    <Column v-for="(col, index) of selectedColumns" :field="col.field" :header="col.header"
            :key="col.field + '_' + index" :sortable="true">
      <!--        DATA COLUMN BODY-->
      <template #body="{data}">
        <!--          NAME COLUMN - HAS TAGS AND TODO: ALERT ICONS-->
        <div v-if="col.field === 'name'">
          <span class="p-m-1"> {{ data.name }}</span>
          <br>
          <span>
            <Tag v-for="tag in data.tags" :key="tag" class="p-mr-2" rounded>{{ tag }}</Tag>
            </span></div>
        <span v-else> {{ data[col.field] }}</span>
      </template>
    </Column>
    <!--      ALERT ROW DROPDOWN -->
    <template #expansion="slotProps">
      <h5>Observables:</h5>
      <ul>
        <li v-for="obs of slotProps.data.observables" :key="obs.value">{{ obs.type }} - {{ obs.value }}</li>
      </ul>
    </template>
  </DataTable>
</template>

<script>
import {FilterMatchMode} from "primevue/api";
import axios from "axios";

export default {
  name: "TheAlertsTable",

  emits: ['alertSelect',
          'alertUnselect',
          'alertSelectAll',
          'alertUnselectAll'],

  data() {
    return {
      alerts: [],
      alertTableFilters: null,
      columns: [{field: 'alert_date', header: 'Alert Date'},
        {field: 'name', header: 'Name'},
        {field: 'disposition', header: 'Disposition'},
        {field: 'owner', header: 'Owner'},
        {field: 'type', header: 'Type'},
        {field: 'disposition_by', header: 'Dispositioned By'},
        {field: 'event_date', header: 'Event Date'},
        {field: 'queue', header: 'Queue'},
        {field: 'remediated_by', header: 'Remediated By'},
        {field: 'remediated_date', header: 'Remediated Date'},
        {field: 'remediation_status', header: 'Remediation Status'},
      ],
      expandedRows: [],
      selectedColumns: null,
      selectedRows: null,
    }
  },
  async created() {
    this.resetAlertTableFilters();

    // Fetch alerts from the backend API
    const response = await axios.get(`${process.env.VUE_APP_BACKEND_URL}/alert`).catch(error => {
      console.error(error);
    });

    if (response && response.status === 200) {
      this.alerts = response.data;
    }

  },
  methods: {
    resetAlertTableFilters() {
      this.initAlertTableFilters();
      this.selectedColumns = this.columns.slice(0, 5);
    },
    initAlertTableFilters() {
      this.alertTableFilters = {
        'global': {value: null, matchMode: FilterMatchMode.CONTAINS}
      }
    },
    onToggle(value) {
      this.selectedColumns = this.columns.filter(col => value.includes(col));
    },
    exportCSV() {
      this.$refs.dt.exportCSV();
    },
    alertSelect(alert) {
      this.$store.dispatch("selectedAlerts/select", alert);
    },
    alertUnselect(alert) {
      this.$store.dispatch("selectedAlerts/unselect", alert);
    },
    alertSelectAll(){
      this.$store.dispatch("selectedAlerts/selectAll", this.alerts);
    },
    alertUnselectAll(){
      this.$store.dispatch("selectedAlerts/unselectAll");
    }
  }
}
</script>

<style scoped>
</style>