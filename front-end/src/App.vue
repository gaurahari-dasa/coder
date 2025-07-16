<script setup>
import { computed, ref, watchEffect } from 'vue';

import FormInput from './components/FormInput.vue';
import FormButton from './components/FormButton.vue';
import FormCheckbox from './components/FormCheckbox.vue';
import FormTabs from './components/FormTabs.vue';
import FormSelect from './components/FormSelect.vue';
import FormRadio from './components/FormRadio.vue';

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
  duped = null;
  morphSpecs = null;
  foreign = null;
  fillable = null;
  searchable = null;
  sortable = null;
  sortOrdinal = null;
  tabs = [
    { name: 'Morph', href: '#', current: true },
    { name: 'Refer', href: '#', current: false },
    { name: 'Input', href: '#', current: false },
    { name: 'Display', href: '#', current: false },
  ];
  selectTab(tabName) {
    for (const tab of this.tabs) {
      tab.current = tab.name === tabName;
    }
  }
};
class Table {
  name = null;
  fields = [];
  selectTabs(tabName) {
    for (const field of this.fields) {
      field.selectTab(tabName);
    }
  }
};
const tables = ref([]);
watchEffect(() => {
  for (const table of tables.value) {
    const fieldNames = new Set();
    for (const field of table.fields) {
      const name = field.alias?.length > 0 ? field.alias : field.name;
      field.duped = fieldNames.has(name);
      fieldNames.add(name);
    }
  }
});

function loadSpec() {
  fetch('http://localhost:5000/read-spec', {
    'method': 'GET'
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
    tables.value.length = 0; // Clear existing tables, Haribol
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
        newField.inputSpecs = field.inputSpecs;
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

function isPrimaryTable(tblname) {
  return tblname == selectData.value.entityTableName;
}

function makeFillable(field, checked) {
  field.inputSpecs = checked ? {} : null;
}

function optionTitle(field) {
  switch (field.inputSpecs.type) {
    case 'checkbox': return 'Default Value';
    case 'text': return 'Max Length';
    case 'select': case 'auto': return 'Options Prop';
    default:
      // field.inputSpecs.options = null;
      return undefined;
  }
}

function matchTitle(field) {
  switch (field.inputSpecs.type) {
    case 'select': case 'auto': return 'Match Variable';
    default:
      // field.inputSpecs.options = null;
      return undefined;
  }
}
</script>

<template>
  <div class="container p-4">
    <h3 class="font-bold text-lg">Model</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput title="Model Class" id="model" v-model="model.name" />
      <div class="relative">
        <FormInput title="Context Class" id="ctxt" v-model="model.cntxtName" />
        <p class="text-xs absolute top-1 right-0">(Leave blank if not applicable, Haribol!)</p>
      </div>
    </div>
    <h3 class="mt-4 font-bold text-lg">Routes</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput title="Entity Route URL" id="entity-route-url" v-model="routes.entityUrl" />
      <FormInput title="Entity Route Name" id="entity-route-name" v-model="routes.entityRouteName" />
      <FormInput title="Context Route URL" id="ctxt-route-url" v-model="routes.cntxtUrl" />
      <FormInput title="Context Route Name" id="ctxt-route-name" v-model="routes.cntxtRouteName" />
    </div>
    <h3 class="mt-4 font-bold text-lg">Select Data</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput title="Entity Table name" id="entity-table-name" v-model="selectData.entityTableName" />
      <FormInput title="Entity Table primary_key" id="entity-table-pk" v-model="selectData.entityTablePrimaryKey" />
      <FormInput title="Context Table name" id="ctxt-table-name" v-model="selectData.cntxtTableName" />
      <FormInput title="Context Table primary_key" id="ctxt-table-pk" v-model="selectData.cntxtTablePrimaryKey" />
    </div>
    <h4 class="mt-4 font-semibold">Tables</h4>
    <div v-for="(table, ix) in tables">
      <h5 class="mt-8 font-semibold">Table {{ ix + 1 }}<span class="italic ml-1"
          v-show="isPrimaryTable(table.name)">(Primary)</span></h5>
      <FormInput title="Table Name" :id="`${table.name}-${ix}`" v-model="table.name" />
      <div class="mt-8 space-y-8">
        <div v-for="field in table.fields" class="grid grid-cols-8 gap-4">
          <div class="relative">
            <FormInput title="Field Name" :id="`field-name-${ix}-${field.name}`" v-model="field.name" />
            <span v-if="field.duped" class="bg-red-500 absolute top-1 right-1 text-xs text-gray-100 p-0.5">duped</span>
          </div>
          <FormInput title="Field Alias" :id="`field-alias-${ix}-${field.name}`" v-model="field.alias" />
          <div class="col-start-3 col-end-9">
            <FormTabs :tabs="field.tabs" @tabbed="table.selectTabs($event.tab.name)" class="mb-1" />
            <div v-show="field.tabs[0].current" class="grid grid-cols-6 gap-4">
              <FormInput title="Morph Specs" :id="`morph-specs-${ix}-${field.name}`" v-model="field.morphSpecs" />
            </div>
            <div v-show="field.tabs[1].current" class="grid grid-cols-6 gap-4">
              <FormInput title="Foreign Key" :id="`foreign-${ix}-${field.name}`" v-model="field.foreign" />
            </div>
            <div v-show="field.tabs[2].current" class="grid grid-cols-6 gap-4">
              <div class="grid grid-cols-3">
                <FormCheckbox title="Fill" :id="`fillable-${ix}-${field.name}`" :disabled="!isPrimaryTable(table.name)"
                  v-model="field.fillable" @changed="makeFillable(field, $event.checked)" />
                <template v-if="field.inputSpecs">
                  <FormCheckbox title="Reqd" :id="`inputspecs-required-${ix}-${field.name}`"
                    v-model="field.inputSpecs.required" />
                  <FormRadio title="Focus" :id="`inputspecs-focus-${ix}-${field.name}`" :name="`${table.name}-focus`"
                    :checked="field.inputSpecs.focus" />
                </template>
              </div>
              <template v-if="field.inputSpecs">
                <FormSelect title="Type" :id="`inputspecs-type-${ix}-${field.name}`" v-model="field.inputSpecs.type"
                  :options="[null, 'text', 'email', 'date', 'select', 'checkbox', 'file', 'auto']" />
                <FormInput title="Title" :id="`inputspecs-title-${ix}-${field.name}`"
                  v-model="field.inputSpecs.title" />
                <FormInput :title="optionTitle(field)" :id="`inputspecs-options-${ix}-${field.name}`"
                  v-model="field.inputSpecs.options" />
                <FormInput :title="matchTitle(field)" :id="`inputspecs-match-value-${ix}-${field.name}`"
                  v-model="field.inputSpecs.matchValue" />
              </template>
            </div>
            <div v-show="field.tabs[3].current" class="grid grid-cols-6 gap-4">
              <FormCheckbox title="Searchable" :id="`searchable-${ix}-${field.name}`"
                :disabled="field.foreign?.length > 0 && isPrimaryTable(table.name)" v-model="field.searchable" />
              <FormCheckbox title="Sortable" :id="`sortable-${ix}-${field.name}`"
                :disabled="field.foreign?.length > 0 && isPrimaryTable(table.name)" v-model="field.sortable" />
              <FormInput inputType="number" :min="0" title="Sort Ordinal" :id="`sort-ordinal-${ix}-${field.name}`"
                :disabled="field.foreign?.length > 0 && isPrimaryTable(table.name)" v-model="field.sortOrdinal" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <FormButton title="Load Spec" @click="loadSpec()" />
    <FormButton title="Generate" @click="generate()" />
    <!-- <h3 v-if="duplicateField">Duplicate field: {{ duplicateField }}</h3> -->
  </div>
</template>
