<template>
  <q-page>
    <div class="q-pa-md">
      <ProtoAccionNueva
        :mostrar="mostrarPopupAniadir"
        @update:mostrar="mostrarPopupAniadir = $event"
      />
      <div v-if="poador.editaAccion">
        <ProtoAccionEditar :accion="poador.editaAccion" />
      </div>
      <div v-else-if="poador.misNuevasAcciones">
        <q-table
          flat
          grid
          hide-header
          title="Propuestas de Acción para el próximo Plan Operativo Anual (POA)"
          :filter="filtro"
          class="tablaAcciones"
          row-key="id"
          :rows="poador.misNuevasAcciones"
          :columns="columnas"
          no-data-label="Aún sin propuestas de acción"
          :pagination="paginacionInicial"
        >
          <template v-slot:top-right>
            <q-input
              borderless
              dense
              debounce="300"
              v-model="filtro"
              placeholder="Buscar"
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
          <template v-slot:item="props">
            <div class="q-pa-md col-xs-12 col-sm-6 col-md-4 col-lg-3">
              <q-card>
                <q-list dense>
                  <q-item
                    v-for="col in props.cols.filter(
                      (col) => col.name !== 'desc'
                    )"
                    :key="col.name"
                  >
                    <q-item-section>
                      <q-item-label>{{ col.label }}</q-item-label>
                    </q-item-section>
                    <q-item-section>
                      <q-item-label caption>
                        {{ col.value }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
                <q-card-section align="right">
                  <q-btn
                    class="q-mr-sm"
                    color="primary"
                    icon="edit"
                    label=""
                    @click="clickEditaAccion(props.key)"
                  />
                </q-card-section>
                <q-separator />
              </q-card>
            </div>
          </template>
        </q-table>
        <q-page-sticky position="bottom-right" :offset="posBoton">
          <q-btn
            round
            size="lg"
            color="primary"
            icon="add"
            @click="clickNuevaAccion"
            :disable="dragging"
            v-touch-pan.prevent.mouse="muevelo"
          />
        </q-page-sticky>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, computed, onMounted, onUnmounted, ref } from "vue";
import { useStore } from "vuex";
import ProtoAccionNueva from "src/components/ProtoAccionNueva.vue";
import ProtoAccionEditar from "src/components/ProtoAccionEditar.vue";

export default defineComponent({
  components: {
    ProtoAccionNueva,
    ProtoAccionEditar,
  },
  setup() {
    const limit = (string, length, end = "...") => {
      return string.length < length
        ? string
        : string.substring(0, length) + end;
    };
    const store = useStore();
    const usuario = computed(() => store.state.usuarix);
    const poador = computed(() => store.state.poador);
    const mostrarPopupAniadir = ref(false);
    const posBoton = ref([40, 70]);
    const dragging = ref(false);
    const columnas = [
      {
        name: "id_uaysen",
        label: "Identificador",
        field: "id_uaysen",
        sortable: true,
      },
      {
        name: "proyecto",
        label: "Proyecto",
        field: "proyecto",
        format: (val, row) => `${limit(val, 15)}`,
      },
      { name: "anio", label: "Año", field: "anio", sortable: true },
      {
        name: "titulo",
        label: "Título",
        field: "titulo",
        format: (val, row) => `${limit(val, 30)}`,
      },
      {
        name: "objetivo",
        label: "Objetivo",
        field: "objetivo",
        format: (val, row) => `${limit(val, 60)}`,
      },
      { name: "tipo", label: "Tipo", field: "tipo", sortable: true },
      {
        name: "num_estrategias",
        label: "Estrategias",
        field: "num_estrategias",
        sortable: true,
      },
      {
        name: "num_hitos",
        label: "Hitos",
        field: "num_hitos",
        sortable: true,
      },
      {
        name: "num_mdvs",
        label: "MDVs",
        field: "num_mdvs",
        sortable: true,
      },
      {
        name: "num_funciones",
        label: "Funciones",
        field: "num_funciones",
        sortable: true,
      },
      {
        name: "num_presupuestos",
        label: "Presupuestos",
        field: "num_presupuestos",
      },
      {
        name: "num_colaboradores",
        label: "Colaboradores",
        field: "num_colaboradores",
      },
      {
        name: "modificacion",
        label: "Última modificación",
        field: "modificacion",
        sortable: true,
      },
      {
        name: "creacion",
        label: "Creación",
        field: "creacion",
        sortable: true,
      },
    ];

    onMounted(() => {
      store.dispatch("poador/reqMisNuevasAcciones");
    });

    return {
      usuario,
      poador,
      mostrarPopupAniadir,
      clickNuevaAccion: () => {
        mostrarPopupAniadir.value = true;
      },
      clickEditaAccion: (id_accion) => {
        store.dispatch("poador/reqDetalleAccion", id_accion);
      },
      columnas,
      filtro: ref(""),
      paginacionInicial: { sortBy: "desc", descending: false, rowsPerPage: 8 },
      dragging,
      posBoton,
      muevelo(ev) {
        dragging.value = ev.isFirst !== true && ev.isFinal !== true;
        posBoton.value = [
          posBoton.value[0] - ev.delta.x,
          posBoton.value[1] - ev.delta.y,
        ];
      },
    };
  },
});
</script>
