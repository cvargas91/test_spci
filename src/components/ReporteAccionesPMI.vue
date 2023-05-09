<template> 
    <q-card-section style="margin-right:178pt; margin-left:158pt; height:30pt;">
        <strong style="text-align:center; color:#385280; font-size:12pt">
            Actividades:
        </strong>   
    </q-card-section>

    <q-card-actions align="around" style="padding-bottom:0pt">
        <p style="">
            <strong style="text-align:center; color:#385280; font-size:10pt">
                Logro
            </strong>   
        </p>
        <p>
            <strong style="text-align:center; color:#385280; font-size:10pt; align-right">
                Indicador de logro
            </strong>  
        </p>
    </q-card-actions>

    <q-card-section horizontal style="width:101%;min-height:30pt; margin-bottom:0pt;margin-top:0pt; padding-top:0%;padding-bottom:15pt">
        <div style="background-color:#fcefd5;width:48%; margin-left:0pt; min-height:45pt; margin-right:0pt; height: auto">
            <q-input
                v-model="indicador"
                autogrow
                type="textarea"
                style="margin-left:4pt; margin-right:4pt"
            />  
        </div>
        
        <div style="background-color:#fcefd5;width:48%;min-height:45pt;margin-left:28pt">
            <q-select
                v-model="indicadorLogro" 
                :options="opcionesLogro" 
                label="No logrado/Logrado con atraso/Logrado" 
                style="width: 96%; margin-left: 4pt;"
                />
        </div>
    </q-card-section>     
    
    <br/>
    
    <div class="row" style="border: solid #385280; border-width:0.5px; margin-left:0pt;margin-right:98pt">
        <p style="color:#385280; margin-bottom:4pt;padding-top:4pt; padding-right:165pt;padding-left:5pt">
            <b>3.- Evaluación final</b>
        </p>            
    </div>

        
    <q-card-section style="margin-right:178pt; margin-left:158pt; height:30pt;">
        <strong style="text-align:center; color:#385280; font-size:12pt">
            Actividades:
        </strong>   
    </q-card-section>
    
    
    <q-card-section style="height:30pt; margin-bottom:0pt;margin-top:0pt;padding-top:0pt">
        <q-card-actions align="around">
            <p>
                <strong style="text-align:center; color:#385280; font-size:12pt">
                    Estado de ejecución*
                </strong>   
            </p>
        </q-card-actions>
    </q-card-section>

    <div style="background-color:#d9e2f3;width:101%; margin-right:0pt; margin-left:0pt; min-height:10pt; padding-right:30pt">
        <q-select
            v-model="indicadorEstadoEjecucion" 
            :options="opcionesJustificacion" 
            style="margin-left:4pt;width:105%"
        />
    </div>
    
    <br/>
    <hr style="border: 1.5px dashed #385280;">
        
    <div class="row justify-end q-gutter-sm q-ma-md" style="margin-right:0pt">
        <q-separator inset />
        <BotonCancelarReporte 
            opcion="accion"
            @guardarAvance="guardarAvance"
        />

        <!--<q-btn
            class="q-ml-sm"
            color="btnCancelar"
            label="   Cancelar   "
            @click="cancelarReporte"
        />-->
        <q-btn
            v-if="validaLabelBoton()"
            color="btnVolver"
            @click="cambioAtras"
            :label="labelBotonAtras"
            class="q-ml-sm"
        />
        <q-btn
            v-if="!validaUltimaAccion()"
            color="btnContinuar"
            @click="siguienteAccion"
            label="   Siguiente Acción    "
            class="q-ml-sm"
        />
        <q-btn
            v-if="validaUltimaAccion()"
            color="btnAdjuntar"
            @click="cambioAdelante"
            label="   Guardar Reporte    "
            class="q-ml-sm"
        />
    </div>

</template>
<script>
    import { ref,toRef, watch ,watchEffect, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";    
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";

    export default defineComponent({        
        components:{
            BotonCancelarReporte,
        },
        props: {
            opcionesJustificacion: Array,    
            indiceReporteAccion: Number,
            reporteAccion: Object,
            funciones: Array,
        },
        watch: {        
            reporteAccion: async function (newValue, oldValue) {

                const reporteAccion = {
                    accion: oldValue.accion,
                    estado_ejecucion: this.indicadorEstadoEjecucion,
                    justificacion_contingencia: this.justificacion,
                    reporte_justificacion_contingencia: this.reporteJustificacion,
                    indicador: this.indicador,
                    indicador_logro: this.indicadorLogro,
                    reporte_funciones: oldValue.reporte_funciones,
                    //reporte_funciones: this.nuevoReporte.nuevoReporteFunciones,
                    reporte_hitos: oldValue.reporte_hitos

                };

                await this.$store.dispatch("reporte/actualizaNuevoReporteAccion", reporteAccion);
            },
        },
        emits:["cambioReporteAccion","guardarReporte", "siguienteReporteAccion"],
        setup(props, {emit}) {
            const store = useStore();
            const router = useRouter();
            const accion = computed(() => store.state.accion);
            const accionesAReportar = computed(() => store.state.accion.aReportar.acciones);

            
            const nuevoReporte = computed(() => store.state.reporte);

            const opcionesEjecucion = ["Si", "No"];
            const opcionesLogro = ['No logrado','Logrado con atrasos','Logrado'];
            const labelBotonAtras = ref("Atras");
            const indicadorLogro = ref(props.reporteAccion.indicador_logro);
            const indicadorEstadoEjecucion = ref(props.reporteAccion.estado_ejecucion);
            const reporteJustificacion = ref(props.reporteAccion.reporte_justificacion_contingencia);
            const justificacion = ref(props.reporteAccion.justificacion_contingencia);
            const indicador = ref(props.reporteAccion.indicador);
            const accionesPendientes = ref(true);
            const idAccion = ref(props.reporteAccion.accion);

            const model = computed({
                get:() => {
                    idAccion.value = props.reporteAccion.accion;
                }
            })

            const cambioAdelante = async () => {

                await store.dispatch("reporte/actualizaNuevoReporteFuncionPMI", props.funciones[0].indicador_set[0].funcion);
                
                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: nuevoReporte.value.nuevoReporteFunciones,                    
                    reporte_hitos: nuevoReporte.value.nuevoReporteHitos,
                    indicador: indicador.value,
                    indicador_logro: indicadorLogro.value,
                };

                await store.dispatch("reporte/actualizaNuevoReporteAccion", reporteAccion);

                emit('guardarReporte', true);
            };

            const siguienteAccion = async () => {
                
                await store.dispatch("reporte/actualizaNuevoReporteFuncionPMI", props.funciones[0].indicador_set[0].funcion);

                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: nuevoReporte.value.nuevoReporteFunciones,                    
                    reporte_hitos: nuevoReporte.value.nuevoReporteHitos,
                    indicador: indicador.value,
                    indicador_logro: indicadorLogro.value,
                };

                
                await store.dispatch("reporte/actualizaNuevoReporteAccion", reporteAccion);
            
                emit('siguienteReporteAccion', props.indiceReporteAccion + 1);
            };

            const cambioAtras = async () => {
                
                await store.dispatch("reporte/actualizaNuevoReporteFuncionPMI", props.funciones[0].indicador_set[0].funcion);

                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: nuevoReporte.value.nuevoReporteFunciones,
                    reporte_hitos: nuevoReporte.value.nuevoReporteHitos,
                    indicador: indicador.value,
                    indicador_logro: indicadorLogro.value,
                }

                
                await store.dispatch("reporte/actualizaNuevoReporteAccion", reporteAccion);

                store.dispatch("accion/reqDetalleAccion", idAccion.value);
                store.dispatch("accion/reqFuncionesPorAccion", idAccion.value);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", idAccion.value);
                store.dispatch("producto/reqHitosReporte", idAccion.value);

                store.dispatch("reporte/setNuevoReporteHito", nuevoReporte.value.nuevoReporteHitos);
                store.dispatch("reporte/setNuevoReporteFuncion", nuevoReporte.value.nuevoReporteFunciones);
                emit('cambioReporteAccion', reporteAccion);
            };

            const validaLabelBoton = () => {                
                labelBotonAtras.value = "Volver a Actividades";
                return true;
            };

            const validaUltimaAccion = () => {
                if(props.indiceReporteAccion === (nuevoReporte.value.nuevoReporte.reporte_acciones.length -1)){
                    return true;
                }else{
                    return false;
                }
            }

            const guardarAvance = async () => {
                await store.dispatch("reporte/actualizaNuevoReporteFuncionPMI", props.funciones[0].indicador_set[0].funcion);

                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: nuevoReporte.value.nuevoReporteFunciones,
                    reporte_hitos: nuevoReporte.value.nuevoReporteHitos,
                    indicador: indicador.value,
                    indicador_logro: indicadorLogro.value,
                };

                await store.dispatch("reporte/actualizaNuevoReporteAccion", reporteAccion);

                store.dispatch("reporte/postReporte", nuevoReporte.value.nuevoReporte);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");
                

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };

            return {
                nuevoReporte,
                labelBotonAtras,
                model,
                cambioAdelante,
                siguienteAccion,
                cambioAtras,
                validaLabelBoton,
                validaUltimaAccion,
                guardarAvance,
                opcionesLogro,
                indicadorLogro,
                accionesAReportar,
                idAccion,
                accion,
                accionesPendientes,
                
                opcionesJustificacion: toRef(props,"opcionesJustificacion"),
                opcionesEjecucion,
                
                justificacion,
                indicador,
                indicadorEstadoEjecucion,

                reporteJustificacion,
                indiceReporteAccion: toRef(props, "indiceReporteAccion"),
            }
        }
    })
</script>