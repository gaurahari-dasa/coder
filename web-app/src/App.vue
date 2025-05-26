<script setup>
import HelloWorld from './components/HelloWorld.vue'
import FormInput from './components/FormInput.vue';
import FormButton from './components/FormButton.vue';
class Column
{
  name = null;
  alias = null;
  inputSpec = {};
};
class Table
{
  name = null;
  columns
};
const tables = [{
  name: null,
}];
function doaction() {
  fetch('http://localhost:5000/read-spec', {
      'method': 'POST'
    }).then(resp => resp.text()).then(t => console.log(t));
}
</script>

<template>
  <div class="container p-4">
    <h3 class="font-bold text-lg">Model</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput caption="Model Class" id="model" />
      <FormInput caption="Context Class" id="ctxt" />
    </div>
    <h3 class="mt-4 font-bold text-lg">Routes</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput caption="Entity Route URL" id="entity-route-url" />
      <FormInput caption="Entity Route Name" id="entity-route-name" />
      <FormInput caption="Context Route URL" id="ctxt-route-url" />
      <FormInput caption="Context Route Name" id="ctxt-route-name" />
    </div>
    <h3 class="mt-4 font-bold text-lg">Select Data</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput caption="Entity Table name" id="entity-table-name" />
      <FormInput caption="Entity Table primary_key" id="entity-table-pk" />
      <FormInput caption="Context Table name" id="ctxt-table-name" />
      <FormInput caption="Context Table primary_key" id="ctxt-table-pk" />
    </div>
    <FormButton caption="Add Table" @click="doaction()" />
  </div>
</template>
