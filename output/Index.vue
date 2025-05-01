<template>
    <Layout :menus :auth>
        <div class="flex flex-col gap-2 sm:gap-6 lg:gap-8">
            <AvatarHeading class="-mt-4 sm:-mt-6 lg:-mt-8" :user="contact" backLabel="Back to what (parent) ???"
                backUrl=/contacts />
            <EntityCard class="px-4 sm:px-6 lg:px-8" :show="showAddForm">
                <h3 class="text-lg font-semibold text-slate-800">Add what (entity) ???</h3>
                <form class="relative" @submit.prevent="addEntity">
                    <FormGuard :allow="!formSaved">
                        <div class="grid grid-cols-4 gap-4">
                        <FormInput type="text" class="mt-4" id="name" title="Name" setFocus required
              v-model="addForm.name" :error="addForm.errors.name" />
<FormInput type="email" class="mt-4" id="email" title="Email"
              v-model="addForm.email" :error="addForm.errors.email" />
<FormInput type="text" class="mt-4" id="mobile" title="Mobile" required
              v-model="addForm.mobile" :error="addForm.errors.mobile" />
<FormFileUpload class="mt-4" id="photoPath" title="Photo"
              @pick="file => addForm.photoPath = file" :error="addForm.errors.photoPath" />
<FormInput type="date" class="mt-4" id="dob" title="DOB"
              v-model="addForm.dob" :error="addForm.errors.dob" />
<FormCheckBox class="mt-4" id="active" title="Active" v-model="addForm.active" />
<FormSelect class="mt-4" id="languageId" title="Language" :options="languages"
              v-model="addForm.languageId" :error="addForm.errors.languageId" />
                        </div>
                    </FormGuard>
                    <div class="relative lg:mt-8 lg:gap-x-8 sm:mt-6 sm:gap-x-6 mt-2 gap-x-2 flex justify-center">
                        <ToastMessage message="Saved Successfully, Haribol!" :show="addForm.recentlySuccessful" />
                        <FormCancelButton @click="closeAddForm">Cancel</FormCancelButton>
                        <FormSubmitButton :disabled="addForm.processing || formSaved">Save</FormSubmitButton>
                    </div>
                </form>
            </EntityCard>
            <EntityCard class="px-4 sm:px-6 lg:px-8" :show="showEditForm">
                <h3 class="text-lg font-semibold text-slate-800">Edit what (entity) ???</h3>
                <form class="relative" @submit.prevent="updateEntity">
                    <div class="grid grid-cols-4 gap-4">
                    <FormInput type="text" class="mt-4" id="name" title="Name" setFocus required
              v-model="editForm.name" :error="editForm.errors.name" />
<FormInput type="email" class="mt-4" id="email" title="Email"
              v-model="editForm.email" :error="editForm.errors.email" />
<FormInput type="text" class="mt-4" id="mobile" title="Mobile" required
              v-model="editForm.mobile" :error="editForm.errors.mobile" />
<FormFileUpload class="mt-4" id="photoPath" title="Photo"
              @pick="file => editForm.photoPath = file" :error="editForm.errors.photoPath" />
<FormInput type="date" class="mt-4" id="dob" title="DOB"
              v-model="editForm.dob" :error="editForm.errors.dob" />
<FormCheckBox class="mt-4" id="active" title="Active" v-model="editForm.active" />
<FormSelect class="mt-4" id="languageId" title="Language" :options="languages"
              v-model="editForm.languageId" :error="editForm.errors.languageId" />
                    </div>
                    <div class="relative lg:mt-8 lg:gap-x-8 sm:mt-6 sm:gap-x-6 mt-2 gap-x-2 flex justify-center">
                        <ToastMessage message="Saved Successfully, Haribol!" :show="editForm.recentlySuccessful" />
                        <FormCancelButton @click="closeEditForm">Cancel</FormCancelButton>
                        <FormSubmitButton :disabled="editForm.processing">Save</FormSubmitButton>
                    </div>
                </form>
            </EntityCard>

            <PaginatedDataTable class="px-4 sm:px-6 lg:px-8" title="what (entities) ???" :showAdd="addable"
                description="A list of all the what ???, Haribol"
                :headings="['Name', 'Email', 'Mobile', '', 'Active']" :pageData="guides"
                :columns="[DataColumn, DataColumn, DataColumn, ImageColumn, ActiveColumn]"
                :fields="['name', 'email', 'mobile', 'photoPath', 'active']" :searchKey
                :sortableFields="['name', 'email', 'mobile', 'photoPath']" :sortField :sortDir
                @table-add="showAddForm = true; showEditForm = false;" @row-act="editRow" focusSearch :actionIcons />
        </div>
    </Layout>
</template>

<script setup>
import Layout from '../../components/Layout.vue';
import PaginatedDataTable from '../../components/PaginatedDataTable.vue';
import AvatarHeading from '../../components/AvatarHeading.vue';
import FormInput from '../../components/FormInput.vue';
import FormFileUpload from '../../components/FormFileUpload.vue';
import FormCheckBox from '../../components/FormCheckBox.vue';
import FormSelect from '../../components/FormSelect.vue';
import DataColumn from '../../components/DataColumn.vue';
import ImageColumn from '../../components/ImageColumn.vue';
import ActiveColumn from '../../components/ActiveColumn.vue';
import EntityCard from '../../components/EntityCard.vue';
import FormCancelButton from '../../components/FormCancelButton.vue';
import FormSubmitButton from '../../components/FormSubmitButton.vue';
import ToastMessage from '../../components/ToastMessage.vue';
import FormGuard from '../../components/FormGuard.vue';
import { filterActions } from '../../utils';

import { computed, ref } from 'vue';
import { useForm } from '@inertiajs/vue3';
import { PencilSquareIcon } from '@heroicons/vue/24/outline';

const props = defineProps({
    menus: Array,
    auth: Object,
    privileges: Array,
    guides: Object,
contactId: Number,
    contact: Object,
languages: Array,
    searchKey: String,
    sortField: String,
    sortDir: String,
});

const actionIcons = computed(() => filterActions(props.privileges, {
    edit_guides: PencilSquareIcon,
}));

const addable = computed(() => {
    return props.privileges.indexOf('add_guides') !== -1;
});

const showAddForm = ref(false);
const showEditForm = ref(false);

const blanked = {
    name: null,
email: null,
mobile: null,
photoPath: null,
dob: null,
active: false,
languageId: null,
};
const addForm = useForm({
...blanked,
contactId: props.contactId,
});
const editForm = useForm(blanked);
const formSaved = ref(false);

function closeAddForm() {
    showAddForm.value = false;
    addForm.clearErrors();
    Object.assign(addForm, blanked);
    formSaved.value = false;
}

function closeEditForm() {
    showEditForm.value = false;
    editForm.clearErrors();
    editId = null;
}

function addEntity() {
    addForm.post('/guides', {
        onSuccess: () => {
            addForm.clearErrors();
            formSaved.value = true;
        },
        preserveScroll: true,
    });
}

var editId = null;

function editRow(id) {
    const datum = props.guides.data.find(v => v.id === id);
    editId = id;
editForm.name = datum.name;
editForm.email = datum.email;
editForm.mobile = datum.mobile;
editForm.dob = datum.dob;
editForm.active = datum.active;
editForm.languageId = datum.languageId;
    showEditForm.value = true;
    showAddForm.value = false;
}

function updateEntity() {
    editForm.patch(`/guides/${editId}`, {
        onSuccess: () => editForm.clearErrors(),
        preserveScroll: true,
    });
}
</script>