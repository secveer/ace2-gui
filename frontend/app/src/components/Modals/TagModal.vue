<template>
  <BaseModal :name="this.name" header="Add Tags" >
        <span class="p-fluid">
              <Chips v-model="newTags" />
              <Dropdown @change="addExistingTag" :options="tags"  optionLabel="label"  :filter="true" placeholder="Select from existing tags"
                        filterPlaceholder="Search tags" />
          </span>
    <template #footer>
      <Button label="Nevermind" icon="pi pi-times" @click="close" class="p-button-text"/>
      <Button label="Add" icon="pi pi-check" @click="close" />
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal"

export default {
  name: "TagModal",
  components: { BaseModal },
  computed: {
    name() {
      return this.$options.name;
    },
  },
  data() {
    return {
      newTags: [],
      tags: [
        {label: 'oh_no', id: 1},
        {label: 'bad', id: 2},
        {label: 'malware', id: 3},
      ],
    }
  },
  methods: {
    addExistingTag(event) {
      this.newTags.push(event.value.label);
    },
    close() {
      this.newTags = [];
      this.$store.dispatch("modals/close", this.name);
    }
  }
}
</script>