<!-- AssignModal.vue -->
<!-- 'Assign' alert action modal -->

<template>
  <BaseModal :name="this.name" header="Assign Ownership">
    <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
      <div class="p-field p-col">
        <Dropdown
          v-model="selectedUser"
          :options="users"
          placeholder="Select a user"
        />
      </div>
    </div>
    <template #footer>
      <Button
        label="Nevermind"
        icon="pi pi-times"
        @click="close"
        class="p-button-text"
      />
      <Button label="Assign" icon="pi pi-check" @click="close" />
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal";

export default {
  name: "AssignModal",
  components: { BaseModal },

  computed: {
    name() {
      return this.$options.name;
    },
  },

  data() {
    return {
      selectedUser: null,
      users: ["Holly", "Analyst", "none"],
    };
  },

  methods: {
    close() {
      this.selectedUser = null;
      this.$store.dispatch("modals/close", this.name);
    },
  },
};
</script>
