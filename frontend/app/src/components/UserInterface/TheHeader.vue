<!-- TheHeader.vue -->
<!-- Header / Navigation bar -->

<template>
  <Menubar>
    <template #start>
      <router-link class="p-m-1" to="/manage_alerts"
        ><img alt="ACE logo" src="../../assets/logo.jpg"
      /></router-link>
      <router-link class="p-m-1" to="/"
        ><Button label="New Analysis" class="p-button-raised"
      /></router-link>
      <router-link class="p-m-1" to="/"
        ><Button label="Events" class="p-button-raised"
      /></router-link>
    </template>
    <template #end>
      <Button icon="pi pi-bell" class="p-button-rounded p-m-1" />
      <router-link to="/"
        ><Button icon="pi pi-cog" class="p-button-rounded p-m-1"
      /></router-link>
      <Button icon="pi pi-user" class="p-button-rounded p-m-1" />
    </template>
  </Menubar>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Menubar from "primevue/menubar";
import Button from "primevue/button";

export default defineComponent({
  name: "TheHeader",
  components: { Menubar, Button },
});
</script>
