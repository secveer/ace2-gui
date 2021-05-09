<template>
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
      <Button class="p-m-1 p-button-sm" icon="pi pi-user" label="Assign" @click="open('AssignModal')"/>
      <AssignModal></AssignModal>
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
</template>

<script>

import AssignModal from "@/components/AssignModal";
export default {
  name: "TheAlertActionToolbar",
  components: {AssignModal},
  props: {
    selectedAlerts: {
      type: Array[Object],
      required: true
    },
  },

  data() {
    return {
      appliedComment: null,
      appliedDisposition: null,
      chosenEvent: null,
      displayAssignModal: false,
      displayCommentModal: false,
      displayConfirmation: false,
      displayDispositionModal: false,
      displayRemediateModal: false,
      displaySaveToEventModal: false,
      displayTagModal: false,
      dispositions: ['FALSE_POSITIVE', 'WEAPONIZATION', 'COMMAND_AND_CONTROL'],
      elevated_dispositions: ['COMMAND_AND_CONTROL'],
      existingEvents: [{'title': 'Open', 'events': ['event1', 'event2']},
        {'title': 'Closed', 'events': ['event3', 'event4']}],
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
      selectedUser: null,
      selectedOwners: null,
      selectedRemediations: null,
      suggestedComments: ['this is an old comment', 'and another'],
      tags: ['oh_no', 'bad', 'malware'],
      types: ['splunk_hunter'],
    }
  },
  computed: {
    showAddToEventButton: function () {
      return this.elevated_dispositions.includes(this.appliedDisposition);
    },
  },
  methods: {
    addExistingTag(event) {
      this.newTags.push(event.value);
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
    open(name) {
      this.$store.dispatch("modals/open", name)
    }
  }
}
</script>

<style scoped>

</style>