<script setup>
defineProps({
    id: String,
    caption: String,
    inputType: {
        type: String,
        default: 'text'
    },
    min: Number,
});
const model = defineModel();
</script>

<template>
    <div>
        <label :for="id" class="block text-sm/6 font-medium text-gray-900">{{ caption }}</label>
        <div class="mt-2">
            <input
                class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                :type="inputType" :min="inputType == 'number' ? min : null" v-model="model" :id />
        </div>
    </div>
</template>
