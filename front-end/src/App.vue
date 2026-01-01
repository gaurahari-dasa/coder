<script setup>
import { ref, watchEffect } from "vue";
import { TrashIcon, ArrowUturnLeftIcon } from "@heroicons/vue/16/solid";

import FormInput from "./components/FormInput.vue";
import FormButton from "./components/FormButton.vue";
import FormCheckbox from "./components/FormCheckbox.vue";
import FormTabs from "./components/FormTabs.vue";
import FormSelect from "./components/FormSelect.vue";
import FormRadio from "./components/FormRadio.vue";
import CardArray from "./components/CardArray.vue";

const baseUrl = "http://localhost:5000";

const model = ref({
  name: null,
  cntxtName: null,
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
  cntxtTablePrimaryKey: null,
  tables: [],
});

watchEffect(() => {
  const fieldNames = new Set();
  const tablesNotSkipped = selectData.value.tables.filter((x) => !x.skipThis);
  for (const table of tablesNotSkipped) {
    const fieldsNotSkipped = table.fields.filter((x) => !x.skipThis);
    for (const field of fieldsNotSkipped) {
      // const name = field.alias?.length > 0 ? field.alias : field.name;
      const name = field.alias ?? field.name;
      if (field.fillable || field.outputted) {
        field.error = fieldNames.has(name) ? "Duplicated!" : null;
        fieldNames.add(name);
      } else {
        field.error = null;
      }
    }
  }
});

const attribTabs = [
  { name: "Refers To", href: "#", current: false },
  { name: "Input", href: "#", current: true },
  { name: "Display", href: "#", current: false },
  { name: "Morph", href: "#", current: false },
];

class Field {
  constructor(key, name = null) {
    this.key = key;
    this.name = name;
  }
  name = null;
  alias = null;
  morphSpecs = null;
  foreign = null;
  fillable = null;
  inputSpecs = null;
  // searchable = null;
  // sortable = null;
  // sortOrdinal = null;
  outputted = null;
  outputSpecs = null;
  tabs = attribTabs;
  skipThis = false;
  selectTab(tabName) {
    for (const tab of this.tabs) {
      tab.current = tab.name === tabName;
    }
  }
}

class Table {
  constructor(key, name = null) {
    this.key = key;
    this.name = name;
  }
  name = null;
  fields = [];
  skipThis = false;
  selectTabs(tabName) {
    for (const field of this.fields) {
      field.selectTab(tabName);
    }
  }
}

function addTable() {
  tables.push(new Table(tables.length));
}

function makeInputtable(field, make) {
  if (make) {
    // field.inputSpecs = $event.checked ? {} : null; console.log('Haribol', field.inputSpecs)
    field.inputSpecs = {
      type: null,
      title: null,
      options: null,
      matchValue: null,
      focus: null,
      required: null,
    };
  }
}

function displayField(field, show) {
  if (show) {
    field.outputSpecs = {
      name: null,
      type: null,
      title: null,
      index: cards.value.length,
      searchable: null,
      sortable: null,
      sortOrdinal: null,
    };
    cards.value.push(field);
  } else {
    field.outputSpecs = null;
    let ix = cards.value.findIndex((v) => v.name == field.name);
    cards.value.splice(ix, 1);
    for (; ix < cards.value.length; ++ix) {
      --cards.value[ix].index;
    }
  }
}

let tables = selectData.value.tables; // an alias, Haribol
const cards = ref([]);

function loadSpec() {
  fetch(`${baseUrl}/read-spec`, {
    method: "GET",
  })
    .then((resp) => resp.json())
    .then((t) => {
      model.value = t.model;
      routes.value = t.routes;
      selectData.value = t.selectData;
      tables = selectData.value.tables; // reset the alias, Haribol
      tables.forEach((table) => {
        table.selectTabs = Table.prototype.selectTabs;
        table.skipThis = false;
        table.fields.forEach((field) => {
          if (field.outputted) {
            cards.value.push(field);
          }
          field.tabs = attribTabs;
          field.selectTab = Field.prototype.selectTab;
          field.skipThis = false;
        });
        // cards.value.length = 0; // clear column display card array, Haribol
      });
    });
}

async function reflectContextTable() {
  const cntxtModel = model.value.cntxtName?.trim();
  if (cntxtModel) {
    const params = new URLSearchParams();
    params.append("name", cntxtModel);
    try {
      const resp = await fetch(`${baseUrl}/reflect/table?${params}`);
      if (resp.ok) {
        const t = await resp.json();
        selectData.value.cntxtTableName = t.table;
        selectData.value.cntxtTablePrimaryKey = t.primaryKey;
      } else {
        resp.json().then((t) => alert(t.message));
      }
    } catch (e) {
      console.error(e);
    }
  }
}

function fillTables(fields) {
  tables.length = 0; // clear array, Haribol
  const tableMap = new Map();
  for (const field of fields) {
    const [tblname, fldname] = field.split(".");
    if (tblname == selectData.value.cntxtTableName) {
      continue; // skip context table fields, Haribol
    }
    let table = null;
    if (!tableMap.has(tblname)) {
      table = new Table(tables.length, tblname);
      tables.push(table);
      tableMap.set(tblname, table);
    } else {
      table = tableMap.get(tblname);
    }
    table.fields.push(new Field(table.fields.length, fldname));
  }
}

function reflectFields() {
  const params = new URLSearchParams();
  params.append("name", model.value.name);
  if (selectData.value.entityTableName) {
    params.append("table", selectData.value.entityTableName);
  }
  fetch(`${baseUrl}/reflect/fields?${params}`)
    .then((resp) => {
      if (resp.ok) {
        resp.json().then((t) => {
          selectData.value.entityTableName = t.table;
          selectData.value.entityTablePrimaryKey = t.primaryKey;
          fillTables(t.fields);
        });
      } else {
        resp.json().then((t) => alert(t.message));
      }
    })
    .catch((e) => console.error(e));
}

async function reflectTable() {
  await reflectContextTable();
  reflectFields();
}

function setError(error) {
  for (var table of tables) {
    if (table.name == error.table_name) {
      for (var field of table.fields) {
        field.error = field.name === error.back_name ? error.message : "";
      }
    }
  }
  console.error(error);
}

function generate() {
  fetch(`${baseUrl}/generate`, {
    method: "POST",
    body: JSON.stringify({
      model: model.value,
      routes: routes.value,
      selectData: selectData.value,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((resp) => {
      if (resp.ok) {
        alert("Generated");
      } else {
        if (resp.status == 422) {
          resp.json().then((j) => setError(j));
          alert("There were errors, Haribol!");
        }
      }
    })
    .catch((rea) => alert("Not generated: " + rea));
}

function isPrimaryTable(tblname) {
  return tblname == selectData.value.entityTableName;
}

function optionTitle(field) {
  switch (field.inputSpecs.type) {
    case "checkbox":
      return "Default Value";
    case "text":
      return "Max Length";
    case "select":
    case "auto":
      return "Options Prop";
    default:
      // field.inputSpecs.options = null;
      return undefined;
  }
}

function matchTitle(field) {
  switch (field.inputSpecs.type) {
    case "select":
    case "auto":
      return "Match Variable";
    default:
      // field.inputSpecs.options = null;
      return undefined;
  }
}

function toggleSkipField(fields, iy) {
  // fields.splice(iy, 1);
  fields[iy].skipThis = !fields[iy].skipThis;
}

function toggleSkipTable(table) {
  table.skipThis = !table.skipThis;
}
</script>

<template>
  <div class="container p-4">
    <h3 class="font-bold text-lg">Model</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput title="Model Class" id="model" v-model="model.name" />
      <div class="relative">
        <FormInput title="Context Class" id="ctxt" v-model="model.cntxtName" />
        <p class="text-[0.5rem] absolute top-1 right-0">
          (Leave blank if not applicable, Haribol!)
        </p>
      </div>
      <FormButton title="Fetch" @click="reflectTable" />
    </div>
    <h3 class="mt-4 font-bold text-lg">Routes</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput
        title="Entity Route URL"
        id="entity-route-url"
        v-model="routes.entityUrl"
      />
      <FormInput
        title="Entity Route Name"
        id="entity-route-name"
        v-model="routes.entityRouteName"
      />
      <FormInput
        title="Context Route URL"
        id="ctxt-route-url"
        v-model="routes.cntxtUrl"
      />
      <FormInput
        title="Context Route Name"
        id="ctxt-route-name"
        v-model="routes.cntxtRouteName"
      />
    </div>
    <h3 class="mt-4 font-bold text-lg">Select Data</h3>
    <div class="grid grid-cols-4 gap-4">
      <div>
        <FormInput
          title="Entity Table name"
          id="entity-table-name"
          v-model="selectData.entityTableName"
        />
        <FormButton title="Fetch" @click="reflectFields" />
      </div>
      <FormInput
        title="Entity Table primary_key"
        id="entity-table-pk"
        v-model="selectData.entityTablePrimaryKey"
      />
      <FormInput
        title="Context Table name"
        id="ctxt-table-name"
        v-model="selectData.cntxtTableName"
      />
      <FormInput
        title="Context Table primary_key"
        id="ctxt-table-pk"
        v-model="selectData.cntxtTablePrimaryKey"
      />
    </div>
    <h4 class="mt-4 font-semibold">Tables</h4>
    <div v-for="(table, ix) in tables">
      <h5 class="mt-8 font-semibold">
        Table {{ ix + 1
        }}<span class="italic ml-1" v-show="isPrimaryTable(table.name)"
          >(Primary)</span
        >
      </h5>
      <div class="relative flex gap-2">
        <button class="hover:cursor-pointer" @click="toggleSkipTable(table)">
          <TrashIcon v-show="!table.skipThis" class="size-4" />
          <ArrowUturnLeftIcon v-show="table.skipThis" class="size-4" />
        </button>
        <FormInput
          title="Table Name"
          :id="`table-name-${ix}`"
          v-model="table.name"
          :class="{ 'opacity-30': table.skipThis }"
        />
      </div>
      <div class="mt-8 space-y-8" :class="{ 'opacity-30': table.skipThis }">
        <div v-for="(field, iy) in table.fields" class="flex gap-2">
          <button
            class="hover:cursor-pointer"
            @click="toggleSkipField(table.fields, iy)"
          >
            <TrashIcon v-show="!field.skipThis" class="size-4" />
            <ArrowUturnLeftIcon v-show="field.skipThis" class="size-4" />
          </button>
          <div
            class="relative grid grid-cols-8 gap-x-4"
            :class="{ 'opacity-20': field.skipThis }"
          >
            <FormInput
              title="Field Name"
              :id="`field-name-${ix}-${iy}`"
              v-model="field.name"
            />
            <FormInput
              title="Field Alias"
              :id="`field-alias-${ix}-${iy}`"
              v-model="field.alias"
            />
            <div class="col-start-3 col-end-9">
              <FormTabs
                :tabs="field.tabs"
                @tabbed="table.selectTabs($event.tab.name)"
                class="mb-1"
              />
              <div
                v-show="field.tabs[0].current"
                class="grid grid-cols-6 gap-4"
              >
                <FormInput
                  title="Uniqe Key (or its alias)"
                  :id="`foreign-${ix}-${iy}`"
                  v-model="field.foreign"
                />
              </div>
              <div
                v-show="field.tabs[1].current"
                class="grid grid-cols-6 gap-4"
              >
                <div class="grid grid-cols-3">
                  <FormCheckbox
                    title="Fill"
                    :id="`fillable-${ix}-${iy}`"
                    :disabled="!isPrimaryTable(table.name)"
                    v-model="field.fillable"
                    @changed="makeInputtable(field, $event.checked)"
                  />
                  <template v-if="field.inputSpecs">
                    <FormCheckbox
                      title="Reqd"
                      :id="`inputspecs-required-${ix}-${iy}`"
                      v-model="field.inputSpecs.required"
                    />
                    <FormRadio
                      title="Focus"
                      :id="`inputspecs-focus-${ix}-${iy}`"
                      :name="`${table.name}-focus`"
                      :checked="field.inputSpecs.focus"
                    />
                  </template>
                </div>
                <template v-if="field.inputSpecs">
                  <FormSelect
                    title="Type"
                    :id="`inputspecs-type-${ix}-${iy}`"
                    v-model="field.inputSpecs.type"
                    :options="[
                      null,
                      'text',
                      'email',
                      'date',
                      'datetime-local',
                      'select',
                      'checkbox',
                      'file',
                      'auto',
                    ]"
                  />
                  <FormInput
                    title="Title"
                    :id="`inputspecs-title-${ix}-${iy}`"
                    v-model="field.inputSpecs.title"
                  />
                  <FormInput
                    :title="optionTitle(field)"
                    :id="`inputspecs-options-${ix}-${iy}`"
                    v-model="field.inputSpecs.options"
                  />
                  <FormInput
                    :title="matchTitle(field)"
                    :id="`inputspecs-match-value-${ix}-${iy}`"
                    v-model="field.inputSpecs.matchValue"
                  />
                </template>
              </div>
              <div
                v-show="field.tabs[2].current"
                class="grid grid-cols-5 gap-4"
              >
                <div class="grid grid-cols-3">
                  <FormCheckbox
                    title="Show"
                    :id="`outputted-${ix}-${iy}`"
                    v-model="field.outputted"
                    @changed="displayField(field, $event.checked)"
                  />
                  <div
                    class="grid grid-cols-2 col-span-2"
                    v-if="field.outputSpecs"
                  >
                    <FormCheckbox
                      title="Search"
                      :id="`outputSpecs-searchable-${ix}-${iy}`"
                      :disabled="
                        field.foreign?.length > 0 && isPrimaryTable(table.name)
                      "
                      v-model="field.outputSpecs.searchable"
                    />
                    <FormCheckbox
                      title="Sort"
                      :id="`outputSpecs-sortable-${ix}-${iy}`"
                      :disabled="
                        field.foreign?.length > 0 && isPrimaryTable(table.name)
                      "
                      v-model="field.outputSpecs.sortable"
                    />
                  </div>
                </div>
                <template v-if="field.outputSpecs">
                  <FormInput
                    inputType="number"
                    :min="0"
                    title="Sort Ordinal"
                    :id="`outputSpecs-sort-ordinal-${ix}-${iy}`"
                    :disabled="
                      field.foreign?.length > 0 && isPrimaryTable(table.name)
                    "
                    v-model="field.outputSpecs.sortOrdinal"
                  />
                  <FormSelect
                    title="Type"
                    :id="`outputSpecs-type-${ix}-${iy}`"
                    v-model="field.outputSpecs.type"
                    :options="[
                      null,
                      'ActiveColumn',
                      'CurrencyColumn',
                      'DataColumn',
                      'DateColumn',
                      'ImageColumn',
                    ]"
                  />
                  <FormInput
                    title="Title"
                    :id="`outputSpecs-title-${ix}-${iy}`"
                    v-model="field.outputSpecs.title"
                  />
                </template>
              </div>
              <div
                v-show="field.tabs[3].current"
                class="grid grid-cols-6 gap-4"
              >
                <FormSelect
                  title="Morph Specs"
                  :id="`morph-specs-${ix}-${iy}`"
                  v-model="field.morphSpecs"
                  :options="[null, 'file', 'date-only', 'date-time']"
                />
              </div>
            </div>
            <span
              v-show="field.error"
              class="col-span-2 bg-red-500 text-gray-100 p-0.5 text-xs absolute -bottom-1 left-0"
              :id="`error-field-name-${ix}-${iy}`"
            >
              {{ field.error }}
            </span>
          </div>
        </div>
      </div>
    </div>
    <h3 class="mt-8 font-bold text-lg">Display Column Ordering</h3>
    <CardArray class="mt-4" :cards />
    <div class="space-x-2">
      <FormButton title="Load Spec" @click="loadSpec()" />
      <FormButton title="Generate" @click="generate()" />
      <FormButton title="Add Table" @click="addTable()" />
    </div>
    <!-- <h3 v-if="duplicateField">Duplicate field: {{ duplicateField }}</h3> -->
  </div>
</template>
