<template>
  <q-page>
    <div class="q-pa-md">
      <div class="text-h6 text-textoAzul"><b>Retroalimentación de productos y verificadores</b></div>
    </div>
    <div class="q-pa-md" v-if="retroalimentacion_productos">
      <q-table
        title="Productos"
        :rows="retroalimentacion_productos"
        :columns="columnasTablas"
        row-key="name"
      />
    </div>
    <div class="q-pa-md" v-if="retroalimentacion_verificadores">
      <q-table
        title="Verificadores"
        :rows="retroalimentacion_verificadores"
        :columns="columnasTablas"
        row-key="name"
      />
    </div>
  </q-page>
</template>

<script>
import { ref, computed, onMounted, defineComponent } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  setup() {
    const store = useStore();
    const columnasTablas = [
      {
        name: "retroalimentacion",
        label: "Detalle de la retroalimentación",
        align: "left",
        style: "white-space: normal",
        field: (row) => row.retroalimentacion,
      },
      {
        name: "accion",
        label: "Acción asociada",
        align: "left",
        field: (row) => row.accion,
      },
      {
        name: "modificado",
        label: "Fecha última modificación",
        align: "left",
        field: (row) => row.modificado,
      },
      {
        name: "creado",
        label: "Fecha creación",
        align: "left",
        field: (row) => row.creado,
      },
    ];
    onMounted(() => {
      store.dispatch("entrega/setRetroalimentaciones");
    });
    return {
      columnasTablas,
      retroalimentacion_productos: computed(
        () => store.state.entrega.retroalimentacion_productos
      ),
      retroalimentacion_verificadores: computed(
        () => store.state.entrega.retroalimentacion_verificadores
      ),
    };
  },
});
</script>
