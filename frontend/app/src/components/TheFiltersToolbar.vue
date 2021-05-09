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
export default {
  name: "TheFiltersToolbar",

  props: {
    appliedFilters: {
      type: Array[Object],
      required: true
    },
  },

  data() {
    return {
      displayEditFilterModal: false,
      dispositions: ['FALSE_POSITIVE', 'WEAPONIZATION', 'COMMAND_AND_CONTROL'],
      endTimeFilterData: null,
      queues: ['external', 'internal', 'intel'],
      remediationStatuses: ['remediated', 'remediation_failed', 'remediating'],
      startTimeFilterData: null,
      tags: ['oh_no', 'bad', 'malware'],
      types: ['splunk_hunter'],
      users: ['Holly', 'Analyst', 'none'],
    }
  },
  methods: {
    openEditFilterModal() {
      this.displayEditFilterModal = true;
    },
    closeEditFilterModal() {
      this.displayEditFilterModal = false;
    },
  }
}
</script>

<style scoped>
</style>