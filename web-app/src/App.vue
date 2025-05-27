<script setup>
import { ref } from 'vue';

import HelloWorld from './components/HelloWorld.vue'
import FormInput from './components/FormInput.vue';
import FormButton from './components/FormButton.vue';

const model = ref({
  name: null,
  cntxtName: null
});
const routes = ref({
  entityUrl: null,
  entityRouteName: null,
  cntxtUrl: null,
  cntxtRouteName: null,
})
class Column {
  name = null;
  alias = null;
  inputSpec = {};
};
class Table {
  name = null;
  columns
};
const tables = [{
  name: null,
}];
function loadSpec() {
  fetch('http://localhost:5000/read-spec', {
    'method': 'POST'
  }).then(resp => resp.json()).then(t => {
    model.value.name = t.model.name;
    model.value.cntxtName = t.model.cntxtName;
    routes.value.entityUrl = t.routes.entityUrl;
    routes.value.entityRouteName = t.routes.entityRouteName;
    routes.value.cntxtUrl = t.routes.cntxtUrl;
    routes.value.cntxtRouteName = t.routes.cntxtRouteName;
  });
}
</script>

<template>
  <div class="container p-4">
    <h3 class="font-bold text-lg">Model</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput caption="Model Class" id="model" v-model="model.name" />
      <FormInput caption="Context Class" id="ctxt" v-model="model.cntxtName" />
    </div>
    <h3 class="mt-4 font-bold text-lg">Routes</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput caption="Entity Route URL" id="entity-route-url" v-model="routes.entityUrl" />
      <FormInput caption="Entity Route Name" id="entity-route-name" v-model="routes.entityRouteName" />
      <FormInput caption="Context Route URL" id="ctxt-route-url" v-model="routes.cntxtUrl" />
      <FormInput caption="Context Route Name" id="ctxt-route-name" v-model="routes.cntxtRouteName" />
    </div>
    <h3 class="mt-4 font-bold text-lg">Select Data</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput caption="Entity Table name" id="entity-table-name" />
      <FormInput caption="Entity Table primary_key" id="entity-table-pk" />
      <FormInput caption="Context Table name" id="ctxt-table-name" />
      <FormInput caption="Context Table primary_key" id="ctxt-table-pk" />
    </div>
    <FormButton caption="Add Table" @click="loadSpec()" />
  </div>
</template>
