<template>
    <div class="overflow-x-scroll rounded-lg bg-white shadow-sm flex gap-1">
        <div v-for="(card, ix) in cards" :key="card.name" class="px-4 py-5 sm:p-6 border border-slate-300 rounded-md">
            <span>{{ card.name }}</span>
            <button @click="swapLeft(ix)" :disabled="ix === 0" class="disabled:text-slate-400"><ChevronLeftIcon class="size-5" /></button>
            <button @click="swapRight(ix)" :disabled="ix === cards.length - 1" class="disabled:text-slate-400"><ChevronRightIcon class="size-5" /></button>
        </div>
    </div>
</template>

<script setup>

import { ref, watch } from 'vue';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/16/solid';

const props = defineProps(['cards']);
const cards = ref([]);
watch(() => props.cards, function (value) {
    cards.value = value.slice();
    cards.value.sort((a, b) => a.index - b.index);
}, {
    immediate: true,
    deep: true,
});

function swapLeft(ix) {
    const temp = cards.value[ix - 1].index;
    cards.value[ix - 1].index = cards.value[ix].index;
    cards.value[ix].index = temp;
}

function swapRight(ix) {
    const temp = cards.value[ix + 1].index;
    cards.value[ix + 1].index = cards.value[ix].index;
    cards.value[ix].index = temp;
}
</script>