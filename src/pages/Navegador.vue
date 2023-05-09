<template>
  <div class="q-pa-md text-textoAzul">
    <div class="text-h6"><b>Navegador POA</b></div>
    <div class="q-pa-md tablaAcciones">
        <div class="q-gutter-md row">
          <q-select
            v-model="modelDireccion"
            :options="actor.direccion"
            label="Dirección"
            style="width: 20em"
            option-label="nombre"
            @update:model-value="cambioDireccion"
          />  
          <br/>
          <q-select
            v-model="modelUnidad"
            :options="actor.unidad"
            label="Unidad"
            style="width: 20em"
            option-label="nombre"
            @update:model-value="cambioUnidad"
          />
          
          <q-select
            v-model="modelRol"
            :options="usuario.opciones.roles"
            label="Rol"
            style="width: 10em"
          />
          <q-select
            v-model="modelTipo"
            :options="usuario.opciones.tipos"
            label="Tipo"
            style="width: 10em"
          /> 
          
          <q-select
            v-model="modelPeriodo"
            :options="accion.anios.periodo"
            label="Año"
            style="width: 10em"
          /> 
          
          <q-select
            v-model="modelOrigen"
            :options="accion.origenes.origenes"
            label="Tipo de Acción"
            style="width: 10em"
          /> 

        </div>        
      
    </div>
    <q-btn
      label="   Filtrar   "
      @click="filtraAcciones"
      class="q-ma-sm"
      no-caps
      color="btnContinuar"
    />
    <q-btn
      label="Limpiar Filtros"
      @click="limpiarFiltros"
      class="q-ma-sm"
      no-caps
      color="btnCancelar"
    />
    <q-space />
    <q-separator/>

    <q-table
      :rows="accion.acciones"
      :columns="opciones"
      row-key="id"
      
      v-model:selected="selected"
      :visible-columns="columnasVisibles"
      @selection="seleccionaFila"
      
      :pagination="initialPagination"
      no-data-label="No hay acciones para el filtro aplicado"
      class="tablaAcciones"
    >
    <!--
      //:rows="acciones"
      //:filter="filter"
    -->
      <template v-slot:body-cell-estrategias="props">
        <q-td :props="props">
          <ul>
            <li v-for="item in props.value" :key="item.id">
              {{ item.id_uaysen }}
              <q-tooltip class="text-body1">{{ item.descripcion }}</q-tooltip>
            </li>
          </ul>
        </q-td>
      </template>
      <template v-slot:top-right>
        <q-btn
          color="primary"
          icon-right="archive"
          label="Descargar"
          no-caps
          @click="exportExcel"
        />
      </template>
      <!--<template v-slot:top-right>
        <q-input
          white
          outlined
          rounded
          filled
          borderless
          dense
          debounce="300"
          v-model="filter"
          placeholder="Buscar"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>  
      </template>-->
      
      <!-- <template v-slot:top-left="props">
        <div v-if="$q.screen.gt.xs" style="min-width: 600px">
          <div class="row">
            <div class="col-4">
              <q-toggle
                v-model="columnasVisibles"
                val="objetivo"
                label="Objetivo de la acción"
              />
            </div> -->
            <!-- <div class="col-4">
              <q-toggle
                v-model="columnasVisibles"
                val="tipo"
                label="Tipo de acción"
              />
            </div> -->
            <!-- <div class="col-4">
              <q-toggle
                v-model="columnasVisibles"
                val="proyecto"
                label="Proyecto"
              />
            </div>
          </div>
          <div class="row">
            <div class="col-4">
              <q-toggle
                v-model="columnasVisibles"
                val="estrategias"
                label="Estrategias"
              />
            </div> -->
            <!--<div class="col-4">
              <q-toggle
                v-model="columnasVisibles"
                val="presupuesto"
                label="Presupuesto"
              />
            </div>-->
            <!-- <div class="col-4">
              <q-toggle v-model="columnasVisibles" 
                val="tributa" 
                label="Tributa" />
            </div>
            <div class="col-4">
              <q-toggle v-model="columnasVisibles" 
                val="anio" 
                label="Año" />
            </div>
          </div>
        </div>
  
      </template> -->
    </q-table>
  
  
  
  </div>
</template>

<script>
import { defineComponent, computed, onMounted, onUnmounted, ref } from "vue";
import { useStore, mapState } from "vuex";
import { exportFile } from "quasar";

export default defineComponent({
  setup() {
    const store = useStore();
    const accion = computed(() => store.state.accion);
    const usuario = computed(() => store.state.usuarix);
    const actor = computed(() => store.state.actor);
    const modelDireccion = ref("Todos");
    const modelUnidad = ref("Todos");
    const modelActor = ref({ label: "Todos", value: "Todos" });
    //const modelActores = ref("Todos");
    const modelRol = ref("Todos");
    const modelTipo = ref("Todos");
    const modelPeriodo = ref("Todos");
    const modelOrigen  = ref("Todos");
    onMounted(() => {
      store.dispatch("accion/reqAniosDisponibles");
      store.dispatch("accion/origenesDisponibles");
    });

    const formatearEstrategias = (arregloEstrategias) => {

      let estrategias = '';
      arregloEstrategias.forEach(element => {
        if(!(arregloEstrategias[arregloEstrategias.length -1].id === element.id)){
          estrategias+= element.id_uaysen+"\n";
        }else{
          estrategias = estrategias + element.id_uaysen
        }
      });    
      return estrategias;
    };

    const wrapCsvValue = (val, formatFn, row) => {
      
      if(Array.isArray(val)){
        val = formatearEstrategias(val);
      }
      let formatted = formatFn !== void 0 ? formatFn(val, row) : val;
      formatted =
        formatted === void 0 || formatted === null ? "" : String(formatted);

      formatted = formatted.split('"').join('""');
      return `"${formatted}"`;
    };

    const formatterPeso = new Intl.NumberFormat("es-CL", {
            style: "currency",
            currency: "CLP",
            minimumFractionDigits: 0,
    });

    const cambioDireccion = (value) => {
      store.dispatch("actor/limpiaUnidad");
      store.dispatch("actor/limpiaActores");
      modelUnidad.value = "Todos";
      //modelActores.value = "Todos";
      
      if(value !== "Todos"){
        store.dispatch("actor/reqUnidad", value.id);
      }else{
        store.dispatch("actor/reqUnidades");
      }
    };

    const cambioUnidad = (value) => {
      store.dispatch("actor/limpiaActores");

      //modelActores.value = "Todos";
      if(value !== "Todos"){
        store.dispatch("actor/reqFiltroActores", value.id);
      }
    };

    //Nueva Tabla
    const procesoAcreditacion = "Proceso de Acreditación";
    const opciones = [
      {
        name: "accion",
        label: "Acción",
        field: (row) => (row ? row.id_uaysen : ""),
        align: "left",
        sortable: true,
      },
      {
        name: "titulo",
        label: "Título",
        field: (row) => (row ? row.titulo : ""),
        align: "left",
        style: "white-space: normal",
      },
      {
        name: "objetivo",
        label: "Objetivo de la acción",
        field: (row) => (row ? row.objetivo : ""),
        align: "left",
        style: "white-space: normal",
      },
      {
        name: "tipo",
        label: "Tipo",
        field: (row) => (row ? row.tipo : ""),
        align: "left",
        sortable: true,
      },
      {
        name: "proyecto",
        label: "Proyecto",
        field: (row) => (row ? row.proyecto : "No tiene"),
        align: "left",
        sortable: true,
      },
      {
        name: "presupuesto",
        label: "Presupuesto",
        field: (row) =>
          row ? formatterPeso.format(row.presupuesto) : "",
        align: "left",
        sortable: true,
      },
    {
        name: "tributa",
        label: "Tributa",
        field: (row) => { 
          if(row.origen === "PMI"){
              return procesoAcreditacion;
          }else{
            if(row.estrategias.length){
              return procesoAcreditacion;
            }else{
              return "";
            }
          }
        },
        align: "left",
        sortable: true,
      },
      {
        name: "estrategias",
        label: "Estrategias",
        field: (row) => (row ? row.estrategias : ""),
        align: "left",
        sortable: true,
      },
      {
        name: "anio",
        label: "Año",
        field: (row) => (row ? row.anio : ""),
        align: "left",
        sortable: true,
      },
    ];
    const columnasVisibles = ref([
      "accion",
      "titulo",
      "objetivo",      
      "tipo",
      "proyecto",
      "tributa",      
      "estrategias",
      "anio",      
    ]);
    const seleccionaFila = (detalles) => {
      //window.scroll({ top: 0, left: 0, behavior: "smooth" });
      console.log("detalles ¡ ", detalles)
      if (detalles.added) {
        store.dispatch(
          "accion/reqHitosYFuncionesPorAccion",
          detalles.rows[0].id
        );
        //store.dispatch("entrega/setNuevaEntrega", detalles.rows[0].accion);
      }
    };
    //Nueva Tabla

    const columnasTabla = [
      {
        name: "accion",
        label: "Acción",
        field: "id_uaysen",
        align: "left",
        sortable: true,
      },
      {
        name: "titulo",
        label: "Título",
        field: "titulo",
        align: "left",
        style: "white-space: normal",
      },
      {
        name: "objetivo",
        label: "Objetivo de la acción",
        field: "objetivo",
        align: "left",
        style: "white-space: normal",
      },
      {
        name: "tipo",
        label: "Tipo",
        field: "tipo",
        align: "left",
        sortable: true,
      },
      {
        name: "tributa",
        label: "Tributa",
        field: (row) => {

          if(row.estrategias.find(element => element.tipo === "PEDI")){
            return "Proceso de Acreditación";
          }else{
            return "";
          }
          
        },
        align: "left",
        sortable: true,
      },
      {
        name: "proyecto",
        label: "Proyecto",
        field: "proyecto",
        align: "left",
        sortable: true,
      },
      {
        name: "presupuesto",
        label: "Presupuesto",
        //field: "presupuesto",
        field: (row) =>
            row ? formatterPeso.format(row.presupuesto) : "",
        align: "right",
        sortable: true,
      },
      /*{
        name: "estrategias",
        label: "Estrategias",
        //field: (row) => (row.accion ? row.accion.estrategias : ""),
        field:"estrategias",
        align: "left",
        sortable: true,
      },*/
    ];

    onMounted(() => {
      store.dispatch("actor/reqDirecciones");
      store.dispatch("actor/reqUnidades");
      store.dispatch("accion/limpiaAcciones");
    });

    onUnmounted(() => {
      store.dispatch("accion/limpiaAcciones");
    });
    
    return {      
      cambioDireccion,
      cambioUnidad,
      modelPeriodo,
      modelOrigen,
      actor,
      accion,
      usuario,
      
      modelDireccion,
      modelUnidad,
      //modelActores,    

      modelActor,
      modelRol,
      modelTipo,
      columnasTabla,
      filtraAcciones: () => {       
          let actor = "Todos";

          if(modelDireccion.value.id){
            actor = modelDireccion.value.id;
          } 
          
          if(modelUnidad.value.id){
            actor = modelUnidad.value.id;
          } 
          
          store.dispatch("accion/reqFiltraAcciones", {
          
          actor: actor,
          rol: modelRol.value,
          tipo: modelTipo.value,
          anio: modelPeriodo.value,
          origen: modelOrigen.value,
        });        
      },
      limpiarFiltros: () => {
          modelActor.value = "Todos";
          modelRol.value = "Todos";
          modelTipo.value = "Todos";
          //modelActores.value = "Todos";
          modelUnidad.value = "Todos";
          modelDireccion.value = "Todos";
          modelPeriodo.value = "Todos";
          modelOrigen.value = "Todos";
      },
      exportTable() {
        // naive encoding to csv format
        const content = [columnasTabla.map((col) => wrapCsvValue(col.label))]
          .concat(
            accion.value.acciones.map((row) =>
              columnasTabla
                .map((col) =>
                  wrapCsvValue(
                    typeof col.field === "function"
                      ? col.field(row)
                      : row[col.field === void 0 ? col.name : col.field],
                    col.format,
                    row
                  )
                )
                .join(",")
            )
          )
          .join("\r\n");


        const status = exportFile(
          "datos_del_navegador_poa.csv",
          content,
            {
              mimeType: "application/vnd.ms-excel",
              //mimeType: "text/csv",
              byteOrderMark: '\uFEFF',
              encoding: "ISO-8859-1",
            }
        );

        if (status !== true) {
          $q.notify({
            message: "Browser denied file download...",
            color: "negative",
            icon: "warning",
          });
        }
      },
      //Nueva tabla
      opciones,
      selected: ref([]),
      columnasVisibles: columnasVisibles,
      seleccionaFila: seleccionaFila,
      initialPagination: {
        page: 1,
        rowsPerPage: 5,
      },

      exportExcel() {
        let opcionesAexcel  = [];
        opciones.map((col) => {
          if(columnasVisibles.value.find(columna => columna == col.name)){
            opcionesAexcel.push(col);
          }
        });

        const content = [opcionesAexcel.map((col) => wrapCsvValue(col.label))]
          .concat(
            accion.value.acciones.map((row) =>
            opcionesAexcel
                .map((col) =>
                  wrapCsvValue(
                    typeof col.field === "function"
                      ? col.field(row)
                      : row[col.field === void 0 ? col.name : col.field],
                    col.format,
                    row
                  )
                )
                .join(",")
            )
          )
          .join("\r\n");

        let contenidoSeparado = "sep=," + "\r" + content;
        
        store.dispatch("reporte/generaReporteNavegadorPOA", contenidoSeparado);
      },
      //Nueva Tabla
    };
  },
  computed: {
    ...mapState(["accion", "usuarix"]),
  },
});
</script>

