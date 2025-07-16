<script setup>
defineProps({
    id: String,
    name: String,
    title: String,
    checked: Boolean,
    disabled: Boolean,
});
defineEmits(['changed']);
</script>

<template>
    <div>
        <label :for="id" class="block text-sm/6 font-medium text-gray-900">{{ title }}</label>
        <div class="mt-2">
            <input type="radio" :id :name :checked :disabled @change="$emit('changed', { checked: $event.target.checked })" />
        </div>
    </div>
</template>
