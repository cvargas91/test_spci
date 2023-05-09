<template>
  <q-page>
    <div v-if="entrega.estadoWorkflow" class="q-pa-md">
      <q-card class="my-card bg-teal-2">
        <q-card-section horizontal>
          <q-card-section>
            <q-avatar color="white" text-color="cyan-8" icon="done" />
          </q-card-section>
          <q-card-section class="text-textoAzul">
            <div class="text-h6"><b>Gracias por Colaborar</b></div>
            Estado de la entrega actualizado
          </q-card-section>
        </q-card-section>      
        <q-card-section class="q-pt-none">
          <q-btn color="light-blue-10"
            label="Volver a la bandeja de entregas"
            @click="limpiaBandeja"
          />          
        </q-card-section>
        <q-card-section>
          <q-separator class="bg-textoAzul" inset />
        </q-card-section>
      </q-card>
    </div>
    <div v-else>
      <div class="q-pa-md" v-if="usuario.perfil">
        <q-card>
          <q-tabs
            :model-value="tab"
            @update:model-value="cambiaTab"
            dense
            class="tablaAcciones"
            active-color="primary"
            indicator-color="primary"
            align="justify"
          >
            <q-tab name="verificadores" label="Verificadores" />
            <q-tab name="productos" label="Productos" />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="tab" animated>
            <q-tab-panel
              name="verificadores"
              class="tablaAcciones q-pa-none"
              v-if="verificador.verificadoresUPCI"
            >
              <q-table
                :rows="verificador.verificadoresUPCI"
                :columns="columnasVerificadores"
                row-key="id"
                selection="single"
                v-model:selected="verificadorSeleccionado"
                no-data-label="No hay verificadores aún"
                class="tablaAcciones"
              >
                <template v-slot:body-cell-adjuntos="props">
                  <q-td :props="props">
                    <div v-if="props.value">
                      <ul class="q-pa-sm">
                        <li
                          v-for="item in props.value.slice(0, 5)"
                          :key="item.id"
                        >
                          <a target="_blank" :href="item.url">{{
                            item.name
                          }}</a>
                        </li>
                        <div v-if="props.value.length > 5">...</div>
                      </ul>
                    </div>
                  </q-td>
                </template>
                <template v-slot:body-cell-accion="props">
                  <q-td :props="props">
                    <div v-if="props.value">
                      {{ props.value.id_uaysen }}
                      <q-tooltip class="text-body1">{{
                        props.value.titulo
                      }}</q-tooltip>
                    </div>
                  </q-td>
                </template>
                <template v-slot:top="props">
                  <div v-if="verificadorSeleccionado.length">
                    <div class="text-subtitle1">
                      {{ verificadorSeleccionado[0].descripcion }}
                    </div>
                  </div>
                </template>
              </q-table>
              <div v-if="verificadorSeleccionado.length" class="row justify-end q-gutter-sm q-ma-md">
                <q-btn
                  color="btnCancelar"
                  label="Cancelar"
                  @click="verificadorSeleccionado = []"
                />
                <BotonSecundarioEntregas
                  :usuario="usuario"
                  :entrega="verificadorSeleccionado[0]"
                  tipoEntrega="verificador"
                />
                <BotonPrincipalEntregas
                  :usuario="usuario"
                  :entrega="verificadorSeleccionado[0]"
                  tipoEntrega="verificador"
                />
              </div>
            </q-tab-panel>
            <q-tab-panel
              name="productos"
              class="tablaAcciones q-pa-none"
              v-if="producto.productosUPCI"
            >
              <q-table
                :rows="producto.productosUPCI"
                :columns="columnasProductos"
                row-key="id"
                selection="single"
                v-model:selected="productoSeleccionado"
                no-data-label="No hay productos aún"
                class="tablaAcciones"
              >
                <template v-slot:body-cell-adjuntos="props">
                  <q-td :props="props">
                    <div v-if="props.value">
                      <ul class="q-pa-sm">
                        <li
                          v-for="item in props.value.slice(0, 5)"
                          :key="item.id"
                        >
                          <a target="_blank" :href="item.url">{{
                            item.name
                          }}</a>
                        </li>
                        <div v-if="props.value.length > 5">...</div>
                      </ul>
                    </div>
                  </q-td>
                </template>
                <template v-slot:body-cell-accion="props">
                  <q-td :props="props">
                    <div v-if="props.value">
                      {{ props.value.id_uaysen }}
                      <q-tooltip class="text-body1">{{
                        props.value.titulo
                      }}</q-tooltip>
                    </div>
                  </q-td>
                </template>
                <template v-slot:top="props">
                  <div v-if="productoSeleccionado.length">
                    <div class="text-subtitle1">
                      {{ productoSeleccionado[0].descripcion }}
                    </div>
                    <div class="q-gutter-sm q-ma-md">                      
                    </div>
                  </div>
                </template>
              </q-table>
              <div v-if="productoSeleccionado.length" class="row justify-end q-gutter-sm q-ma-md">              
                <q-btn
                  color="btnCancelar"
                  label="Cancelar"
                  @click="productoSeleccionado = []"
                />
                <BotonSecundarioEntregas
                  :usuario="usuario"
                  :entrega="productoSeleccionado[0]"
                  tipoEntrega="producto"
                />
                <BotonPrincipalEntregas
                  :usuario="usuario"
                  :entrega="productoSeleccionado[0]"
                  tipoEntrega="producto"
                />
              </div>
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, defineComponent } from "vue";
import { useStore } from "vuex";
import BotonPrincipalEntregas from "src/components/BotonPrincipalEntregas.vue";
import BotonSecundarioEntregas from "src/components/BotonSecundarioEntregas.vue";

export default defineComponent({
  components: {
    BotonPrincipalEntregas,
    BotonSecundarioEntregas,
  },
  setup() {
    const store = useStore();
    const usuario = computed(() => store.state.usuarix.usuario);
    const producto = computed(() => store.state.producto);
    const verificador = computed(() => store.state.verificador);
    const entrega = computed(() => store.state.entrega);
    const productoSeleccionado = ref([]);
    const verificadorSeleccionado = ref([]);
    const tab = ref("verificadores");
    const cambiaTab = (value, event) => {
      store.dispatch("accion/limpiaAcciones");
      if (value == "productos")
        store.dispatch("producto/reqProductosEnviadosAUPCI");
      else if (value == "verificadores")
        store.dispatch("verificador/reqVerificadoresEnviadosAUPCI");
      tab.value = value;
    };
    onMounted(() => {
      store.dispatch("entrega/limpiaEntregas");
      store.dispatch("producto/reqProductosEnviadosAUPCI");
      store.dispatch("verificador/reqVerificadoresEnviadosAUPCI");
    });
    onUnmounted(() => {});
    return {
      usuario,
      entrega,
      productoSeleccionado,
      verificadorSeleccionado,
      columnasProductos: [
        {
          name: "descripcion",
          label: "Descripción",
          field: "descripcion",
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "colaborador",
          label: "Colaborador",
          field: (row) => row.usuario.first_name + " " + row.usuario.last_name,
          align: "left",
        },
        {
          name: "mdv",
          label: "Medio de Verificación",
          field: (row) => row.mdv ? row.mdv.nombre : row.hitos[0].nombre,
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "accion",
          label: "Acción",
          field: (row) => row.mdv ? row.mdv.accion : row.hitos[0].accion,
          align: "left",
        },
        {
          name: "accionTipo",
          label: "Tipo acción",
          field: (row) => row.mdv ? row.mdv.accion.tipo : row.hitos[0].accion.origen,
          align: "left",
          sortable: true,
        },
        {
          name: "adjuntos",
          label: "Adjuntos",
          field: "adjuntos",
          align: "left",
        },
        {
          name: "estado",
          label: "Estado",
          field: "estado",
          align: "left",
          sortable: true,
        },
        {
          name: "fecha",
          label: "Fecha",
          field: "fecha_creacion",
          align: "left",
          sortable: true,
        },
      ],
      columnasVerificadores: [
        {
          name: "descripcion",
          label: "Descripción",
          field: "descripcion",
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "colaborador",
          label: "Colaborador",
          field: (row) => row.usuario.first_name + " " + row.usuario.last_name,
          align: "left",
        },
        {
          name: "indicador",
          label: "Indicador",
          field: (row) => row.indicador.nombre,
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "funcion",
          label: "Función",
          field: (row) => row.indicador.funcion.nombre,
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "accion",
          label: "Acción",
          field: (row) => row.indicador.funcion.accion,
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "adjuntos",
          label: "Adjuntos",
          field: "adjuntos",
          align: "left",
        },
        {
          name: "estado",
          label: "Estado",
          field: "estado",
          align: "left",
          sortable: true,
        },
        {
          name: "fecha",
          label: "Fecha",
          field: "fecha_creacion",
          align: "left",
          sortable: true,
        },
      ],
      producto,
      verificador,
      tab,
      cambiaTab,
      limpiaBandeja: () => {
        productoSeleccionado.value = [];
        verificadorSeleccionado.value = [];
        store.dispatch("entrega/limpiaEntregas");
        store.dispatch("producto/reqProductosEnviadosAUPCI");
        store.dispatch("verificador/reqVerificadoresEnviadosAUPCI");
      },
    };
  },
});
</script>

