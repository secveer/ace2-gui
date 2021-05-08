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
          <Button v-if="showAddToEventButton" label="Save to Event" class="p-button-raised" @click="closeDispositionModal();openSaveToEventModal();autoSetEventName();" />
        </template>
      </Dialog>
<!--      SAVE TO EVENT -->
      <Dialog header="Save to Event" v-model:visible="displaySaveToEventModal" :style="{width: '50vw'}" :modal="true" :closable="false">
        <TabView class="p-m-1">
          <TabPanel v-for="eventType of existingEvents" :key="eventType.title" :header="eventType.title">
            <div v-for="eventItem of eventType.events" :key="eventItem" class="p-field-radiobutton p-inputgroup">
              <RadioButton :id="eventItem" name="eventItem" :value="eventItem" v-model="chosenEvent"/>
              <label :for="eventItem">{{ eventItem }}</label>
            </div>
            <div class="p-field-radiobutton p-inputgroup">
              <RadioButton id="newEventItem" name="newEventItem" value="New Event" v-model="chosenEvent"/>
              <label for="newEventItem">New Event</label>
            </div>
            <div v-if="newEventSelected" class="p-m-1 p-grid p-fluid p-formgrid">
              <div class="p-field p-col p-m-1">
              <InputText name="newEventName" type="text" v-model="newEventName"/>
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
          <Button label="Save" icon="pi pi-check" @click="closeSaveToEventModal"  :disabled="!anyEventSelected"/>
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
          <Button label="Add" icon="pi pi-check" @click="closeCommentModal" />
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
          <Button label="Assign" icon="pi pi-check" @click="closeAssignModal" />
        </template>
      </Dialog>
<!--      TAG MODAL -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-tags" label="Tag" @click="openTagModal"/>
      <Dialog header="Add Tags" v-model:visible="displayTagModal" :style="{width: '50vw'}" :modal="true">
        <span class="p-fluid">
              <Chips v-model="newTags" />
              <Dropdown @change="addExistingTag" :options="tags" :filter="true" placeholder="Select from existing tags"
                        filterPlaceholder="Search tags" />
          </span>
        <template #footer>
          <Button label="Nevermind" icon="pi pi-times" @click="closeTagModal" class="p-button-text"/>
          <Button label="Add" icon="pi pi-check" @click="closeTagModal" />
        </template>
      </Dialog>
<!--      REMEDIATE MODAL -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-times-circle" label="Remediate" @click="openRemediateModal"/>
      <Dialog header="Remediate" v-model:visible="displayRemediateModal" :style="{width: '50vw'}" :modal="true">
        <DataTable :value="remediationTargets"
                   :rows="10"
                   :sortOrder="1"
                   columnResizeMode="fit"
                   dataKey="id"
                   removableSort
                   responsiveLayout="scroll"
                   sortField="type"
                   stripedRows
                   v-model:selection="selectedRemediations">
          <Column id="remediation-select" selectionMode="multiple" headerStyle="width: 3em"/>
          <Column field="type" header="Type" :sortable="true"></Column>
          <Column field="target" header="Target" :sortable="true"></Column>
          <Column field="status" header="Status" :sortable="true"></Column>
        </DataTable>
        <template #footer>
          <Button label="Stop" class="p-button-text"/>
          <Button label="Remove" icon="pi pi-times" />
          <Button label="Restore" icon="pi pi-check" />
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
          <Button label="Do it!" icon="pi pi-check" @click="closeConfirmation" class="p-button-text" />
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
<!--      DATE PICKER -->
      <i class="pi pi-calendar"></i>
      <Calendar class="p-m-1" id="startTimeFilter" v-model="startTimeFilterData" :manualInput="true" :showTime="true"
                selectionMode="single" style="width: 180px"/> to
      <Calendar class="p-m-1" id="endTimeFilter" v-model="endTimeFilterData" :manualInput="true" :showTime="true"
                selectionMode="single" style="width: 180px"/>
<!--      EDIT FILTERS -->
      <Button type="button" icon="pi pi-filter"
              label="Edit" class="p-button-outlined p-m-1" style="float: right" @click="openEditFilterModal"/>
      <Dialog header="Edit Filters" v-model:visible="displayEditFilterModal" :style="{width: '50vw'}" :modal="true">
        <p class="p-m-0">Edit Filters.</p>
        <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeEditFilterModal" class="p-button-text"/>
          <Button label="Yes" icon="pi pi-check" @click="closeEditFilterModal" />
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
               v-model:selection="selectedAlerts">

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
  </div>
</template>

<script>

import axios from 'axios';

import {FilterMatchMode, FilterOperator} from 'primevue/api';

export default {
  data() {
    return {
      alerts: [],
      alertTableFilters: null,
      appliedComment: null,
      appliedDisposition: null,
      chosenEvent: null,
      columns: [{field: 'alert_date', header: 'Alert Date'},
        {field: 'disposition', header: 'Disposition'},
        {field: 'disposition_by', header: 'Dispositioned By'},
        {field: 'event_date', header: 'Event Date'},
        {field: 'name', header: 'Name'},
        {field: 'owner', header: 'Owner'},
        {field: 'queue', header: 'Queue'},
        {field: 'remediated_by', header: 'Remediated By'},
        {field: 'remediated_date', header: 'Remediated Date'},
        {field: 'remediation_status', header: 'Remediation Status'},
        {field: 'type', header: 'Type'},
      ],
      displayAssignModal: false,
      displayCommentModal: false,
      displayConfirmation: false,
      displayDispositionModal: false,
      displayEditFilterModal: false,
      displayRemediateModal: false,
      displaySaveToEventModal: false,
      displayTagModal: false,
      dispositions: ['FALSE_POSITIVE', 'WEAPONIZATION', 'COMMAND_AND_CONTROL'],
      elevated_dispositions: ['COMMAND_AND_CONTROL'],
      endTimeFilterData: null,
      existingEvents: [{'title': 'Open', 'events': ['event1', 'event2']},
                        {'title': 'Closed', 'events': ['event3', 'event4']}],
      expandedRows: [],
      filteredTags: null,
      newEventComment: null,
      newEventName: null,
      newTags: [],
      queues: ['external', 'internal', 'intel'],
      remediationStatuses: ['remediated', 'remediation_failed', 'remediating'],
      remediationTargets: [
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
      selectedAlerts: null,
      selectedColumns: null,
      selectedOwners: null,
      selectedQueues: null,
      selectedRemediations: null,
      selectedUser: null,
      startTimeFilterData: null,
      suggestedComments: ['this is an old comment', 'and another'],
      types: ['splunk_hunter'],
      users: ['Holly', 'Analyst', 'none'],
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
  computed: {
    anyEventSelected: function () {
      return Boolean(this.chosenEvent);
    },
    newEventSelected: function () {
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
      // todo: modify tags in alert object to be objects rather than a string
      // this will allow for proper filtering
      return unique_tags;
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