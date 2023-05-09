<template>    
  <div class="q-pa-md" v-if="selected.length">
    <q-card style="width: 250%">
      <PopupAccionDescripcion
        :accion="selected[0]"
        :mostrar="mostrarPopupDescripcion"
        @update:mostrar="mostrarPopupDescripcion = $event"
      />
      <PopupAccionEstrategias
        :estrategias="selected[0].accion.estrategias"
        :accion="selected[0]"
        :mostrar="mostrarPopupEstrategias"
        @update:mostrar="mostrarPopupEstrategias = $event"
      />
    </q-card>
    <q-card class="tarjetaAmarilla">
      <q-splitter v-model="splitterModel" style="height: 400px">
        <template v-slot:before>
          <q-tabs v-model="tab" vertical>
            <q-tab name="funciones" icon="construction"><b>Funciones</b></q-tab>
            <q-tab name="hitos" icon="event_available"><b>Hitos</b></q-tab>
          </q-tabs>
        </template>
        <template v-slot:after>
          
          <div v-if="detalleAccion.detalleAccion">
            <div class="text-h4 q-pa-md">
              <b>{{ selected[0].accion.id_uaysen }}</b>
            </div>
            <q-tab-panels
              v-model="tab"
              animated
              transition-prev="slide-down"
              transition-next="slide-up"
            >
            {{ cambioReferencia() }}

              <q-tab-panel name="funciones" class="tarjetaAmarilla">
                <div class="text-h6 q-mb-md" v-if="mantencionPOA2023">
                  En Mantención según POA 2023.
                </div>
                <div v-if="!mantencionPOA2023">
                  
                  <div class="text-h6 q-mb-md">
                    <b>Funciones de la acción seleccionada</b>
                  </div>
                  
                  <q-list bordered separator>
                    <q-item
                      v-ripple
                      v-for="(item, index) in detalleAccion.detalleAccion.funciones"
                      :key="item.value"
                    >
                      <q-item-section side>
                        {{ index + 1 }}
                      </q-item-section>
                      <q-item-section>{{ item.label }} </q-item-section>
                    </q-item>
                  </q-list>

                </div>

                <BotonSubirEntregable
                  tipoEntrega="verificador"
                  tipoTactica="funciones"
                  :referencia="referencia"
                  @mantencion="manejoMantencion"
                />
                
              </q-tab-panel>
              <q-tab-panel name="hitos" class="tarjetaAmarilla">
                <div class="text-h6 q-mb-md" v-if="mantencionPOA2023">
                  En Mantención según POA 2023.
                </div>
                
                <div v-if="!mantencionPOA2023">
                  <div class="text-h6 q-mb-md">
                    <b>Hitos de la acción seleccionada</b>
                  </div>
                  <q-list bordered separator>
                    <q-item
                      v-ripple
                      v-for="(item, index) in detalleAccion.detalleAccion.hitos"
                      :key="item.value"
                    >
                      <q-item-section side>
                        {{ index + 1 }}
                      </q-item-section>
  
                      <q-item-section>
                        <q-item-label class="text-textoAzul"
                          ><b>{{ item.label }}</b></q-item-label
                        >
                        <q-item-label class="text-textoAzul" caption>
                          {{ item.descripcion }}
                        </q-item-label>
                      </q-item-section>
                      <q-separator vertical/>
                      <div class="flex-bottom col-3 q-px-lg">
                        <ManejoPlazo 
                          :hito="item"
                        />
                      </div>
                      
                    </q-item>
                  </q-list>
                </div>

                <BotonSubirEntregable
                  tipoEntrega="producto"
                  tipoTactica="hitos"
                  :referencia="referencia"
                  @mantencion="manejoMantencion"
                />
              </q-tab-panel>
            </q-tab-panels>
            <div class="flex-bottom col-xxl-5">
              <q-btn
                class="q-ma-sm bg-btnVolver"
                unelevated
                rounded
                size="sm"
                color="primary"
                label="Ver estrategias"
                @click="mostrarPopupEstrategias = !mostrarPopupEstrategias"
              >
              </q-btn>
              <q-btn
                class="q-ma-sm bg-btnVolver"
                unelevated
                rounded
                size="sm"
                color="primary"
                label="Ver detalles"
                @click="mostrarPopupDescripcion = !mostrarPopupDescripcion"
              >
              </q-btn>
            </div>
          </div>
        </template>
      </q-splitter>
    </q-card>
    <q-btn
      class="q-ma-sm"
      color="btnCancelar"
      label="Cancelar"
      @click="cancelar"
    />
    <!--@click="selected = []"-->
  </div>
  <div class="q-px-sm">
    <q-table
      :rows="acciones"
      :columns="opciones"
      row-key="id"
      selection="single"
      v-model:selected="selected"
      :visible-columns="columnasVisibles"
      @selection="seleccionaFila"
      :filter="filter"
      :filter-method="customFilter"
      :pagination="initialPagination"
      no-data-label="No hay acciones para el filtro aplicado"
      class="tablaAcciones"
    >
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
      </template>
      <template v-slot:top-left="props">
        <div v-if="$q.screen.gt.xs" style="min-width: 600px">
          <!-- <div class="row">
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
          </div> -->
          <!-- <div class="row">
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
              <q-toggle 
                v-model="columnasVisibles" 
                val="actor" 
                label="Actor" 
              />
            </div>
            <div class="col-4">
              <q-toggle 
                v-model="columnasVisibles" 
                val="anio" 
                label="Período" 
              />
            </div>
          </div> -->
        </div>
        <q-select
          v-else
          v-model="columnasVisibles"
          multiple
          borderless
          dense
          options-dense
          :display-value="$q.lang.table.columns"
          emit-value
          map-options
          :options="opciones"
          option-value="name"
          style="min-width: 150px"
        />
      </template>
    </q-table>
  </div>
</template>
<script>
import { ref, toRef, defineComponent, computed } from "vue";
import PopupAccionDescripcion from "src/components/PopupAccionDescripcion.vue";
import PopupAccionEstrategias from "src/components/PopupAccionEstrategias.vue";
import BotonSubirEntregable from "src/components/BotonSubirEntregable.vue";
import ManejoPlazo from "src/components/ManejoPlazo.vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

export default defineComponent({
  components: {
    PopupAccionDescripcion,
    PopupAccionEstrategias,
    BotonSubirEntregable,
    ManejoPlazo,
  },
  props: {
    acciones: Array,
    referencia: String,
  },
  watch: {
    acciones: function (newValue, oldValue) { 
      if(newValue){
        this.cancelar();
      }
    },
    referencia: function(newValue){
      this.manejoMantencion(false);
    }
    
  },
  methods: {
    cambioReferencia(){
      if(this.selected.length){      
        if (this.selected[0].accion.origen === "PMI"){
          this.referencia = "AccionesPMI"
        }else{
          this.referencia = "AccionesPOA"
        }
      }      
    },
    manejoMantencion(mantencion){
      this.mantencionPOA2023 = mantencion
    },
    customFilter(rows, terms){            
      let lowerSearch = this.filter ? this.lowerCase(this.filter) : ""
      
      const filteredRows = rows.filter((row) =>{
          
          if(lowerSearch != ""){
            let rowValues = Object.values(row.accion);

            let rowValuesLower = rowValues.map(elemento => {
              if(elemento){
                //Control para arreglo de estrategias
                if(Array.isArray(elemento)){
                  return elemento;
                }
                return this.lowerCase(elemento.toString());
              }else{
                return "";
              }
            });
            
            for (let val=0; val < rowValuesLower.length; val++){
              if (rowValuesLower[val].includes(lowerSearch)){
                return row;
              }else{
                if(Array.isArray(rowValuesLower[val]) && this.buscaEstrategia(rowValuesLower[val], lowerSearch)){
                  return row;
                }
              }              
            }
          }

        })        
        return filteredRows
    },
    lowerCase(cadena){
      return cadena.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    },
    buscaEstrategia (estrategias, lowerSearch){      
      let encontrado = false;

      for (let val=0; val < estrategias.length; val++){
        let valor = Object.values(estrategias[val]).map(elemento => {
            if(elemento){
              if(typeof elemento === 'object'){
                return "";
              }
              return this.lowerCase(elemento.toString());
            }else{                
              return "";
            }
        });
        
        for (let val = 0; val < valor.length; val++){
          if (valor[val].includes(lowerSearch)){
            encontrado = true;
            break;
          }
        } 

        if(encontrado){
          break;
        }
      }
      return encontrado;
    }
  },
  setup(props) {
    const router = useRouter();
    const store = useStore();
    const detalleAccion = computed(() => store.state.accion);
    const accion = props.acciones;
    const referencia = ref("");
    const mostrarPopupDescripcion = ref(false);
    const mostrarPopupEstrategias = ref(false);
    const mantencionPOA2023 = ref(false);
    const formatterPeso = new Intl.NumberFormat("es-CL", {
      style: "currency",
      currency: "CLP",
      minimumFractionDigits: 0,
    });
    const selected = ref([]);
    const opciones = [
      {
        name: "accion",
        label: "Acción",
        field: (row) => (row.accion ? row.accion.id_uaysen : ""),
        align: "left",
        sortable: true,
      },
      {
        name: "titulo",
        label: "Título",
        field: (row) => (row.accion ? row.accion.titulo : ""),
        align: "left",
        style: "white-space: normal",
      },
      // {
      //   name: "origen",
      //   label: "Tipo de Accion",
      //   field: (row) => {
      //     if(row.accion.origen === "TRANSVERSAL"){          
      //       return "Transversal";
      //     }else{
      //       return row.accion.origen;
      //     }
      //   },
      //   align: "left",
      //   style: "white-space: normal",
      // },
      {
        name: "objetivo",
        label: "Objetivo de la acción",
        field: (row) => (row.accion ? row.accion.objetivo : ""),        
        align: "left",
        style: "white-space: normal",
      },
      {
        name: "tipo",
        label: "Tipo",
        field: (row) => (row.accion ? row.accion.tipo : ""),
        align: "left",
        sortable: true,
      },
      {
        name: "proyecto",
        label: "Proyecto",
        field: (row) => (row.accion ? row.accion.proyecto : "No tiene"),
        align: "left",
        sortable: true,
      },
      {
        name: "presupuesto",
        label: "Presupuesto",
        field: (row) =>
          row.accion ? formatterPeso.format(row.accion.presupuesto) : "",
        align: "left",
        sortable: true,
      },
      {
        name: "estrategias",
        label: "Estrategias",
        field: (row) => (row.accion ? row.accion.estrategias : ""),
        align: "left",
        sortable: true,
      },
      {
        name: "anio",
        label: "Período ",
        field: (row) => (row.accion ? row.accion.anio : ""),
        align: "left",
        sortable: true,
      },
      {
        name: "actor",
        label: "Actor",
        field: (row) => (row.accion ? row.actor.nombre : ""),        
        align: "left",
        style: "white-space: normal",
        sortable: true,
      },
    ];
    const seleccionaFila = async (detalles) => {
      window.scroll({ top: 0, left: 0, behavior: "smooth" });
      if (detalles.added) {
        await store.dispatch(
          "accion/reqHitosYFuncionesPorAccion",
          detalles.rows[0].accion.id
        );
        await store.dispatch("entrega/setNuevaEntrega", detalles.rows[0].accion);
      }
    };
    const columnasVisibles = ref([
      "accion",
      "titulo",
      "objetivo",
      "origen",
      "tipo",
      "proyecto",
      "estrategias",
      "actor",
      "anio"
    ]);
    return {
      mantencionPOA2023,
      detalleAccion,
      acciones: toRef(props, "acciones"),
      //referencia: toRef(props, "referencia"),
      referencia,
      opciones,
      filter: ref(""),
      //selected: ref([]),
      selected,
      columnasVisibles: columnasVisibles,
      seleccionaFila: seleccionaFila,
      initialPagination: {
        page: 1,
        rowsPerPage: 5,
      },
      tab: ref("funciones"),
      splitterModel: ref(15),
      mostrarPopupDescripcion,
      mostrarPopupEstrategias,
      accion,
      cancelar: () => {
        selected.value = [];
      },
    };
  },
});
</script>
