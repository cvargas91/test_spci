<template>
  <q-form class="q-gutter-sm" style="min-width: 500px">
    <div>en desarrollo</div>
    <q-btn color="btnCancelar" label="Cancelar" @click="clicCancelar" />
  </q-form>
</template>

<script>
import { computed, ref, onMounted, onUnmounted } from "vue";
import { useStore } from "vuex";

export default {
  props: { mostrar: Boolean, id_accion: Number },
  setup(props, { emit }) {
    const store = useStore();
    const mostrar = computed({
      get: () => props.mostrar,
      set: (value) => emit("update:mostrar", value),
    });
    onMounted(() => {});
    onUnmounted(() => {});
    return {
      aniadirHito: () => {
        mostrar.value = false;
      },
      clicCancelar: () => {
        mostrar.value = false;
      },
    };
  },
};
</script>
