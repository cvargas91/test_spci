<template>
  <q-dialog v-model="mostrar">
    <q-card>
      <q-card-section class="row items-center">
        <q-avatar icon="warning" color="primary" text-color="white" />
        <span class="q-ml-sm"
          >¿Estas segur@ que deseas descartar (eliminar) la entrega?</span
        >
      </q-card-section>
      <q-card-section>
        Se eliminarán los siguientes adjuntos subidos a Google Drive:
        <ul>
          <li>archivos aca</li>
        </ul>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Cancelar" color="btnCancelar" v-close-popup />
        <q-btn
          flat
          label="Sí, descártala"
          color="primary"
          @click="clicDescartar"
          v-close-popup
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

export default {
  props: {
    mostrar: Boolean,
    entrega: Object,
    tipoEntrega: String,
  },
  setup(props, { emit }) {
    const store = useStore();
    const mostrar = computed({
      get: () => props.mostrar,
      set: (value) => emit("update:mostrar", value),
    });
    return {
      clicDescartar: () => {
        store.dispatch("entrega/workflowDescarta", {
          entrega_id: props.entrega.id,
          entrega_tipo: props.tipoEntrega,
        });
      },
      mostrar,
    };
  },
};
</script>
