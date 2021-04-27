<template>
  <br>
<!--  ALERT ACTION TOOLBAR -->
  <Toolbar>
    <template #left>
<!--      DISPOSITION -->
      <Button class="p-m-1 p-button-normal p-button-success" icon="pi pi-thumbs-up" label="Disposition"
              @click="openDispositionModal"/>
      <Dialog header="Set Disposition" v-model:visible="displayDispositionModal" :style="{width: '50vw'}" :modal="true">
        <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
          <div class="p-field p-col">
            <div v-for="disposition of dispositions" :key="disposition" class="p-field-radiobutton p-inputgroup">
              <RadioButton :id="disposition" name="disposition" :value="disposition" v-model="appliedDisposition"/>
              <label :for="disposition">{{ disposition }}</label>
            </div>
          </div>
          <div class="p-field p-col">
            <Textarea v-model="appliedComment" :autoResize="true" rows="5" cols="30" placeholder="Add a comment..."/>
            <Dropdown v-model="appliedComment" :options="suggestedComments" :showClear="true" placeholder="Select from a past comment" />
          </div>
          </div>
        <template #footer>
          <Button label="Save" class="p-button-outlined" @click="closeDispositionModal"/>
          <Button v-if="showAddToEventButton" label="Save to Event" class="p-button-raised" @click="closeDispositionModal();openSaveToEventModal();autoSetEventName();" autofocus/>
        </template>
      </Dialog>
<!--      SAVE TO EVENT -->
      <Dialog header="Save to Event" v-model:visible="displaySaveToEventModal" :style="{width: '50vw'}" :modal="true">
        <TabView class="p-m-1">
          <TabPanel v-for="event of events" :key="event.title" :header="event.title">
            <div v-for="eventItem of event.events" :key="eventItem" class="p-field-radiobutton p-inputgroup">
              <RadioButton :id="eventItem" name="eventItem" :value="eventItem" v-model="chosenEvent"/>
              <label :for="eventItem">{{ eventItem }}</label>
            </div>
            <div class="p-field-radiobutton p-inputgroup">
              <RadioButton id="newEventItem" name="newEventItem" value="New Event" v-model="chosenEvent"/>
              <label for="newEventItem">New Event</label>
            </div>
            <div v-if="newEventSelected" class="p-m-1 p-grid p-fluid p-formgrid">
              <div class="p-field p-col p-m-1">
              <InputText id="newEventName" type="text" v-model="newEventName"/>
              <Textarea v-model="newEventComment" :autoResize="true" rows="5" cols="30" id="newEventComment" placeholder="Add a comment..."/>
                <Dropdown v-model="newEventComment" :options="suggestedComments" :showClear="true"
                          placeholder="Select from a past comment"/>
              </div>
              <div class="p-col-1 p-m-1">
                <Button type="button" icon="pi pi-refresh"
                        class="p-button-outlined p-m-1" @click="autoSetEventName"/>
              </div>
            </div>
          </TabPanel>
        </TabView>
        <template #footer>
          <Button label="Back" icon="pi pi-arrow-left" @click="closeSaveToEventModal();openDispositionModal()" class="p-button-text"/>
          <Button label="Save" icon="pi pi-check" @click="closeSaveToEventModal" autofocus :disabled="!anyEventSelected"/>
        </template>
      </Dialog>
<!--      COMMENT -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-comment" label="Comment" @click="openCommentModal"/>
      <Dialog header="Add Comment" v-model:visible="displayCommentModal" :style="{width: '50vw'}" :modal="true">
        <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
          <div class="p-field p-col">
            <Textarea v-model="appliedComment" :autoResize="true" rows="5" cols="30" placeholder="Add a comment..."/>
            <Dropdown v-model="appliedComment" :options="suggestedComments" :showClear="true"
                      placeholder="Select from a past comment"/>
          </div>
        </div>
        <template #footer>
          <Button label="Nevermind" icon="pi pi-times" @click="closeCommentModal" class="p-button-text"/>
          <Button label="Add" icon="pi pi-check" @click="closeCommentModal" autofocus/>
        </template>
      </Dialog>
<!--      TAKE OWNERSHIP -- NO MODAL -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-briefcase" label="Take Ownership"/>
<!--      ASSIGN -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-user" label="Assign" @click="openAssignModal"/>
      <Dialog header="Assign Ownership" v-model:visible="displayAssignModal" :style="{width: '50vw'}" :modal="true">
        <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
          <div class="p-field p-col">
        <Dropdown v-model="selectedUser" :options="users"
                  placeholder="Select a user"/>
          </div>
        </div>
        <template #footer>
          <Button label="Nevermind" icon="pi pi-times" @click="closeAssignModal" class="p-button-text"/>
          <Button label="Assign" icon="pi pi-check" @click="closeAssignModal" autofocus/>
        </template>
      </Dialog>
<!--      TAG MODAL -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-tags" label="Tag" @click="openTagModal"/>
      <Dialog header="Add Tags" v-model:visible="displayTagModal" :style="{width: '50vw'}" :modal="true">
        <span class="p-fluid">
              <Chips v-model="newTags" />
              <Dropdown @change="addExistingTag" :options="tags" :filter="true" placeholder="Select from existing tags"
                        filterPlaceholder="Search tags" filterFields="options.value"/>
          </span>
        <template #footer>
          <Button label="Nevermind" icon="pi pi-times" @click="closeTagModal" class="p-button-text"/>
          <Button label="Add" icon="pi pi-check" @click="closeTagModal" autofocus/>
        </template>
      </Dialog>
<!--      REMEDIATE MODAL -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-times-circle" label="Remediate" @click="openRemediateModal"/>
      <Dialog header="Remediate" v-model:visible="displayRemediateModal" :style="{width: '50vw'}" :modal="true">
        <DataTable :value="remediation_targets"
                   responsiveLayout="scroll"
                   :rows="10"
                   sortField="type"
                   :sortOrder="1"
                   removableSort
                   dataKey="id"
                   v-model:selection="selectedRemediations"
                   stripedRows
                   columnResizeMode="fit">
          <Column id="remediation-select" selectionMode="multiple" headerStyle="width: 3em"/>
          <Column field="type" header="Type" :sortable="true"></Column>
          <Column field="target" header="Target" :sortable="true"></Column>
          <Column field="status" header="Status" :sortable="true"></Column>
        </DataTable>
        <template #footer>
          <Button label="Stop" class="p-button-text"/>
          <Button label="Remove" icon="pi pi-times" autofocus/>
          <Button label="Restore" icon="pi pi-check" autofocus/>
        </template>
      </Dialog>
<!--      DELETE ALERT -->
      <Button class="p-m-1 p-button-sm p-button-danger" icon="pi pi-trash" label="Delete" @click="openConfirmation"/>
      <Dialog header="Confirmation" v-model:visible="displayConfirmation" :style="{width: '350px'}" :modal="true">
        <div class="confirmation-content">
          <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem"/>
          <span>Are you sure you want to delete this alert?</span>
        </div>
        <template #footer>
          <Button label="Actually, no" icon="pi pi-times" @click="closeConfirmation" class="p-button-text"/>
          <Button label="Do it!" icon="pi pi-check" @click="closeConfirmation" class="p-button-text" autofocus/>
        </template>
      </Dialog>

    </template>
    <template #right>
      <Button icon="pi pi-link" class="p-button-rounded"/>

    </template>
  </Toolbar>
  <!--    FILTER ALERTS TOOLBAR -->
  <br>
  <Toolbar>
    <template #left>
      <Calendar class="p-m-1" id="time24" v-model="calendarData" :manualInput="false" :showTime="true"
                selectionMode="range"
                :showSeconds="true" :showIcon="true" style="width: 375px"/>
      <Button type="button" icon="pi pi-filter"
              label="Edit" class="p-button-outlined p-m-1" style="float: right" @click="openEditFilterModal"/>
      <Dialog header="Edit Filters" v-model:visible="displayEditFilterModal" :style="{width: '50vw'}" :modal="true">
        <p class="p-m-0">Edit Filters.</p>
        <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeEditFilterModal" class="p-button-text"/>
          <Button label="Yes" icon="pi pi-check" @click="closeEditFilterModal" autofocus/>
        </template>
      </Dialog>
    </template>
<!--    TODO: SHOW APPLIED FILTERS -->
    <template #right>
<!--      CLEAR FILTERS-->
      <Button type="button" icon="pi pi-filter-slash"
              label="Clear" class="p-button-outlined p-m-1"/>
<!--      RESET FILTERS-->
      <Button type="button" icon="pi pi-refresh"
              label="Reset" class="p-button-outlined p-m-1"/>
    </template>
  </Toolbar>
  <br>
<!--  ALERTS DATA TABLE-->
  <div class="card">
    <DataTable :value="alerts"
               responsiveLayout="scroll"
               :paginator="true"
               :rows="10"
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
               v-model:selection="selectedAlerts"
               dataKey="id"
               v-model:expandedRows="expandedRows"
               ref="dt"
               :resizableColumns="true"
               columnResizeMode="fit">

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
              <InputText v-model="narrowFilters['global'].value" placeholder="Search in table"/>
          </span>
<!--            CLEAR TABLE FILTERS -->
            <Button icon="pi pi-refresh" class="p-button-rounded p-m-1" @click="clearFilter1()"/>
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
  </div>
</template>

<script>

import {FilterMatchMode, FilterOperator} from 'primevue/api';

export default {
  data() {
    return {
      suggestedComments: ['this is an old comment', 'and another'],
      appliedDisposition: null,
      appliedComment: null,
      selectedRemediations: null,
      narrowFilters: null,
      calendarData: null,
      selectedUser: null,
      chosenEvent: null,
      newEventName: null,
      newEventComment: null,
      selectedOwners: null,
      newTags: [],
      filteredTags: null,
      users: ['Holly', 'Analyst', 'none'],
      selectedQueues: null,
      queues: ['external', 'internal', 'intel'],
      dispositions: ['FALSE_POSITIVE', 'WEAPONIZATION', 'COMMAND_AND_CONTROL'],
      elevated_dispositions: ['COMMAND_AND_CONTROL'],
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
          "id": "1234",
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
        {
          "id": "2345",
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
        {
          "id": "3456",
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
        {
          "id": "4567",
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
        {
          "id": "5678",
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
        {
          "id": "6789",
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
        {
          "id": "7890",
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
        {
          "id": "0978",
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
      remediation_targets: [
        {
          'type': 'zerofox',
          'target': 'bad_url',
          'status': 'remediation failed',
          'id': '123'
        },
        {
          'type': 'email',
          'target': 'msgID|email.com',
          'status': 'remediating',
          'id': '124'
        },
        {
          'type': 'email',
          'target': 'msgID|email2.com',
          'status': 'removed',
          'id': '125'
        },
        {
          'type': 'email',
          'target': 'msgID|email3.com',
          'status': 'restored',
          'id': '126'
        },
      ],
      selectedColumns: null,
      selectedAlerts: null,
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
  computed: {
    anyEventSelected: function () {
      return Boolean(this.chosenEvent);
    },
    newEventSelected: function () {
      console.log(this.chosenEvent);
      return this.chosenEvent === "New Event";
    },
    showAddToEventButton: function () {
      return this.elevated_dispositions.includes(this.appliedDisposition);
    },
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
      return unique_tags;
    }
  },
  methods: {
    clearFilter1() {
      this.initAlertNarrowFilters();
      this.selectedColumns = this.columns.slice(0, 5);
    },
    resetFilters() {
      this.initAlertNarrowFilters();
    },
    initAlertNarrowFilters() {
      this.narrowFilters = {
        'global': {value: null, matchMode: FilterMatchMode.CONTAINS}
      }
    },
    onToggle(value) {
      this.selectedColumns = this.columns.filter(col => value.includes(col));
    },
    addExistingTag(event) {
      this.newTags.push(event.value);
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
    autoSetEventName() {
      this.newEventName = "this is a placeholder";
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
a {
  color: #42b983;
}
</style>