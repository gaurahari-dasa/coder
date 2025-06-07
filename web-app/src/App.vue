<script setup>
import { ref } from 'vue';

import HelloWorld from './components/HelloWorld.vue'
import FormInput from './components/FormInput.vue';
import FormButton from './components/FormButton.vue';
import FormCheckbox from './components/FormCheckbox.vue';

const model = ref({
  name: null,
  cntxtName: null
});
const routes = ref({
  entityUrl: null,
  entityRouteName: null,
  cntxtUrl: null,
  cntxtRouteName: null,
});
const selectData = ref({
  entityTableName: null,
  entityTablePrimaryKey: null,
  cntxtTableName: null,
  cntxtTablePrimaryKey: null
});
class Field {
  name = null;
  alias = null;
  morphSpecs = null;
  foreign = null;
  fillable = null;
  searchable = null;
  sortable = null;
  sortOrdinal = null;
};
class Table {
  name = null;
  fields = [];
};
const tables = ref([]);

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
    selectData.value.entityTableName = t.selectData.entityTableName;
    selectData.value.entityTablePrimaryKey = t.selectData.entityTablePrimaryKey;
    selectData.value.cntxtTableName = t.selectData.cntxtTableName;
    selectData.value.cntxtTablePrimaryKey = t.selectData.cntxtTablePrimaryKey;
    tables.length = 0; // Clear existing tables, Haribol
    t.selectData.tables.forEach(table => {
      const newTable = new Table();
      newTable.name = table.name;
      table.fields.forEach(field => {
        const newField = new Field();
        newField.name = field.name;
        newField.alias = field.alias;
        newField.morphSpecs = field.morphSpecs;
        newField.foreign = field.foreign;
        newField.fillable = field.fillable;
        newField.searchable = field.searchable;
        newField.sortable = field.sortable;
        newField.sortOrdinal = field.sortOrdinal;
        newTable.fields.push(newField);
      })
      tables.value.push(newTable);
    });
  });
}

function generate() {
  fetch('http://localhost:5000/generate', {
    'method': 'POST'
  }).then(resp => alert('Generated'))
    .catch(rea => alert('Not generated: ' + rea));
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
      <FormInput caption="Entity Table name" id="entity-table-name" v-model="selectData.entityTableName" />
      <FormInput caption="Entity Table primary_key" id="entity-table-pk" v-model="selectData.entityTablePrimaryKey" />
      <FormInput caption="Context Table name" id="ctxt-table-name" v-model="selectData.cntxtTableName" />
      <FormInput caption="Context Table primary_key" id="ctxt-table-pk" v-model="selectData.cntxtTablePrimaryKey" />
    </div>
    <h4 class="mt-4 font-semibold">Tables</h4>
    <div v-for="(table, ix) in tables">
      <h5 class="mt-8 font-semibold">Table {{ ix + 1 }}</h5>
      <FormInput caption="Table Name" :id="`table-name-${ix}`" v-model="table.name" />
      <div v-for="field in table.fields" class="mt-4 grid grid-cols-8 gap-4">
        <FormInput caption="Field Name" :id="`field-name-${ix}-${field.name}`" v-model="field.name" />
        <FormInput caption="Field Alias" :id="`field-alias-${ix}-${field.name}`" v-model="field.alias" />
        <FormInput caption="Morph Specs" :id="`morph-specs-${ix}-${field.name}`" v-model="field.morphSpecs" />
        <FormInput caption="Foreign Key" :id="`foreign-key-${ix}-${field.name}`" v-model="field.foreign" />
        <FormCheckbox caption="Fillable" :id="`fillable-${ix}-${field.name}`" v-model="field.fillable" />
        <FormCheckbox caption="Searchable" :id="`searchable-${ix}-${field.name}`" v-model="field.searchable" />
        <FormCheckbox caption="Sortable" :id="`sortable-${ix}-${field.name}`" v-model="field.sortable" />
        <FormInput inputType="number" :min="0" caption="Sort Ordinal" :id="`sort-ordinal-${ix}-${field.name}`" v-model="field.sortOrdinal" />
      </div>
    </div>
    <FormButton caption="Load Spec" @click="loadSpec()" />
    <FormButton caption="Generate" @click="generate()" />
  </div>
</template>
