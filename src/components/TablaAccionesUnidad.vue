<template>
    <div class="q-px-sm">        
        <q-table
            :rows="acciones" 
            :columns="opciones"
            selection="multiple"
            v-model:selected="accionesSeleccionadas"
            no-data-label="No hay acciones para el filtro aplicado"
            class="tablaAcciones"
        >
        </q-table>
        <br/>
        
        <q-separator v-if="verReportes" class="text-textoAzul" horizontal/>        
        
        <TablaReportes
            v-if="verReportes"
            :reportes="reportesFiltrados"
        />
        
        <div class="q-pa-md" >    
            <div class="row justify-end q-gutter-sm q-ma-md">                
                <q-btn
                    v-if="accionesSeleccionadas.length"
                    class="q-ma-sm"
                    color="btnCancelar"
                    label="   Cancelar   "
                    @click="accionesSeleccionadas = []"
                />
                <q-btn
                    class="q-ma-sm"
                    color="btnContinuar"
                    :label="labelVerReportes"
                    @click="verReportesFinalizados"
                />
                <q-btn
                    v-if="accionesSeleccionadas.length"
                    class="q-ma-sm"
                    label="   Reporte    "                
                    color="light-blue-10"
                    @click="accionBoton"
                />
            </div>
        </div>
    </div>
</template>
<script>
import { ref, toRef ,computed, onMounted, onUnmounted, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import TablaReportes from "src/components/componentesReportes/TablaReportes.vue";

export default defineComponent({
    components:{
        TablaReportes,
    },
    props: {
        acciones: Array,
        id_responsable: Number,
        origen: String,
        reportes: Array,
    },
    watch: {
        id_responsable (newValue){
            this.verReportes = false;
            this.labelVerReportes ="Ver Finalizados";
            this.reportesFiltrados = reportes.filter(elemento => elemento.actor == newValue);
        }
    },
    setup(props) {
        const router = useRouter();
        const store = useStore();
        const usuario = computed(() => store.state.usuarix.usuario);
        //const id_responsable = props.id_responsable;
        const id_responsable = computed({
            get: () => props.id_responsable
        });
        const reportes = computed({
            get:() => props.reportes
        });
        const reportesFiltrados = ref();
        const accion = computed(() => store.state.accion.accion);
        const accionesSeleccionadas = ref([]);
        const origen = props.origen;
        const verReportes = ref(false);
        const labelVerReportes = ref("Ver Finalizados");

        onMounted(() => {
            store.dispatch("accion/limpiaAccionAReportar");
        });
        const columnasVisibles = ref([
            "accion",
            "titulo",
            "tipo",
            //"estrategias",        
        ]);
        
        return {
            reportes,
            reportesFiltrados,
            origen,
            accion,
            acciones: toRef(props, "acciones"),
            id_responsable,
            verReportes,
            labelVerReportes,
            opciones: [
                {
                    name: "accion",
                    label: "Acción",
                    //field: (row) => (row.accion ? row.accion.id_uaysen : ""),
                    field: (row) => (row.accion.id_uaysen),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "titulo",
                    label: "Título",
                    //field: (row) => (row.accion ? row.accion.titulo : ""),
                    field: (row) => (row.accion.titulo),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "tipo",
                    label: "Tipo",
                    //field: (row) => (row.accion ? row.accion.tipo : ""),
                    field: (row) => (row.accion.tipo),
                    align: "left",
                    sortable: true,
                },
            ],
            usuario,
            accionesSeleccionadas,
            columnasVisibles: columnasVisibles,
            verReportesFinalizados: async () => {
                reportesFiltrados.value = reportes.value.filter(elemento => elemento.actor == id_responsable.value)
                if(origen === "POA"){
                    await store.dispatch("accion/reqAccionesAReporte", id_responsable.value);
                } else{
                    await store.dispatch("accion/reqAccionesAReportePMI", id_responsable.value);
                }
                if(verReportes.value){
                    verReportes.value = false;
                    labelVerReportes.value = "Ver Finalizados"
                }else{
                    labelVerReportes.value = "Ocultar Finalizados"
                    verReportes.value = true;
                }
                
            },
            accionBoton: async () => {        
                const reporte = {
                    usuario: usuario.value.id,
                    actor: accionesSeleccionadas.value[0].actor.id,
                    estado: 'Borrador',
                    recomendacion: '',
                    tipo: "",
                    reporte_acciones: []
                };
                if(origen === "POA"){
                    await store.dispatch("accion/reqAccionesAReporte", accionesSeleccionadas.value[0].actor.id);
                    reporte.tipo = "POA";
                } else{
                    await store.dispatch("accion/reqAccionesAReportePMI", accionesSeleccionadas.value[0].actor.id);
                    reporte.tipo = "PMI";
                }
                

                store.dispatch("reporte/setNuevoReporte", {
                    reporte: reporte,
                    acciones: accionesSeleccionadas.value
                });
                
                
                store.dispatch("accion/reqFuncionesPorAccion", accionesSeleccionadas.value[0].accion.id);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", accionesSeleccionadas.value[0].accion.id);
                store.dispatch("producto/reqHitosReporte", accionesSeleccionadas.value[0].accion.id);
                
                if(origen === "POA"){
                    router.push("reporteUpci");
                }else{
                    router.push("reporteUpciPMI");
                }
                
            },

        };
    },
});
</script>