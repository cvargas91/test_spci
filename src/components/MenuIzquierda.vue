<template>
  <q-item clickable :to="link" exact active-class="fondoAmarillo">
    <q-item-section v-if="icon" avatar>
      <q-avatar class="bg-textoAzul" text-color="white" :icon="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label class="text-textoAzul"><b>{{ title }}</b></q-item-label>
      <q-item-label class="text-textoAzul" caption>
        {{ caption }}
      </q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "MenuIzquierda",
  props: {
    title: {
      type: String,
      required: true,
    },

    caption: {
      type: String,
      default: "",
    },

    link: {
      type: String,
      default: "#",
    },

    icon: {
      type: String,
      default: "",
    },
  },
});
</script>
