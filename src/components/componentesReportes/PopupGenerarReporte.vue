<template>
  <q-dialog v-model="mostrar">
    mostrar
      <q-card>
        <q-card-section style="we">
          <div class="text-h6 text-textoAzul">  Espere....  </div>  
        </q-card-section>
      </q-card>
  </q-dialog>
</template>

<script>
import { computed } from "vue";

export default {
  props: {
    mostrar: Boolean,
  },
  setup(props, { emit }) {
    const mostrar = computed({
      get: () => props.mostrar,
      set: (value) => emit("update:mostrar", value),
    });
    return {
      mostrar,
    };
  },
};
</script>
