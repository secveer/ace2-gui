<template>
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
</template>

<script>
import axios from 'axios';
import {FilterMatchMode} from 'primevue/api';

export default {
  name: "TheFiltersToolbar",

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
      selectedRemediations: null,
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

<style scoped>
</style>