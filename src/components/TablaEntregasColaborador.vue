<template>
  <div v-if="entregas">
    <div class="text-h6 q-mb-md" v-if="mantencionPOA2023">
      En Mantención según POA 2023.
    </div>
    <q-table
      flat
      class="tablaAcciones"
      :rows="entregas"
      :columns="
        tipoEntrega == 'verificador' ? columnasVerificador : columnasProducto
      "
      row-key="id"
      selection="single"
      v-model:selected="entregaSeleccionada"
      no-data-label="No hay verificadores para el filtro aplicado"
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
            <q-tooltip class="text-body1">{{ props.value.titulo }}</q-tooltip>
          </div>
        </q-td>
      </template>
      <template v-slot:top="props">
        <div v-if="entregaSeleccionada.length">
          <div class="text-subtitle1">
            {{ entregaSeleccionada[0].descripcion }}
            <div v-if="adjuntos" class="text-h6 q-mb-md text-textoAzul">
              Acción <b> Sin archivos adjuntos</b>.
            </div>
          </div>
          <div
            v-if="entregaSeleccionada.length"
            class="row justify-end q-gutter-sm q-ma-md"
          >
            <q-btn
              color="btnCancelar"
              label="   Cancelar   "
              @click="entregaSeleccionada = []"
            />
            <BotonSecundarioEntregas
              :usuario="usuario"
              :entrega="entregaSeleccionada[0]"
              :tipoEntrega="tipoEntrega"
              @mantencion="manejoMantencion"
            />
            <BotonEdicionEntregas
              :usuario="usuario"
              :entrega="entregaSeleccionada[0]"
              :tipoEntrega="tipoEntrega"
              @mantencion="manejoMantencion"
            />
            <BotonPrincipalEntregas
              :usuario="usuario"
              :entrega="entregaSeleccionada[0]"
              :tipoEntrega="tipoEntrega"
              @ajuntosEntregas="getAdjuntos"
              @mantencion="manejoMantencion"
            />
          </div>
        </div>
      </template>
    </q-table>
  </div>
</template>
<script>
import { ref, toRef, defineComponent } from "vue";
import BotonPrincipalEntregas from "src/components/BotonPrincipalEntregas.vue";
import BotonSecundarioEntregas from "src/components/BotonSecundarioEntregas.vue";
import BotonEdicionEntregas from "src/components/BotonEdicionEntregas.vue";

export default defineComponent({
  components: {
    BotonPrincipalEntregas,
    BotonSecundarioEntregas,
    BotonEdicionEntregas,
  },
  props: {
    entregas: Array,
    usuario: Object,
    tipoEntrega: String,
  },
  methods: {
    manejoMantencion(mantencion){
      this.mantencionPOA2023 = mantencion
    },
  },
  setup(props) {
    const adjuntos = ref(false);
    const mantencionPOA2023 = ref(false);
    const getAdjuntos = (adjunto) => {
      adjuntos.value = adjunto;
    };
    return {
      mantencionPOA2023,
      getAdjuntos,
      adjuntos,
      entregas: toRef(props, "entregas"),
      tipoEntrega: toRef(props, "tipoEntrega"),
      entregaSeleccionada: ref([]),
      columnasProducto: [
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
      columnasVerificador: [
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
    };
  },
});
</script>
