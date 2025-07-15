<template>
    <div>
        <label :for="id" class="block text-sm/6 font-medium text-gray-900">{{ title }}</label>
        <div class="mt-2 grid grid-cols-1">
            <select :id name="location" v-model="opted" :disabled
                class="col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
                <option v-for="opt in options">{{ opt }}</option>
            </select>
            <ChevronDownIcon
                class="pointer-events-none col-start-1 row-start-1 mr-2 size-5 self-center justify-self-end text-gray-500 sm:size-4"
                aria-hidden="true" />
        </div>
    </div>
</template>

<script setup>
import { ChevronDownIcon } from '@heroicons/vue/16/solid'

const props = defineProps({
    id: String,
    title: String,
    options: Array,
    disabled: Boolean
});
const opted = defineModel();
</script>