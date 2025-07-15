<script setup>
defineProps({
    id: String,
    title: String,
    disabled: Boolean,
});
const model = defineModel();
</script>

<template>
    <div>
        <label :for="id" class="block text-sm/6 font-medium text-gray-900">{{ title }}</label>
        <div class="mt-2">
            <input type="checkbox" v-model="model" :id :disabled />
        </div>
    </div>
</template>
