<template>
  <BaseModal :name="this.name" header="Delete" >
    <div class="confirmation-content">
      <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem"/>
      <span>Are you sure you want to delete this?</span>
    </div>
    <template #footer>
      <Button label="Actually, no" icon="pi pi-times" @click="close" class="p-button-text"/>
      <Button label="Do it!" icon="pi pi-check" @click="close" class="p-button-text" />
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal"

export default {
  name: "DeleteModal",
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