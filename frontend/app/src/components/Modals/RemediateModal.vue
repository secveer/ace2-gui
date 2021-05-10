<!-- RemediateModal.vue -->
<!-- 'Remediation' alert action modal -->

<template>
  <BaseModal :name="this.name" header="Remediate" >
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
  </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal"

export default {
  name: "RemediationModal",
  components: { BaseModal },

  computed: {
    name() {
      return this.$options.name;
    },
  },

  data() {
    return {
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

      selectedRemediations: [],
    };
  },

  methods: {
    close() {
      this.selectedRemediations = [];
      this.$store.dispatch("modals/close", this.name);
    }
  }
}
</script>