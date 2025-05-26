<script setup>
defineProps(['caption']);
defineEmits(['click']);
</script>

<template>
    <button type="button"
        class="rounded-md bg-indigo-600 px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
        @click="$emit('click')">{{
        caption }}</button>
</template>
