<script setup>
defineProps(['id', 'caption'])
const model = defineModel();
</script>

<template>
    <div>
        <label :for="id" class="block text-sm/6 font-medium text-gray-900">{{ caption }}</label>
        <div class="mt-2">
            <input type="checkbox" v-model="model" :id />
        </div>
    </div>
</template>
