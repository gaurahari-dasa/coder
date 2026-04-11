<template>
    <p class="mt-1 text-red-600 text-xs/5 italic" v-if="error">{{ error }}</p>
</template>

<script setup>
defineProps(["error"]);
</script>
