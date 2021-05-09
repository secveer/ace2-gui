<template>
  <Menubar>
    <template #start>
      <router-link class="p-m-1" to="/manage_alerts"><img alt="ACE logo" src="../../assets/logo.jpg"></router-link>
      <router-link class="p-m-1" to="/"><Button label="New Analysis" class="p-button-raised"/></router-link>
      <router-link class="p-m-1" to="/"><Button label="Events" class="p-button-raised" /></router-link>
    </template>
    <template #end>
      <Button   icon="pi pi-bell" class="p-button-rounded p-m-1"  />
      <router-link to="/"><Button icon="pi pi-cog" class="p-button-rounded p-m-1" /></router-link>
      <Button icon="pi pi-user" class="p-button-rounded p-m-1" />
    </template>
  </Menubar>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "TheHeader",
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>