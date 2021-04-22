<template>
  <br>
  <Toolbar>
    <template #left>
      <Button class="p-m-1 p-button-normal p-button-success" icon="pi pi-thumbs-up" label="Disposition"
              @click="openDispositionModal"/>
      <Dialog header="Header" v-model:visible="displayDispositionModal" :style="{width: '50vw'}" :modal="true">
        <p class="p-m-0">Disposition</p>
        <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeDispositionModal" class="p-button-text"/>
          <Button label="Yes" icon="pi pi-check" @click="closeDispositionModal" autofocus/>
        </template>
      </Dialog>
      <Dialog header="Header" v-model:visible="displaySaveToEventModal" :style="{width: '50vw'}" :modal="true" @click="openSaveToEventModal">
        <p class="p-m-0">Disposition</p>
        <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeSaveToEventModal" class="p-button-text"/>
          <Button label="Yes" icon="pi pi-check" @click="closeSaveToEventModal" autofocus/>
        </template>
      </Dialog>
      <Button class="p-m-1 p-button-sm" icon="pi pi-comment" label="Comment" @click="openCommentModal"/>
      <Dialog header="Header" v-model:visible="displayCommentModal" :style="{width: '50vw'}" :modal="true">
        <p class="p-m-0">Comment.</p>
        <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeCommentModal" class="p-button-text"/>
          <Button label="Yes" icon="pi pi-check" @click="closeCommentModal" autofocus/>
        </template>
      </Dialog>
      <Button class="p-m-1 p-button-sm" icon="pi pi-briefcase" label="Take Ownership"/>
      <Button class="p-m-1 p-button-sm" icon="pi pi-user" label="Assign" @click="openAssignModal"/>
      <Dialog header="Header" v-model:visible="displayAssignModal" :style="{width: '50vw'}" :modal="true">
        <p class="p-m-0">Assign.</p>
        <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeAssignModal" class="p-button-text"/>
          <Button label="Yes" icon="pi pi-check" @click="closeAssignModal" autofocus/>
        </template>
      </Dialog>
      <Button class="p-m-1 p-button-sm" icon="pi pi-tags" label="Tag" @click="openTagModal"/>
      <Dialog header="Header" v-model:visible="displayTagModal" :style="{width: '50vw'}" :modal="true">
        <p class="p-m-0">Tag.</p>
        <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeTagModal" class="p-button-text"/>
          <Button label="Yes" icon="pi pi-check" @click="closeTagModal" autofocus/>
        </template>
      </Dialog>
      <Button class="p-m-1 p-button-sm" icon="pi pi-times-circle" label="Remediate" @click="openRemediateModal"/>
      <Dialog header="Header" v-model:visible="displayRemediateModal" :style="{width: '50vw'}" :modal="true">
        <p class="p-m-0">Remediate.</p>
        <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeRemediateModal" class="p-button-text"/>
          <Button label="Yes" icon="pi pi-check" @click="closeRemediateModal" autofocus/>
        </template>
      </Dialog>
      <Button class="p-m-1 p-button-sm p-button-danger" icon="pi pi-trash" label="Delete" @click="openConfirmation"/>
      <Dialog header="Confirmation" v-model:visible="displayConfirmation" :style="{width: '350px'}" :modal="true">
        <div class="confirmation-content">
          <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem"/>
          <span>Are you sure you want to proceed?</span>
        </div>
        <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeConfirmation" class="p-button-text"/>
          <Button label="Yes" icon="pi pi-check" @click="closeConfirmation" class="p-button-text" autofocus/>
        </template>
      </Dialog>

    </template>
    <template #right>
      <Button icon="pi pi-link" class="p-button-rounded"/>

    </template>
  </Toolbar>
  <br>
  <Toolbar>
    <template #left>
      <Calendar class="p-m-1" id="time24" v-model="calendarData" :manualInput="false" :showTime="true"
                selectionMode="range"
                :showSeconds="true" :showIcon="true" style="width: 375px"/>
      <Button type="button" icon="pi pi-filter"
              label="Edit" class="p-button-outlined p-m-1" style="float: right" @click="openEditFilterModal"/>
      <Dialog header="Header" v-model:visible="displayEditFilterModal" :style="{width: '50vw'}" :modal="true">
        <p class="p-m-0">Edit Filters.</p>
        <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeEditFilterModal" class="p-button-text"/>
          <Button label="Yes" icon="pi pi-check" @click="closeEditFilterModal" autofocus/>
        </template>
      </Dialog>
    </template>
    <template #right>
      <Button type="button" icon="pi pi-filter-slash"
              label="Clear" class="p-button-outlined p-m-1"/>
      <Button type="button" icon="pi pi-refresh"
              label="Reset" class="p-button-outlined p-m-1"/>
    </template>
  </Toolbar>
  <br>
  <div class="card">
    <DataTable :value="alerts"
               responsiveLayout="scroll"
               :paginator="true"
               :rows="5"
               paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
               :rowsPerPageOptions="[5,10,50]"
               currentPageReportTemplate="Showing {first} to {last} of {totalRecords}"
               sortField="name"
               :sortOrder="1"
               removableSort
               :globalFilterFields="['global',
                                      'name',
                                      'alert_date',
                                      'type',
                                      'disposition',
                                      'disposition_by',
                                      'event_date',
                                      'owner',
                                      'queue',
                                      'remediated_by',
                                      'remediated_date',
                                      'remediation_status']"
               v-model:filters="alertNarrowFilters"
               filterDisplay="menu"
               v-model:selection="selectedAlerts"
               dataKey="code"
               v-model:expandedRows="expandedRows"
               ref="dt"
               :resizableColumns="true"
               columnResizeMode="fit">

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
              <InputText v-model="alertNarrowFilters['global'].value" placeholder="Search in table"/>
          </span>
            <Button icon="pi pi-refresh" class="p-button-rounded p-m-1" @click="clearFilter1()"/>
            <Button class="p-button-rounded p-m-1" icon="pi pi-download" @click="exportCSV($event)"/>

          </template>

        </Toolbar>
      </template>

      <Column id="alert-expand" :expander="true" headerStyle="width: 3rem"/>
      <Column id="alert-select" selectionMode="multiple" headerStyle="width: 3em"/>
      <Column v-for="(col, index) of selectedColumns" :field="col.field" :header="col.header"
              :key="col.field + '_' + index" :sortable="true">
        <template #body="{data}">
          <div v-if="col.field === 'name'">
            <span class="p-m-1"> {{ data.name }}</span>
            <br>
            <span>
            <Tag v-for="tag in data.tags" :key="tag" class="p-mr-2" rounded>{{ tag }}</Tag>
            </span></div>
          <span v-else> {{ data.name }}</span>
        </template>
        <template #filter="{filterModel}">
          <InputText v-if="col.field === 'name'" InputText type="text" v-model="filterModel.value"
                     class="p-column-filter" placeholder="Search by name"/>
          <InputText v-if="col.field === 'tag'" InputText type="text" v-model="filterModel.value"
                     class="p-column-filter" placeholder="Search by tag"/>
          <Calendar
              v-else-if="col.field === 'alert_date' || col.field === 'event_date' || col.field === 'remediated_date'"
              v-model="filterModel.value" dateFormat="mm/dd/yy" placeholder="mm/dd/yyyy HH:MM:SS" :showTime="true"
              :showSeconds="true"/>
          <MultiSelect
              v-else-if="col.field === 'disposition_by' || col.field === 'owner' || col.field === 'remediated_by'"
              v-model="filterModel.value" :options="users" optionLabel="col.header" placeholder="Any"
              class="p-column-filter">
            <template #option="slotProps">
              <span>{{ slotProps.option }}</span>
            </template>
          </MultiSelect>
          <MultiSelect v-else-if="col.field === 'disposition'" v-model="filterModel.value" :options="dispositions"
                       optionLabel="col.header" placeholder="Any" class="p-column-filter">
            <template #option="slotProps">
              <span>{{ slotProps.option }}</span>
            </template>
          </MultiSelect>
          <MultiSelect v-else-if="col.field === 'type'" v-model="filterModel.value" :options="types"
                       optionLabel="col.header" placeholder="Any" class="p-column-filter">
            <template #option="slotProps">
              <span>{{ slotProps.option }}</span>
            </template>
          </MultiSelect>
          <MultiSelect v-else-if="col.field === 'queue'" v-model="filterModel.value" :options="queues"
                       optionLabel="col.header" placeholder="Any" class="p-column-filter">
            <template #option="slotProps">
              <span>{{ slotProps.option }}</span>
            </template>
          </MultiSelect>
          <MultiSelect v-else-if="col.field === 'remediation_status'" v-model="filterModel.value"
                       :options="remediation_statuses" optionLabel="col.header" placeholder="Any"
                       class="p-column-filter">
            <template #option="slotProps">
              <span>{{ slotProps.option }}</span>
            </template>
          </MultiSelect>
        </template>

      </Column>
      <template #expansion="slotProps">
        <h5>Observables:</h5>
        <ul>
          <li v-for="obs of slotProps.data.observables" :key="obs.value">{{ obs.type }} - {{ obs.value }}</li>
        </ul>
      </template>

    </DataTable>
  </div>
</template>

<script>

import {FilterMatchMode, FilterOperator} from 'primevue/api';


export default {
  data() {
    return {
      calendarData: null,
      selectedOwners: null,
      users: ['Holly', 'Analyst', 'none'],
      selectedQueues: null,
      queues: ['external', 'internal', 'intel'],
      dispositions: ['FALSE_POSITIVE', 'WEAPONIZATION', 'COMMAND_AND_CONTROL'],
      types: ['splunk_hunter'],
      remediation_statuses: ['remediated', 'remediation_failed', 'remediating'],
      columns: [
        {field: 'alert_date', header: 'Alert Date'},
        {field: 'name', header: 'Name'},
        {field: 'type', header: 'Type'},
        {field: 'owner', header: 'Owner'},
        {field: 'disposition', header: 'Disposition'},
        {field: 'disposition_by', header: 'Dispositioned By'},
        {field: 'event_date', header: 'Event Date'},
        {field: 'queue', header: 'Queue'},
        {field: 'remediated_by', header: 'Remediated By'},
        {field: 'remediated_date', header: 'Remediated Date'},
        {field: 'remediation_status', header: 'Remediation Status'},
      ],
      alerts: [
        {
          "id": "1000",
          "alert_date": "04/20/2020 T2:00:00",
          "name": "Splunk Hunt: Example",
          "type": "splunk_hunter",
          "disposition": "FALSE_POSITIVE",
          "disposition_by": "Holly",
          "event_date": "04/20/2020 T2:00:00",
          "owner": "Holly",
          "queue": "default",
          "remediated_by": "Holly",
          "remediated_date": "04/20/2020 T2:00:00",
          "remediation_status": "remediated",
          "tags": ['bad', 'malware', 'oh_no'],
          "observables": [{'type': 'URL', 'value': 'http://www.google.com'},
            {'type': 'FQDN', 'value': 'google.com'},]
        },
      ],
      selectedColumns: null,
      selectedAlerts: null,
      alertNarrowFilters: null,
      displayCommentModal: false,
      displayDispositionModal: false,
      displaySaveToEventModal: false,
      displayAssignModal: false,
      displayTagModal: false,
      displayEditFilterModal: false,
      displayRemediateModal: false,
      displayConfirmation: false,
      expandedRows: []
    }
  },
  created() {
    this.initAlertNarrowFilters();
    this.selectedColumns = this.columns.slice(0, 5);
  },
  methods: {
    clearFilter1() {
      this.initAlertNarrowFilters();
    },
    resetFilters() {
      this.initAlertNarrowFilters();
    },
    initAlertNarrowFilters() {
      this.alertNarrowFilters = {
        'global': {value: null, matchMode: FilterMatchMode.CONTAINS},
        'name': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
        'alert_date': {
          operator: FilterOperator.AND,
          constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]
        },
        'type': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
        'disposition': {
          operator: FilterOperator.AND,
          constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]
        },
        'disposition_by': {
          operator: FilterOperator.AND,
          constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]
        },
        'event_date': {
          operator: FilterOperator.AND,
          constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]
        },
        'owner': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
        'queue': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
        'remediated_by': {
          operator: FilterOperator.AND,
          constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]
        },
        'remediated_date': {
          operator: FilterOperator.AND,
          constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]
        },
        'remediation_status': {
          operator: FilterOperator.AND,
          constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]
        },
        'tag': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
      }
    },
    onToggle(value) {
      this.selectedColumns = this.columns.filter(col => value.includes(col));
    },
    exportCSV() {
      this.$refs.dt.exportCSV();
    },
    openDispositionModal() {
      this.displayDispositionModal = true;
    },
    closeDispositionModal() {
      this.displayDispositionModal = false;
    },
    openCommentModal() {
      this.displayCommentModal = true;
    },
    closeCommentModal() {
      this.displayCommentModal = false;
    },
    openAssignModal() {
      this.displayAssignModal = true;
    },
    closeAssignModal() {
      this.displayAssignModal = false;
    },
    openTagModal() {
      this.displayTagModal = true;
    },
    closeTagModal() {
      this.displayTagModal = false;
    },
    openRemediateModal() {
      this.displayRemediateModal = true;
    },
    closeRemediateModal() {
      this.displayRemediateModal = false;
    },
    openEditFilterModal() {
      this.displayEditFilterModal = true;
    },
    closeEditFilterModal() {
      this.displayEditFilterModal = false;
    },
    openSaveToEventModal() {
      this.displaySaveToEventModal = true;
    },
    closeSaveToEventModal() {
      this.displaySaveToEventModal = false;
    },
    openConfirmation() {
      this.displayConfirmation = true;
    },
    closeConfirmation() {
      this.displayConfirmation = false;
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