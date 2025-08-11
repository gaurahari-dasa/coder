<script setup>
defineProps({
    id: String,
    title: String,
    inputType: {
        type: String,
        default: 'text'
    },
    min: Number,
    disabled: Boolean,
    duped: Boolean
});
const model = defineModel();
defineEmits(['input']);
</script>

<template>
    <div v-show="title">
        <label :for="id" class="block text-sm/6 font-medium text-gray-900">{{ title }}</label>
        <div class="mt-1">
            <input
                class="block w-full rounded-md bg-white px-3 py-1.5 text-base outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"  :class="duped ? 'text-red-500' : 'text-gray-900'"
                :type="inputType" :min="inputType == 'number' ? min : null" v-model="model" :id :disabled @input="$emit('input', { value: $event.target.value })" />
        </div>
    </div>
</template>
