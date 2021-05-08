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
             @row-select="$emit('alertSelect', $event.data)"
             @row-unselect="$emit('alertUnselect', $event.data)"
             @row-select-all="$emit('alertSelectAll', $event.data)"
             @row-unselect-all="$emit('alertUnselectAll', $event.data)">

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

export default {
  name: "TheAlertsTable",

  props: {
    alerts: {
      type: Array[Object],
      required: true
    },
  },

  emits: ['alertSelect',
          'alertUnselect',
          'alertSelectAll',
          'alertUnselectAll'],

  data() {
    return {
      alertTableFilters: null,
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
      selectedColumns: null,
      selectedOwners: null,
      selectedRows: null,
      selectedRemediations: null,
      startTimeFilterData: null,
      suggestedComments: ['this is an old comment', 'and another'],
      types: ['splunk_hunter'],
      users: ['Holly', 'Analyst', 'none'],
    }
  },
  async created() {
    this.resetAlertTableFilters();
  },
  computed: {
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
    },
    test(event) {
      console.log(event);
    }
  }
}
</script>

<style scoped>
</style>