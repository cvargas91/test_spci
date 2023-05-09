<template>
    <PopupGenerarReporte
        :mostrar="mostrarPopupGenerarReporte"
        @update:mostrar="mostrarPopupGenerarReporte = $event"
        @respuestaPopup="mostrarPopupGenerarReporte"
    />
    <div class="q-px-sm"> 
        <TablaReportes
            :reportes="reportes"
            :reporteSeleccionado="accionesSeleccionadas"
            :opcion="true"
            @cambio-seleccion="actualizarSeleccion"
        />
        
        <div class="q-pa-md" v-if="accionesSeleccionadas.length">    
            <div class="row justify-end q-gutter-sm q-ma-md">
                <q-btn
                    class="q-ma-sm"
                    color="btnCancelar"
                    label="   Cancelar   "
                    @click="accionesSeleccionadas = []"
                />
                <q-btn
                    v-if="!seRenderea"
                    class="q-ma-sm"
                    color="positive"
                    label="   Editar    "                
                    @click="accionBotonEdicion"
                />
                <q-btn
                    v-if="seRenderea"
                    class="q-ma-sm"
                    label="   Marcar como Enviado    "                
                    color="secondary"
                    @click="accionEnviarReporte"
                />
                <q-btn
                    v-if="seRenderea"
                    class="q-ma-sm"
                    label="   Descargar    "                
                    color="light-blue-10"
                    @click="accionBotonGeneracion"
                />
            </div>
        </div>
    </div>
</template>

<script>
import { ref, toRef,computed, onMounted, onUnmounted, defineComponent } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

import PopupGenerarReporte from "src/components/componentesReportes/PopupGenerarReporte.vue";
import TablaReportes from "src/components/componentesReportes/TablaReportes.vue";

export default defineComponent({
    components:{
        PopupGenerarReporte,
        TablaReportes
    },
    props: {
        reportes: Array,
    },
    methods: {
        actualizarSeleccion(nuevaSeleccion) {
            this.accionesSeleccionadas = nuevaSeleccion;
        },
    },
    setup(props) {
        const store = useStore();        
        const router = useRouter();
        const accionesSeleccionadas = ref([]);
        const actores = computed(() => store.state.actor.actores);
        
        const seRenderea = ref(false);
        const reportes = computed({
            get:() => props.reportes
        });
        const mostrarPopupGenerarReporte = ref(false);
        onMounted(()=> {
            store.dispatch("accion/reqAccionesPorRolResponsable", 0);
        });
        
        if(props.reportes.length){
            if(props.reportes[0].estado === "Finalizado"){
                seRenderea.value = true;
            }
        }else{
            
        }      
        const getValor = (actor) => {
            let detalleActor = actores.value.filter(elemento => elemento.id === actor).map(detalle => detalle.id_uaysen);
            return (detalleActor);
        }
        return {
            mostrarPopupGenerarReporte,
            filter: ref(''),
            getValor,
            actores,
            accionesSeleccionadas,
            reportes,//: toRef(props, "reportes"),
            seRenderea,
            
            accionBotonEdicion: async () => {
                //await store.dispatch("accion/reqAccionesAReporte", accionesSeleccionadas.value[0].actor);
                if(accionesSeleccionadas.value[0].tipo === "POA"){
                    await store.dispatch("accion/reqAccionesAReporte", accionesSeleccionadas.value[0].actor);
                } else{ 
                    await store.dispatch("accion/reqAccionesAReportePMI", accionesSeleccionadas.value[0].actor);
                }

                await store.dispatch("accion/reqDetalleAccion", accionesSeleccionadas.value[0].reporte_acciones[0].accion);
                store.dispatch("accion/reqFuncionesPorAccion", accionesSeleccionadas.value[0].reporte_acciones[0].accion);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", accionesSeleccionadas.value[0].reporte_acciones[0].accion);
                store.dispatch("producto/reqHitosReporte", accionesSeleccionadas.value[0].reporte_acciones[0].accion);
                
                store.dispatch("reporte/setReporteAEditar", accionesSeleccionadas.value[0]);
                store.dispatch("reporte/setReporteHitosAEditar", accionesSeleccionadas.value[0].reporte_acciones[0].reporte_hitos);
                store.dispatch("reporte/setReporteFuncionesAEditar", accionesSeleccionadas.value[0].reporte_acciones[0].reporte_funciones)
                
                if(accionesSeleccionadas.value[0].tipo === "POA"){
                    router.push("reporteUpciEdicion");
                }else{
                    router.push("reporteUpciEdicionPMI");
                }
            },
            accionBotonGeneracion: async () => {
                mostrarPopupGenerarReporte.value = true;
                let getActor = getValor(accionesSeleccionadas.value[0].actor);
                getActor.push(accionesSeleccionadas.value[0].modificado.substring(0, 10));

                getActor.push(accionesSeleccionadas.value[0].id);
                
                if(accionesSeleccionadas.value[0].tipo === "POA"){
                    await store.dispatch("reporte/generaReporte", getActor);
                }else{
                    await store.dispatch("reporte/generaReportePMI", getActor);
                }
                
                accionesSeleccionadas.value=[];

                mostrarPopupGenerarReporte.value = false;
                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");
                router.push("panelReportesUpci");
            },
            accionEnviarReporte: async () => {            
                mostrarPopupGenerarReporte.value = true;                

                const reporteAGuardar = {
                    id: accionesSeleccionadas.value[0].id,
                    usuario: accionesSeleccionadas.value[0].usuario,
                    actor: accionesSeleccionadas.value[0].actor,
                    estado: "Finalizado",
                    enviado: true,
                    recomendacion: accionesSeleccionadas.value[0].recomendacion,
                    tipo : accionesSeleccionadas.value[0].tipo,
                    reporte_acciones: accionesSeleccionadas.value[0].reporte_acciones
                }
                

                await store.dispatch("reporte/patchReporte", reporteAGuardar);            
                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");
                accionesSeleccionadas.value=[];

                mostrarPopupGenerarReporte.value = false;
                router.push("panelReportesUpci");
                
            }

        };
    }
    
});
</script>