<template>
  <q-form class="q-gutter-sm" style="min-width: 500px">
    <q-input
      filled
      v-model="mdv_nombre"
      label="Nombre del Medio De Verificación"
      hint=""
      lazy-rules
      :rules="[
        (val) => (val && val.length > 0) || 'Ingrese un nombre, por favor',
      ]"
    />
    <div class="q-gutter-xs">
      <q-btn
        label="En desarrollo"
        type="button"
        color="primary"
        class="q-mr-sm"
        @click="aniadirHito"
        disable
      />
      <q-btn color="btnCancelar" label="Cancelar" @click="clicCancelar" />
    </div>
  </q-form>
</template>

<script>
import { computed, ref, onMounted, onUnmounted } from "vue";
import { useStore } from "vuex";

export default {
  props: { mostrar: Boolean, id_accion: Number },
  setup(props, { emit }) {
    const mdv_nombre = ref("");
    const store = useStore();
    const mostrar = computed({
      get: () => props.mostrar,
      set: (value) => emit("update:mostrar", value),
    });
    onMounted(() => {});
    onUnmounted(() => {});
    return {
      mdv_nombre,
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
