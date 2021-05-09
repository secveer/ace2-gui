<template>
  <Toolbar>
    <template #left>
      <!--      DISPOSITION -->
      <Button class="p-m-1 p-button-normal p-button-success" icon="pi pi-thumbs-up" label="Disposition"
              @click="open('DispositionModal')"/>
      <DispositionModal></DispositionModal>
      <!--      COMMENT -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-comment" label="Comment" @click="open('CommentModal')"/>
      <CommentModal></CommentModal>
      <!--      TAKE OWNERSHIP -- NO MODAL -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-briefcase" label="Take Ownership"/>
      <!--      ASSIGN -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-user" label="Assign" @click="open('AssignModal')"/>
      <AssignModal></AssignModal>
      <!--      TAG MODAL -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-tags" label="Tag" @click="open('TagModal')"/>
      <TagModal></TagModal>
      <!--      REMEDIATE MODAL -->
      <Button class="p-m-1 p-button-sm" icon="pi pi-times-circle" label="Remediate" @click="open('RemediationModal')"/>
      <RemediationModal></RemediationModal>
      <!--      DELETE ALERT -->
      <Button class="p-m-1 p-button-sm p-button-danger" icon="pi pi-trash" label="Delete" @click="open('DeleteModal')"/>
      <DeleteModal></DeleteModal>

    </template>
    <template #right>
      <Button icon="pi pi-link" class="p-button-rounded"/>

    </template>
  </Toolbar>
</template>

<script>

import AssignModal from "@/components/AssignModal";
import CommentModal from "@/components/CommentModal";
import TagModal from "@/components/TagModal";
import RemediationModal from "@/components/RemediateModal";
import DeleteModal from "@/components/DeleteModal";
import DispositionModal from "@/components/DispositionModal";
export default {
  name: "TheAlertActionToolbar",
  components: {DispositionModal, DeleteModal, RemediationModal, TagModal, CommentModal, AssignModal},
  props: {
    selectedAlerts: {
      type: Array[Object],
      required: true
    },
  },
  methods: {
    open(name) {
      this.$store.dispatch("modals/open", name)
    }
  }
}
</script>

<style scoped>

</style>