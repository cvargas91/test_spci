<template>
  <q-form class="q-gutter-sm" style="min-width: 500px">
    <q-input
      filled
      v-model="hito_nombre"
      label="Nombre del hito"
      hint="Ej: Aprobación de la conformación de..."
      lazy-rules
      :rules="[
        (val) => (val && val.length > 0) || 'Ingrese un nombre, por favor',
      ]"
    />
    <q-input
      filled
      v-model="hito_descripcion"
      label="Descripción del hito"
      hint="Ej: Planificación, implementación, seguimiento y evaluación de..."
      lazy-rules
      :rules="[
        (val) =>
          (val && val.length > 0) || 'Ingrese una descripción, por favor',
      ]"
      type="textarea"
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
    const hito_nombre = ref("");
    const hito_descripcion = ref("");
    const store = useStore();
    const mostrar = computed({
      get: () => props.mostrar,
      set: (value) => emit("update:mostrar", value),
    });
    onMounted(() => {});
    onUnmounted(() => {});
    return {
      hito_nombre,
      hito_descripcion,
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
