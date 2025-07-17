<script setup>
defineProps({
    id: String,
    title: String,
    disabled: Boolean,
});
const model = defineModel();
defineEmits(['changed']);
</script>

<template>
    <div>
        <label :for="id" class="block text-sm/6 font-medium text-gray-900">{{ title }}</label>
        <div class="mt-1">
            <input type="checkbox" v-model="model" :id :disabled @change="$emit('changed', { checked: $event.target.checked })" />
        </div>
    </div>
</template>
