<template>
  <BaseModal :name="this.name" header="Edit Filters" >
    <p class="p-m-0">Edit Filters.</p>
    <template #footer>
      <Button label="No" icon="pi pi-times" @click="close" class="p-button-text"/>
      <Button label="Yes" icon="pi pi-check" @click="close" />
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal"

export default {
  name: "EditFilterModal",
  components: { BaseModal },
  computed: {
    name() {
      return this.$options.name;
    },
  },
  methods: {
    close() {
      this.$store.dispatch("modals/close", this.name);
    }
  }
}
</script>