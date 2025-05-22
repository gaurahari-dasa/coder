<script setup>
import HelloWorld from './components/HelloWorld.vue'
import FormInput from './components/FormInput.vue';
</script>

<template>
  <div class="container p-4">
    <h3 class="font-bold text-lg">Model Definition</h3>
    <div class="grid grid-cols-4 gap-4">
      <FormInput caption="Model Class" id="model" />
      <FormInput caption="Context Model Class" id="ctxt-model" />
    </div>
  </div>
</template>
