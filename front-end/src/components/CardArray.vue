<template>
    <div class="overflow-x-scroll rounded-lg bg-white shadow-sm flex gap-1">
        <div v-for="(card, ix) in cards" :key="name(card)" class="px-4 py-5 sm:p-6 border border-slate-300 rounded-md">
            <span>{{ name(card) }}</span>
            <button @click="swapCard(ix, ix - 1)" :disabled="ix === 0" class="disabled:text-slate-400">
                <ChevronLeftIcon class="size-5" />
            </button>
            <button @click="swapCard(ix, ix + 1)" :disabled="ix === cards.length - 1" class="disabled:text-slate-400">
                <ChevronRightIcon class="size-5" />
            </button>
        </div>
    </div>
</template>

<script setup>

import { ref, watch } from 'vue';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/16/solid';

function name(card) {
    return card.alias ?? card.name;
}

const props = defineProps(['cards']);
const cards = ref([]);
watch(() => props.cards, function (value) {
    cards.value = value.slice();
    cards.value.sort((a, b) => a.outputSpecs.index - b.outputSpecs.index);
}, {
    immediate: true,
    deep: true,
});

function swapCard(ia, ib) {
    const a = cards.value[ia].outputSpecs;
    const b = cards.value[ib].outputSpecs;
    [a.index, b.index] = [b.index, a.index]
}
</script>